"""CPU functionality."""
import sys
class CPU:
    """Main CPU class."""
    def __init__(self):
        self.ram = 256 * [0]      # hold 256 bytes of memory   
        self.reg = [0] * 8        # 8 general-purpose registers.
        self.pc = 0               # internal register prop
        self.reg[7] = 0xFF        # Add stack pointer 
        self.sp = 7               # Set it to 7
        self.fl = 0b00000000
        # opcodes
        self.opcodes = {
            "LDI": 0b10000010,    # load "immediate", store a value in a register, or "set this register to this value".
            "PRN": 0b01000111,    # a pseudo-instruction that prints the numeric value stored in a register.
            "HLT": 0b00000001,    # halt the CPU and exit the emulator.
            "MUL": 0b10100010,
            "PUSH": 0b01000101,
            "POP": 0b01000110,
            "CALL": 0b01010000,
            "RET": 0b00010001,
            "ADD": 0b10100000,
            "CMP": 0b10100111,
            "JMP": 0b01010100,
            "JEQ": 0b01010101,
            "JNE": 0b01010110
        }
    # RAM functions
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, address, value):
        self.ram[address] = value
    # stack_push function 
    def stack_push(self, value):
        self.alu("DEC", self.sp, self.reg[value])
        self.ram_write(self.reg[self.sp], value)
    # stack_pop function 
    def stack_pop(self, value):
        popped = self.ram_read(self.reg[self.sp])
        self.alu("INC", self.sp, value)
        return popped
    # return function 
    def RET(self, value):
        self.pc = self.stack_pop(self)  
    # add function to check for output
    def ADD(self, reg_data, reg_val):
        self.alu("ADD", reg_data, reg_val)
        self.pc += 3
    def load(self, filename):
        """Load a program into memory."""
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    # split before and after any comment symbols
                    comment_split = line.split('#')
                    # convert the pre-comment portion to a value
                    number = comment_split[0].strip()  # trim whitespace
                    if number == "":
                        continue  # ignore blank lines
                    val = int(number, 2)
                    # store it in memory
                    self.ram_write(address, val)
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # increment op for stack
        elif op == "INC":
            self.reg[reg_a] += 1
        # decrement op for stack
        elif op == "DEC":
            self.reg[reg_a] -= 1
        # change flags based on the operands given to the CMP opcode.
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            else:
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def run(self):
        """Run the CPU."""
        # running?
        running = True
        # fetch decode execute
        while running:
            # Fetch
            instruction = self.ram[self.pc]
            # Decode
            if instruction == self.opcodes["HLT"]:
                self.running = False
                sys.exit(1)
            elif instruction == self.opcodes["LDI"]:
                reg_data = self.ram[self.pc+1]
                reg_val = self.ram[self.pc+2]
                self.reg[reg_data] = reg_val
                self.pc += 3
            elif instruction == self.opcodes["PRN"]:
                reg_data = self.ram[self.pc+1]
                print(self.reg[reg_data])
                self.pc += 2
            elif instruction == self.opcodes["MUL"]:
                reg_data = self.ram_read(self.pc + 1)
                reg_val = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_data, reg_val)
                self.pc += 3
            elif instruction == self.opcodes["PUSH"]:
                reg_data = self.ram_read(self.pc + 1)
                self.stack_push(self.reg[reg_data])
                self.pc += 2
            elif instruction == self.opcodes["POP"]:
                reg_data = self.ram_read(self.pc + 1)
                self.reg[reg_data] = self.stack_pop(self.reg[reg_data])
                self.pc += 2
            elif instruction == self.opcodes["CALL"]:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                next_instruction = self.ram[self.pc + 1]
                self.pc = self.reg[next_instruction]
            elif instruction == self.opcodes["RET"]:
                self.pc = self.stack_pop(self)
            elif instruction == self.opcodes["ADD"]:
                reg_data = self.ram_read(self.pc + 1)
                reg_val = self.ram_read(self.pc + 2)
                self.alu("ADD", reg_data, reg_val)
                self.pc += 3
            # CMP
            elif instruction == self.opcodes["CMP"]:
                reg_data = self.ram_read(self.pc + 1)
                reg_val = self.ram_read(self.pc + 2)
                self.alu("CMP", reg_data, reg_val)
                self.pc += 3
            # JMP
            elif instruction == self.opcodes["JMP"]:
                reg_data = self.ram_read(self.pc + 1)
                # Set the pc to be the address stored in the given register
                self.pc = self.reg[reg_data]
            # JEQ
            elif instruction == self.opcodes["JEQ"]:
                reg_data = self.ram_read(self.pc + 1)
                # Check if equal flag is set
                # Then jump to the address stored in the given register
                if self.fl == 0b00000001:
                    self.pc = self.reg[reg_data]
                else:
                    self.pc += 2
            # JNE
            elif instruction == self.opcodes["JNE"]:
                reg_data = self.ram_read(self.pc + 1)
                # Check If equal flag is clear, 
                # Then jump to the address stored in the given register
                if self.fl != 0b00000001:
                    self.pc = self.reg[reg_data]
                else:
                    self.pc += 2
            else:
                sys.exit(1)
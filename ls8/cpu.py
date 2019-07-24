"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = 256 * [0]      # hold 256 bytes of memory   
        self.reg = [0] * 8        # 8 general-purpose registers.
        self.pc = 0               # internal register prop
        # opcodes
        self.opcodes = {
            "LDI": 0b10000010,    # load "immediate", store a value in a register, or "set this register to this value".
            "PRN": 0b01000111,    # a pseudo-instruction that prints the numeric value stored in a register.
            "HLT": 0b00000001,    # halt the CPU and exit the emulator.
        }
        
    def increment_pc(self, op_code):
        add_to_pc = (op_code >> 6) + 1
        self.pc += add_to_pc    
    # RAM functions
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
     
    def load(self):
        """Load a program into memory."""

        address = 0
# same as toms lecture
        try:
            with open(filename) as f:
                for line in f:
                    # split before and after any comment symbols
                    comment_split = line.split('#')
                    # convert the pre-comment portion to a value
                    number = comment_split[0].strip() # trim whitespace

                    if number == "":
                        continue # ignore blank lines

                    val = int(number, 2)

                    # store it in memory
                    memory[address] = val

                    address += 1 
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
            if instruction == self.opcodes['HLT']:
                self.running = False
            elif instruction == self.opcodes['LDI']:
                reg_data = self.ram[self.pc+1]
                reg_val = self.ram[self.pc+2]
                self.reg[reg_data] = reg_val
                self.pc += 3
            elif instruction == self.opcodes['PRN']:
                reg_data = self.ram[self.pc+1]
                print(self.reg[reg_data])
                self.pc += 2
        
            else:
                sys.exit(1)

  def process(self):
        """
        Process a single opcode from the current program counter.  This is
        normally called from the running loop, but can also be called
        manually to provide a "step-by-step" debugging interface, or
        to slow down execution using time.sleep().  This is the method
        that will also need to used if you build a TK/GTK/Qt/curses frontend
        to control execution in another thread of operation.
        """
        self.fetch()
        opcode, data = int(math.floor(self.ir / 100)), self.ir % 100
        self.__opcodes[opcode](data)
    def opcode_0(self, data):
        """ INPUT Operation """
        self.mem[data] = self.reader.pop()
    def opcode_1(self, data):
        """ Clear and Add Operation """
        self.acc = self.get_memint(data)
    def opcode_2(self, data):
        """ Add Operation """
        self.acc += self.get_memint(data)
    def opcode_3(self, data):
        """ Test Accumulator contents Operation """
        if self.acc < 0:
            self.pc = data
    def opcode_4(self, data):
        """ Shift operation """
        x,y = int(math.floor(data / 10)), int(data % 10)
        for i in range(0,x):
            self.acc = (self.acc * 10) % 10000
        for i in range(0,y):
            self.acc = int(math.floor(self.acc / 10))
    def opcode_5(self, data):
        """ Output operation """
        self.output.append(self.mem[data])
    def opcode_6(self, data):
        """ Store operation """
        self.mem[data] = self.pad(self.acc)
    def opcode_7(self, data):
        """ Subtract Operation """
        self.acc -= self.get_memint(data)
    def opcode_8(self, data):
        """ Unconditional Jump operation """
        self.pc = data
    def opcode_9(self, data):
        """ Halt and Reset operation """
        self.reset()
    def run(self, pc=None):
        """ Runs code in memory until halt/reset opcode. """
        if pc:
            self.pc = pc
        self.running = True
        while self.running:
            self.process()
        print "Output:\n%s" % '\n'.join(self.output)
        self.init_output()

if __name__ == '__main__':
    c = Cardiac()
    c.read_deck('deck1.txt')
    try:
        c.run()
    except:
        print "IR: %s\nPC: %s\nOutput: %s\n" % (c.ir, c.pc, '\n'.join(c.output))
        raise

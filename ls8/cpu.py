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

    # RAM functions
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value
     
    def load(self):
        """Load a program into memory."""

        address = 0

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
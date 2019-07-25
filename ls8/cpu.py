"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # r5 = interrupt mask
        # r6 = interrupt status
        # r7 = stack pointer
        self.registers = [0] * 8  # r0 - r7
        self.running = False
        self.ram = [0] * 512
        self.pc = 0
        # adding pop and push
        self.pp = 7

    def ram_read(self, MAR):
        """Read the RAM. MAR = memory address register"""
        try:
            return self.ram[MAR]
        except IndexError:
            print("index out of range for RAM read")

    def ram_write(self, MDR, MAR):
        """write to the RAM. MDR = Memory Data Register"""
        try:
            self.ram[MAR] = MDR
        except IndexError:
            print("index out of range for RAM write")

    def increment_pc(self, op_code):
        add_to_pc = (op_code >> 6) + 1
        self.pc += add_to_pc

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
                    self.ram_write(val, address)

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        if op == "MUL":
            self.registers[reg_a] = bin(
                self.registers[reg_a] * self.registers[reg_b])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            op_code = self.ram_read(self.pc)  # instruction

            if op_code == 0b00000001:  # HLT (halt)
                self.running = False
                sys.exit(1)

            elif op_code == 0b10000010:  # LDI (load "immediate")
                data_a = self.ram_read(self.pc + 1)
                data_b = self.ram_read(self.pc + 2)
                self.registers[data_a] = data_b
                self.increment_pc(op_code)

            elif op_code == 0b01000111:  # PRN ()
                address_a = self.ram_read(self.pc + 1)
                print(int(self.registers[address_a], 2))
                self.increment_pc(op_code)
                pass

            elif op_code == 0b10100010:  # MUL R0,R1
                address_a = self.ram_read(self.pc + 1)
                address_b = self.ram_read(self.pc + 2)
                self.alu('MUL', address_a, address_b)

                self.increment_pc(op_code)

            else:
                 print('here is the else')
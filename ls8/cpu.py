"""CPU functionality."""

import sys
from instruction_switcher import InstructionSwitcher
from alu_switcher import ALUSwitcher
from abstract_cpu import AbstractCPU


class CPU(InstructionSwitcher):
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        InstructionSwitcher.__init__(self)
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, ):
        """Load a program into memory."""
        # Get filename from command line args
        program_filename = sys.argv[1]

        address = 0

        with open(program_filename) as f:
            # parse each line of program file, remove any comments and whitespace
            for line in f:
                line = line.split("#")[0]
                line = line.strip()
                # skip if line is empty
                if line == "":
                    continue

                # add the program line to th RAM
                value = int(line, 2)
                self.ram[address] = value
                # increment the address
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # initialize alu switch
        alu = ALUSwitcher()
        solution = alu.switch(op, self.reg[reg_a], self.reg[reg_b])
        # save the result
        self.reg[reg_a] = solution

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
        self.load()
        self.init_switcher()

        running = True

        while running:
            # Instruction Register, contains a copy of the currently executing instruction
            IR = self.ram_read(self.pc)
            # grab the first 2 digits of the instruction
            operand_count = IR >> 6
            # excute the corresponding function to the current instruction
            # self.switcher.switch(IR)
            self.switch(IR)
            # move to next instruction
            if (IR & 0b00010000) >> 4 == 0:
                # increment the pc
                self.pc += operand_count + 1

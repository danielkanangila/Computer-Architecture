import sys

from abstract_cpu import AbstractCPU
from utils.switcher import Switcher


LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000


class InstructionSwitcher(AbstractCPU, Switcher):
    def __init__(self):
        Switcher.__init__(self)

    def init_switcher(self):
        self.case(LDI, lambda IR: self.ldi())
        self.case(PRN, lambda IR: self.prn())
        self.case(ADD, lambda IR: self.alu_ir(IR))
        self.case(HLT, lambda IR: sys.exit(0))

    def ldi(self):
        register = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        # store data in the register
        self.reg[register] = value
        # increment program count
        self.pc += 3

    def prn(self):
        operand = self.ram_read(self.pc + 1)
        print(self.reg[operand])
        self.pc += 2

    def alu_ir(self, ir):
        reg_a = self.ram_read(self.pc + 2)
        reg_b = self.ram_read(self.pc + 3)
        self.alu(ir, reg_a, reg_b)
        self.pc += 3

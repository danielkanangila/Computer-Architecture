import sys

from abstract_cpu import AbstractCPU
from utils.switcher import Switcher


LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

SP = 7


class InstructionSwitcher(AbstractCPU, Switcher):
    def __init__(self):
        Switcher.__init__(self)

    def init_switcher(self):
        self.case(LDI, lambda IR: self.ldi())
        self.case(PRN, lambda IR: self.prn())
        self.case(ADD, lambda IR: self.alu_ir(IR))
        self.case(MUL, lambda IR: self.alu_ir(IR))
        self.case(PUSH, lambda IR: self.push())
        self.case(POP, lambda IR: self.pop())
        self.case(HLT, lambda IR: sys.exit(0))

    def ldi(self):
        register = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        # store data in the register
        self.reg[register] = value
        # increment program count
        # self.pc += 3

    def prn(self):
        operand = self.ram_read(self.pc + 1)
        print(self.reg[operand])
        # self.pc += 2

    def alu_ir(self, ir):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu(ir, reg_a, reg_b)
        # self.pc += 3

    def push(self):
        # Push the value to a given register
        register = self.ram_read(self.pc + 1)
        # Get value of this register in the register
        value = self.reg[register]
        # Decrement the register value at the stack pointer
        self.reg[SP] -= 1
        # copy the value from the register to the mempry at the stack pointer index
        self.ram_write(self.reg[SP], value)

    def pop(self):
        # pop the value to the top of a given register
        register = self.ram_read(self.pc + 1)
        # get the last value in the stack
        last_value = self.ram_read(self.reg[SP])
        # copy the value to the register
        self.reg[register] = last_value
        # Increment the SP
        self.reg[SP] += 1

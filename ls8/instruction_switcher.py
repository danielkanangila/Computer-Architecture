import sys

from abstract_cpu import AbstractCPU
from utils.switcher import Switcher


LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
DIV = 0b10100011
SUB = 0b10100001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7


class InstructionSwitcher(AbstractCPU, Switcher):
    def __init__(self):
        Switcher.__init__(self)

    def init_switcher(self):
        self.case(LDI, lambda IR: self.ldi())
        self.case(PRN, lambda IR: self.prn())
        self.case(ADD, lambda IR: self.alu_ir(IR))
        self.case(MUL, lambda IR: self.alu_ir(IR))
        self.case(SUB, lambda IR: self.alu_ir(IR))
        self.case(DIV, lambda IR: self.alu_ir(IR))
        self.case(CMP, lambda IR: self.alu_ir(IR))
        self.case(PUSH, lambda IR: self.push())
        self.case(POP, lambda IR: self.pop())
        self.case(CALL, lambda IR: self.call())
        self.case(RET, lambda IR: self.ret())
        self.case(JMP, lambda IR: self.jmp())
        self.case(JEQ, lambda IR: self.jeq())
        self.case(JNE, lambda IR: self.jne())
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

    def call(self):
        # decrement the stack pointer
        self.reg[SP] -= 1
        # Get the register location
        register = self.ram_read(self.pc + 1)
        # store the return address to the stack
        self.ram_write(self.reg[SP], self.pc + 2)
        # set the program counter to the value of the where the function is stored
        self.pc = self.reg[register]

    def ret(self):
        # set the program counter to the value at the top of the memory stack
        self.pc = self.ram_read(self.reg[SP])
        # pop the value to the stack
        self.reg[SP] += 1

    def jmp(self):
        # Jump to the address stored in the given register
        register = self.ram_read(self.pc + 1)
        # set the program counter to the address of the given register
        self.pc = self.reg[register]

    def jeq(self):
        # If equal flag is set (true), jump to the address stored in the given register
        if self.flag & 0b00000001 == 1:
            register = self.ram_read(self.pc + 1)
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def jne(self):
        # If E flag is clear (false, 0), jump to the address stored in the given register.
        if self.flag & 0b00000001 == 0:
            register = self.ram_read(self.pc + 1)
            self.pc = self.reg[register]
        else:
            self.pc += 2

import sys


class Switcher:
    def __init__(self):
        self.IR = dict()

    def case(self, instruction, fn):
        self.IR[instruction] = fn

    def switch(self, instruction):
        if not instruction in self.IR:
            print(f"Incorrect command: {instruction}")
            sys.exit(1)
        return self.IR.get(instruction)(instruction)

import sys


class Switcher:
    def __init__(self):
        self.IR = dict()

    def case(self, instruction, fn):
        self.IR[instruction] = fn

    def switch(self, instruction, *args, **kwargs):
        if not instruction in self.IR:
            print(instruction)
            raise Exception("Incorrect command.")
        return self.IR.get(instruction)(instruction, *args, **kwargs)

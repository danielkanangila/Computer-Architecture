from utils.switcher import Switcher
ADD = 0b10100000
MUL = 0b10100010
DIV = 0b10100011
SUB = 0b10100001


class ALUSwitcher(Switcher):
    def __init__(self):
        Switcher.__init__(self)
        self.init()

    def init(self):
        self.case(ADD, lambda ir, *args: self.add(ir, *args))
        self.case(MUL, lambda ir, *args: self.mul(ir, *args))
        self.case(DIV, lambda ir, *args: self.div(ir, *args))
        self.case(SUB, lambda ir, *args: self.sub(ir, *args))

    def add(self, ir, *args):
        return args[0] + args[1]

    def sub(self, ir, *args):
        return args[0] - args[1]

    def mul(self, ir, *args):
        return args[0] * args[1]

    def div(self, ir, *args):
        return args[0] / args[1]

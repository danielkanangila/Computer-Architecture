from abc import ABC, abstractmethod


class AbstractCPU(ABC):
    def __init__(self):
        super().__init__()
        self.ram = []
        self.reg = []
        self.pc = 0

    @abstractmethod
    def ram_read(self, MAR):
        pass

    @abstractmethod
    def ram_write(self, MAR, MDR):
        pass

    @abstractmethod
    def alu(self, op, reg_a, reg_b):
        pass

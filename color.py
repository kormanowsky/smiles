import random


class Color:
    def __init__(self, r, g, b):
        self.r = abs(int(r) % 256)
        self.g = abs(int(g) % 256)
        self.b = abs(int(b) % 256)

    def get(self):
        return self.r, self.g, self.b

    def reset(self, r, g, b):
        self.__init__(r, g, b)


class RandomColor(Color):
    def __init__(self):
        super().__init__(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def reset(self, r=0, g=0, b=0):
        self.__init__()


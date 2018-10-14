import random
from color import *


class GameSettings:
    @classmethod
    def instance(cls):
        return cls(1000, 1000, Color(0, 0, 0), 4)

    def __init__(self, width, height, background_color, level):
        self.width = int(width)
        self.height = int(height)
        self.background_color = background_color
        self.level = abs(int(level)) % 8


class SmileSettings:
    @classmethod
    def instance(cls, screen_w, screen_h, max_size=None, min_size=None):
        if not max_size:
            max_size = min(screen_h, screen_w) // 4
        else:
            max_size = int(max_size)
        if not min_size:
            min_size = 10
        else:
            min_size = int(min_size)
        size = random.randint(min_size, max_size)
        return cls(size+random.randint(0, screen_w-size*2),
                   size+random.randint(0, screen_h-size*2),
                   size, RandomColor(), RandomColor(), 1)

    def __init__(self, x, y, size, background, foreground, speed):
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.background = background
        self.foreground = foreground
        self.speed = int(speed)


class TextSettings:
    def __init__(self, text, size, color, x, y):
        self.text = str(text)
        self.size = int(size)
        self.x = int(x)
        self.y = int(y)
        self.color = color

import random
import pygame
import math
from color import *
from settings import SmileSettings

class Smile:
    @classmethod
    def instance(cls, screen, screen_w, screen_h, min_size=None, max_size=None):
        return cls(screen, screen_w, screen_h, SmileSettings.instance(screen_w, screen_h, min_size, max_size))

    def __init__(self, screen, screen_w, screen_h, settings):
        # Settings
        if not (settings and isinstance(settings, SmileSettings)):
            settings = SmileSettings.instance(screen_w, screen_h)
        self.settings = settings
        # Screen
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        # Delta values
        delta_x = random.randint(-1, 1)
        delta_y = random.randint(-1, 1)
        if not delta_x and not delta_y:
            delta_x = 1
            delta_y = -1
        self.delta_x = int(delta_x)
        self.delta_y = int(delta_y)

    def move(self):
        if self.settings.x + self.delta_x + self.settings.size > self.screen_w or \
                self.settings.x + self.delta_x - self.settings.size < 0:
            self.delta_x *= -1
        if self.settings.y + self.delta_y + self.settings.size > self.screen_h or \
                self.settings.y + self.delta_y - self.settings.size < 0:
            self.delta_y *= -1
        self.settings.x += self.delta_x*self.settings.speed
        self.settings.y += self.delta_y*self.settings.speed

    @classmethod
    def deg_to_arc(cls, deg):
        return deg / 180 * math.pi

    def draw(self):
        pygame.draw.circle(self.screen, self.settings.background.get(),
                           (self.settings.x, self.settings.y), self.settings.size, 0)
        pygame.draw.circle(self.screen, self.settings.foreground.get(),
                           (self.settings.x - self.settings.size // 3, self.settings.y - self.settings.size // 3),
                           self.settings.size * 4 // 15, 0)
        pygame.draw.circle(self.screen, self.settings.foreground.get(),
                           (self.settings.x + self.settings.size // 3, self.settings.y - self.settings.size // 3),
                           self.settings.size * 4 // 15, 0)
        pygame.draw.arc(self.screen, self.settings.foreground.get(),
        (self.settings.x - self.settings.size * 2 // 3,
         self.settings.y - self.settings.size // 3, self.settings.size * 215 // 150, self.settings.size),
        Smile.deg_to_arc(180), Smile.deg_to_arc(360), self.settings.size // 3)
        self.move()

    def set_speed(self, speed):
        self.settings.speed = int(speed)
        return self

    def is_under_mouse(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        return ((x - self.settings.x) ** 2 + (y - self.settings.y) ** 2) ** 0.5 <= self.settings.size

    def get_score(self):
        return (max(self.screen_h, self.screen_w) // self.settings.size + self.settings.speed) * 10

    def get_square(self):
        return math.pi * self.settings.size ** 2

    def collides_with(self, other):
        dst = ((self.settings.x-other.settings.x)**2+(self.settings.y-other.settings.y)**2)**0.5
        sum = self.settings.size + other.settings.size
        if dst < sum:
            return 2
        elif dst == sum:
            return 1
        return 0
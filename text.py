import pygame


class Text:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

    def draw(self):
        font = pygame.font.Font("courier_new.ttf", self.settings.size)
        text = font.render(self.settings.text, True, self.settings.color.get())
        self.screen.blit(text, (self.settings.x, self.settings.y))

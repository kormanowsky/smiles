import pygame
from smile import Smile
from settings import GameSettings, TextSettings
from text import Text
from color import Color

class Game:
    @classmethod
    def instance(cls):
        return cls()

    def __init__(self, settings=None):
        if not settings or not isinstance(settings, GameSettings):
            settings = GameSettings.instance()
        self.settings = settings
        self.smile_speed = 1
        self.score = 0
        self.frames = 0
        self.smiles = []
        self.screen = None

    def draw_frame(self):
        # Draw each smile
        for smile in self.smiles:
            smile.draw()

        # Double buffering and refilling the screen
        pygame.display.flip()
        self.screen.fill(self.settings.background_color.get())

    def draw_final_frame(self):
        # TODO: Fix this and add some score info
        Text(self.screen, TextSettings("Game over!", 100, Color(255, 255, 255),
                                       self.settings.width // 2, self.settings.height // 2)).draw()
        pygame.display.flip()
        self.screen.fill(self.settings.background_color.get())
        pygame.display.flip()
        pygame.time.wait(5000)

    def start(self):
        # Init pygame library and the screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.screen.fill(self.settings.background_color.get())
        self.smiles.append(Smile.instance(self.screen, self.settings.width, self.settings.height))
        # The main game loop
        while not self.is_over():
            # Compute frames count and add smile if necessary
            self.frames += 1
            if self.frames % (90 - self.settings.level*10) is 0:
                self.smiles.append(Smile.instance(self.screen, self.settings.width, self.settings.height))
            if self.frames % 10000*(90 - self.settings.level*10) is 0:
                for smile in self.smiles:
                    smile.set_speed(smile.settings.speed + 1)
            # Interactions
            for event in pygame.event.get():
                # The end of the game
                if event.type is pygame.QUIT:
                    return
                # The click on the smile
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    # If a smile was clicked, remove it and add some points to the score
                    for smile in list(reversed(self.smiles)):
                        if smile.is_under_mouse():
                            self.score += smile.get_score()
                            print("SCORE_CHANGED", self.score)
                            self.smiles.remove(smile)
                            break
            # Draw the frame
            self.draw_frame()
        self.draw_final_frame()

    def is_over(self):
        square = 0.0
        for smile in self.smiles:
            square += smile.get_square()
        return square >= self.settings.width * self.settings.height

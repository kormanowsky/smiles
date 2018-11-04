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
        self.process_collisions()
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
        # The main game loop
        while not self.is_over():
            # Compute frames count and add smile if necessary
            self.frames += 1
            if self.frames % (90 - self.settings.level*10) is 0:
                new_smile = Smile.instance(self.screen, self.settings.width, self.settings.height)
                collides = False
                for smile in self.smiles:
                    if smile.collides_with(new_smile):
                        collides = True
                if not collides:
                    self.smiles.append(new_smile)
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
        return square >= 0.75 * self.settings.width * self.settings.height

    def process_collisions(self):
        for i in range(len(self.smiles)):
            for j in range(len(self.smiles)):
                if j <= i:
                    continue
                collision = self.smiles[i].collides_with(self.smiles[j])
                if collision is 1:
                    center_1 = (self.smiles[i].settings.x, self.smiles[i].settings.y)
                    center_2 = (self.smiles[j].settings.x, self.smiles[j].settings.y)
                    deltas_1 = (self.smiles[i].delta_x, self.smiles[i].delta_y)
                    deltas_2 = (self.smiles[j].delta_x, self.smiles[j].delta_y)
                    m = (center_1[0] + center_2[0]) / 2, (center_1[1] + center_2[1]) / 2
                    centers = [center_1, center_2]
                    deltas = [deltas_1, deltas_2]
                    idxs = [i, j]
                    for t in range(2):
                        delta = deltas[t]
                        center = centers[t]
                        v1 = delta
                        v2 = m[0] - center[0], m[1] - center[1]
                        cos_a = (v1[0] * v2[0] + v1[1] * v2[1]) / (v1[0] ** 2 + v1[1] ** 2) ** 0.5 / (
                                v2[0] ** 2 + v2[1] ** 2) ** 0.5
                        if not cos_a:
                            return
                        cm_m = (v2[0] ** 2 + v2[1] ** 2) ** 0.5
                        cm_dm = (v1[0] ** 2 + v1[1] ** 2) ** 0.5
                        cm_n = cm_m / cos_a
                        diff = cm_n / cm_dm
                        n = center[0] + delta[0] * diff, center[1] + delta[1] * diff
                        k = m[0] + 2 * (n[0] - m[0]), m[1] + 2 * (n[1] - m[1])
                        cn = -1 * v2[0] + k[0], -1 * v2[1] + k[1]
                        self.smiles[idxs[t]].delta_x = round((cn[0] - n[0]) / diff)
                        self.smiles[idxs[t]].delta_y = round((cn[1] - n[1]) / diff)
                elif collision is 2:
                    deltas_1 = (self.smiles[i].delta_x, self.smiles[i].delta_y)
                    deltas_2 = (self.smiles[j].delta_x, self.smiles[j].delta_y)
                    deltas_1, deltas_2 = deltas_2, deltas_1
                    self.smiles[i].delta_x = deltas_1[0]
                    self.smiles[i].delta_y = deltas_1[1]
                    self.smiles[j].delta_x = deltas_2[0]
                    self.smiles[j].delta_y = deltas_2[1]
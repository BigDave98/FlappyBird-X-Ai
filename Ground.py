import pygame
import os


GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))

class Ground:
    SPEED = 5
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH

    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        if self.x0 + self.WIDTH < 0:
            self.x0 += self.WIDTH
        if self.x1 + self.WIDTH < 0:
            self.x1 += self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMG, (self.x0, self.y))
        screen.blit(self.IMG, (self.x1, self.y))
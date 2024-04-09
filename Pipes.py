import pygame
import os
import random

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))

class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.top_pos = 0
        self.ground_pos = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_GROUND = PIPE_IMG
        self.survived = False
        self.def_height()

    def def_height(self):
        self.height = random.randrange(50,450)
        self.top_pos = self.height - self.PIPE_TOP.get_height()### self.ground_pos
        self.ground_pos = self.height + self.DISTANCE ###

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top_pos))
        screen.blit(self.PIPE_GROUND, (self.x, self.ground_pos))

    def collide(self, bird):
        bird_mask= bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        ground_mask = pygame.mask.from_surface(self.PIPE_GROUND)

        distance_top = (self.x - bird.x, self.top_pos - round(bird.y))
        distance_ground = (self.x - bird.x, self.ground_pos - round(bird.y))

        top_crash = bird_mask.overlap(top_mask, distance_top)
        base_crash = bird_mask.overlap(ground_mask, distance_ground)

        if top_crash or base_crash:
            return True
        else:
            False
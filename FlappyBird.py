import pygame
import os
import random
import neat

ai_playing = True
generation = 0

# Set the widrh and height of the game screen:
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Assign images to their constants:
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# Set the score board font:
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)

# Create the game Objects:
class Bird:
    IMGS = BIRD_IMGS

    # Bird rotation animations:
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    # Bird attributes:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # Calculate the bird falling movement:
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        # Restrict the movement:
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # Bird Angle:
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle >-90:
                self.angle = self.ROTATION_SPEED

    def draw(self, screen):
        # Specify the bird image to use:
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count >= self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If the bird is falling, do not flap wings:
        if self.angle <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Draw Image:
        rotated_img = pygame.transform.rotate(self.img, self.angle)
        pos_img_center = self.img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_img.get_rect(center=pos_img_center)
        screen.blit(rotated_img, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

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


def draw_game(screen, birds, pipes, ground, score):
    screen.blit(BACKGROUND_IMG, (0,0))

    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    text = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    if ai_playing:
        text = SCORE_FONT.render(f"Generation: {generation}", 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    ground.draw(screen)
    pygame.display.update()

def main(genomes, config): #Fitness function
    global generation
    generation += 1

    if ai_playing:
        nets = []
        genomes_list = []
        birds = []
        for _, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0
            genomes_list.append(genome)
            birds.append(Bird(230, 350))

    else:
        birds = [Bird(230, 350)]

    ground = Ground(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    time = pygame.time.Clock()

    game = True
    while game:
        time.tick(30)

        #User interactions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
            if not ai_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 0 and birds[0].x > (pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                pipe_index = 1

        else:
            game = False
            break

        #Move objects
        for i, bird in enumerate(birds):
            bird.move()
            #Increas Fitness:
            genomes_list[i].fitness += 0.1
            output = nets[i].activate((bird.y,
                                       abs(bird.y - pipes[pipe_index].height),
                                       pipes[pipe_index].ground_pos)) # -1 and 1 -> if output > 0.5 bird jumps

            if output[0] > 0.6:
                bird.jump()
        ground.move()

        add_pipe = False
        remove_pipes = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                    if ai_playing:
                        genomes_list[i].fitness -= 1
                        genomes_list.pop(i)
                        nets.pop(i)

                if not pipe.survived and bird.x > pipe.x:
                    pipe.survived = True
                    add_pipe = True
            pipe.move()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            for genome in genomes_list:
                genome.fitness += 5

        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.img.get_height()) > ground.y or bird.y < 0:
                birds.pop(i)
                if ai_playing:
                    genomes_list.pop(i)
                    nets.pop(i)

        draw_game(screen, birds, pipes, ground, score)

def run(path_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                path_config)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if ai_playing:
        population.run(main)
    else:
        main(None, None)

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    path_config = os.path.join(path, 'config.txt')
    run(path_config)







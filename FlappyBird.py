import pygame
import os
import random
import neat
from Bird import Bird
from Pipes import Pipe
from Ground import Ground

ai_playing = True #If you want to play this variable have to be False
generation = 0

# Set the widrh and height of the game screen:
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Assign images to their constants:
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))


# Set the score board font:
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('arial', 50)

# Create the game Objects:

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







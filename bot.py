from bird import Bird
import pygame
import time
import neat
import os
import random
pygame.font.init()

GEN = 0

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMGS = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))

STATE_FONT = pygame.font.SysFont("comicsans", 50)


class Pipe:
    # Space between pipe
    GAP = 200
    # Speed of the pipe moving backwards
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        # Keep track of where the top and bottom pipe will be drawn
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMGS, False, True)
        self.PIPE_BOTTOM = PIPE_IMGS
        #  Check if this current pipe has pass the bird
        self.passed = False
        self.set_height()

    # Used to define how tall both pipes are
    def set_height(self):
        # PIP_TOP's height is 640
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        # print(self.top, self.bottom)

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # Offset between the top pipe's mask and the birds masks
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Find their point of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # if any part of the bird mask overlaps with either the top pipe mask or bottom pipe mask, end the game with the boolean true
        if b_point or t_point:
            return True

        return False


class Base:
    # Same speed as pipes
    VEL = 5
    # Get the actual width of this image
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, generation):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    for bird in birds:
        bird.draw(win)
    text = STATE_FONT.render("Score: " + str(score), 1,
                             (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STATE_FONT.render("Gen: " + str(generation), 1,
                             (255, 255, 255))
    win.blit(text, (10, 10))
    text = STATE_FONT.render("Birds: " + str(len(birds)), 1,
                             (255, 255, 255))
    win.blit(text, (200, 10))

    base.draw(win)
    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    neural_networks = []
    ind_genome = []
    birds = []

    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_networks.append(network)
        genome.fitness = 0  # Initial fitness to 0
        ind_genome.append(genome)
        birds.append(Bird(230, 350))

    # So that it is at the bottom of our screen cause our height is 800
    base = Base(730)
    pipes = [Pipe(600)]
    # Clock.tick controls the number of ticks for each while loop
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    score = 0
    while run:
        clock.tick(30)
        add_pipe = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_BOTTOM.get_width():
                pipe_index = 1
        else:
            # if no bird left quit the game
            run = False
            break
        # Checking the out put value
        for index, bird in enumerate(birds):
            bird.move()
            ind_genome[index].fitness += 0.1
            # Passing in the 3 arguements defined in config-feedforward for our input layer
            output = neural_networks[index].activate((bird.y, abs(
                bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()

        for pipe in pipes:
            pipe.move()
            for index, bird in enumerate(birds):
                # Check if each bird has collided
                # If the bird has collided ajust its fitness value
                # -1 from the activation function
                if pipe.collide(bird, win):
                    ind_genome[index].fitness -= 1
                    birds.pop(index)
                    neural_networks.pop(index)
                    ind_genome.pop(index)

            # pipes.append(Pipe(700))
            # if pipe.x =7 300:
            #     pipes.append(Pipe(700))
            #  Bird has not passed the pipe boolean, and actual position of pipe is behind the x position of the bird
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.PIPE_BOTTOM.get_width() < 0:
                print("Removing pipe")
                pipes.pop(0)
        # Added score and pipes
        if add_pipe:
            score += 1
            for genome in ind_genome:
                genome.fitness += 5
            pipes.append(Pipe(600))

        for index, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(index)
                neural_networks.pop(index)
                ind_genome.pop(index)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(file):
    # Load config file
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        file)
    # Set up pop
    population = neat.Population(config)

    # give us some print() in console
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Running 50 gens (Calling the main function 50 times)
    winner = population.run(main, 50)


# time.sleep(4)
# Give us our current dir
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

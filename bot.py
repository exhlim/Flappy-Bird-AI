import pygame
import time
import neat
import os
import random
from bird import Bird
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
        # 300
        # 340
        # 300+200
        # 840
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        print(self.top, self.bottom)

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


def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    bird.draw(win)
    pygame.display.update()


def main():
    # Initializing the starting position of the bird
    bird = Bird(230, 350)
    # So that it is at the bottom of our screen cause our height is 800
    base = Base(730)
    pipes = [Pipe(700)]
    # Clock.tick controls the number of ticks for each while loop
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        base.move()
        for pipe in pipes:
            pipe.move()
        draw_window(win, bird, pipes, base)
    pygame.quit()
    quit()


main()

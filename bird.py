import pygame
import time
import neat
import os
import random

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]


class Bird():
    IMGS = BIRD_IMGS
    # How much do you want the bird to tilt when the bird is tilting up or down
    MAX_ROTATION = 25
    # What is the speed at which you want the bird to tilt whe bird is facing up or facing down
    ROT_VEL = 20
    # The speed of the flapping of the bird
    ANIMATION_TIME = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # how much the image is actualyl tilted so we will know how to draw it on the screen
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        # Which index of the image array you are at so you can keep track of which image is currently being displayed
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        # 0 coordinates start at the top left for pygame so you need a negative velocity to move up
        self.vel = -10.5
        # Keep track of when we last jumped
        self.tick_count = 0
        # Keep track of where the bird is jumping from
        self.height = self.y

    def move(self):
        # One tick happen, a frame happened
        self.tick_count += 1
        # how many pixels we move up and down during this frame
        # base on our current birds vel how much we moving up or down
        # tick_count refers to the time
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        # So that if we moving down we dont go down any faster. we cap the speed down at 16
        if d >= 16:
            d = 16
        # When we are moving upwards our d will always be negative so we set the displacement upwards to be -2
        if d < 0:
            d -= 2
        self.y = self.y + d
        # If the bird is higher than its previouse position where it jumped from then we keep the direction of where the bird is facing to be still upwards
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
# Win is the window that we are drawing the bird onto

    def draw(self, win):
        self.img_count += 1
        # print(self.img_count)
        # This entire if and elif refers to which image do we want to base on the img_count that we are at right now
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            # Puts the wings back to level
            self.img_count = self.ANIMATION_TIME*2
        # This entire 3-4 lines below will rotate the image for us. Rotating the image from the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    # handle collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

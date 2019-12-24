import pygame
from os import path
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (150, 100, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)

counter = 0  # used as a general cycler in the while loop to trigger events such as mob spawn rate etc.
score = 0
flipper = -1  # used to flip positive and negative values
pct = 100  # used to create green life bar amount
fill = 200  # used for max amount of health

img = path.dirname(__file__)
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Ugly command that 'turns on' sprite
        self.image = pygame.image.load(path.join(img_dir, "eyelander2.png")).convert()
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.image.set_colorkey(WHITE)

        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        self.gravity = -5
        self.drift = 0
        self.acceleration = 0
        self.shield = 100
        self.fuel = 100
        pct = self.shield

    def update(self):
        self.speedx = self.drift
        self.fuel = self.fuel + .5
        if self.fuel < 0:
            self.fuel = 0
        if self.fuel > 100:
            self.fuel = 100
        self.acceleration = self.acceleration + .25
        self.gravity = self.gravity + .3
        self.speedy = self.gravity + self.acceleration
        self.image = pygame.image.load(path.join('img', "eyelander2.png")).convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        if self.drift > 0:
            self.drift = self.drift - .101
        else:
            self.drift = self.drift + .1
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.fuel > 5:
            self.drift = self.drift - .5
            self.fuel = self.fuel - 2

        if keystate[pygame.K_RIGHT] and self.fuel > 5:
            self.drift = self.drift + .5
            self.fuel = self.fuel - 2
        if keystate[pygame.K_UP] and self.fuel > 5:
            self.acceleration = self.acceleration - .5
            self.fuel = self.fuel - 4
            self.image = pygame.image.load(path.join('img', "eyelander.png")).convert()

            self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect.x += self.speedx + self.drift
        self.rect.y += self.speedy + self.gravity + self.acceleration

        if self.rect.left > WIDTH:
            self.rect.left = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

        if self.rect.bottom > 600:
            self.rect.y = self.rect.y - 20
            self.acceleration = -self.acceleration
        if self.gravity > 0:
            self.gravity = self.gravity - .6

        if self.rect.bottom < HEIGHT / 2:
            self.acceleration = self.acceleration + .05
        if self.rect.bottom < HEIGHT / 3:
            self.acceleration = self.acceleration + .05
        if self.rect.bottom < HEIGHT / 4:
            self.acceleration = self.acceleration + .05

        if self.acceleration > 0:
            self.acceleration = self.acceleration - .15
        else:
            self.acceleration = self.acceleration + .05
        if self.acceleration > 7:
            self.acceleration = 7
        if self.acceleration < -7:
            self.acceleration = -7

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

counter = 0  # used as a general cycler in the while loop to trigger events such as mob spawn rate etc.
score = 0
flipper = -1  # used to flip positive and negative values
pct = 100  # used to create green life bar amount
fill = 200  # used for max amount of health


class Mob(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.size_maker = random.randrange(50, 60)
        self.image = pygame.image.load(path.join("img", "enemy00.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.size_maker, self.size_maker))

        self.image = pygame.image.load(path.join('img', "enemy01.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.size_maker, self.size_maker))

        self.image = pygame.image.load(path.join('img', "enemy02.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.size_maker, self.size_maker))

        self.image = pygame.image.load(path.join('img', "enemy03.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.size_maker, self.size_maker))

        self.rect = self.image.get_rect()
        self.radius = 50  # returns the size to self.rect for ref.
        self.image_copy = self.image
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = -50
        self.speedx = random.randrange(-5, 5)
        self.speedy = random.randrange(1, 3)
        self.costumecounter = 0
        self.flipper = -1

    def update(self):
        self.rect.x += self.speedx * self.flipper
        self.rect.y += self.speedy
        self.costumecounter = random.randrange(1, 4)
        self.randomflipper = random.randrange(1, 101)
        if self.randomflipper > 98:
            self.flipper = -self.flipper

        if self.costumecounter == 1:
            self.image = pygame.image.load(path.join("img", "enemy00.png")).convert()
            self.image.set_colorkey(BLACK)
        elif self.costumecounter == 2:
            self.image = pygame.image.load(path.join("img", "enemy01.png")).convert()
            self.image.set_colorkey(BLACK)
        elif self.costumecounter == 3:
            self.image = pygame.image.load(path.join("img", "enemy02.png")).convert()
            self.image.set_colorkey(BLACK)
        else:
            self.image = pygame.image.load(path.join("img", "enemy03.png")).convert()
            self.image.set_colorkey(BLACK)

        if self.rect.y > HEIGHT:
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join('img', "heart.png")).convert()
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.heartsize = random.randrange(30, 50)
        self.image = pygame.transform.scale(self.image, (self.heartsize, self.heartsize))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = HEIGHT
        self.speedy = random.randrange(-4, -1)
        self.platformxloc = self.rect.x

    def update(self):
        self.platformxloc = self.rect.x
        self.rect.y += self.speedy * (self.heartsize * .01)
        if self.rect.y < 0:
            self.kill()


class Stars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.starsize = random.randrange(1, 4)
        self.image = pygame.Surface((self.starsize, self.starsize))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = self.starsize / 1.3

    def update(self):
        self.rect.y += self.starsize
        if self.rect.y >= HEIGHT:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Ugly command that 'turns on' sprite
        self.image = pygame.image.load(path.join('img', "starfieldIII.png")).convert()
        self.image = pygame.transform.scale(self.image, (801, 607))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.

        self.rect.centerx = WIDTH / 2
        self.rect.centery = -300

    def update(self):
        self.rect.y = self.rect.y + 1
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


class BackgroundII(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Ugly command that 'turns on' sprite
        self.image = pygame.image.load(path.join('img', "starfield.png")).convert()

        self.image.set_colorkey(WHITE)

        self.image = pygame.transform.scale(self.image, (801, 607))
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.rect.centerx = WIDTH / 2
        self.rect.centery = 300

    def update(self):
        self.rect.y = self.rect.y + 1
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0

import pygame
import random
from os import path
from player import *
from game_objects import *

# screen width height and frame rate
WIDTH = 800
HEIGHT = 600
FPS = 30

# creates path name so this code will run on any computer
mandala_folder = path.dirname(__file__)

# prepares and sets fonts for screen writing
pygame.font.init()
combo_count = 0
game_font = pygame.font.SysFont('Tahoma', 20)
score_font = pygame.font.SysFont('Tahoma', 40)
health_surface = game_font.render('HEALTH', False, (255, 255, 255))
fuel_surface = game_font.render('FUEL', False, (255, 255, 255))
bullet_surface = game_font.render('WEAPONS', False, (255, 255, 255))
combo_surface = game_font.render('{}'.format(combo_count), False, (255, 255, 255))
bullet_pct = 100

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


def draw_combo_count(combo_count):
    combo_count = combo_count + 1
    print(combo_count)
    combo_surface = score_font.render('SCORE: 000{}'.format(score), False, (255, 255, 255))
    return combo_count


def draw_shield_bar(screen, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 120
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if BAR_LENGTH > 120:
        fill = 120
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)


def draw_fuel_bar(screen, x, y, pct):
    BAR_LENGTH = 4
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_HEIGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, -BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, BAR_LENGTH, -fill)
    if BAR_HEIGHT > 40:
        fill = 40
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 1)


def draw_big_fuel_bar(screen, x, y, fuel_pct):
    BAR_LENGTH = 120
    BAR_HEIGHT = 15
    fill = (fuel_pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if BAR_LENGTH > 120:
        BAR_LENGTH = 120
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)


def draw_bullet_bar(screen, x, y, bullet_pct):
    BAR_LENGTH = 120
    BAR_HEIGHT = 15
    fill = (bullet_pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if BAR_LENGTH > 120:
        fill = 120
    pygame.draw.rect(screen, LIGHT_BLUE, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)
    if fill < 20:
        pygame.draw.rect(screen, RED, outline_rect, 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.rect.center = player.rect.center
        self.speedbulletx = 15
        self.speedbullety = -15
        self.bulletamt = 100


class BulletR(Bullet):
    def __init__(self):
        Bullet.__init__(self)

    def update(self):
        self.rect.x += self.speedbulletx
        self.bulletamt = self.bulletamt - 1
        if self.rect.x <= 0:
            self.kill()


class BulletL(Bullet):
    def __init__(self):
        Bullet.__init__(self)

    def update(self):
        self.bulletamt = self.bulletamt - 1
        self.rect.x -= self.speedbulletx
        if self.rect.x >= WIDTH:
            self.kill()


class TopBullet(pygame.sprite.Sprite):
    def __init__(self):
        Bullet.__init__(self)

    def update(self):
        self.rect.y += self.speedbullety
        if self.rect.y <= 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join('img', "explosion.png")).convert()
        self.rect = self.image.get_rect()  # returns the size to self.rect for ref.
        self.image = pygame.transform.scale(self.image, (256, 96))
        self.image.set_colorkey(BLACK)
        self.rect.center = player.rect.center
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.sheetmultiplier = 32



    def update(self):
        if hits == True:
            for expl in range (0,8):
                self.rect.x = player.rect.x + (self.sheetmultiplier*expl)
                self.rect.y = player.rect.y
        else:
            self.rect.x = 100
            self.rect.y = 100

        if self.rect.y < 0:
            self.kill()

# initialize pygame and create window
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce Around")
clock = pygame.time.Clock()

player_img = pygame.image.load(path.join(img_dir, "eyelander.png")).convert
player_img = pygame.image.load(path.join(img_dir, "eyelander2.png")).convert

mobcostumes = []

jump_snd = pygame.mixer.Sound(path.join(snd_dir, "synth_laser_01.ogg"))
newalien_snd = pygame.mixer.Sound(path.join(snd_dir, "synth_laser_04.ogg"))
shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "synth_laser_01.ogg"))
plathit_snd = pygame.mixer.Sound(path.join(snd_dir, "bad_bounce.ogg"))
sad_snd = pygame.mixer.Sound(path.join(snd_dir, "synth_misc_09.ogg"))
death_snd = pygame.mixer.Sound(path.join(snd_dir, "wave.wav"))
bad_bounce = pygame.mixer.Sound(path.join(snd_dir, "bad_bounce.ogg"))

pygame.mixer.music.load(path.join(snd_dir, "Story.ogg"))

pygame.mixer.music.set_volume(.09)
pygame.mixer.Sound.set_volume(jump_snd, .09)
pygame.mixer.Sound.set_volume(newalien_snd, .09)
pygame.mixer.Sound.set_volume(plathit_snd, .09)
pygame.mixer.Sound.set_volume(shoot_snd, .09)
pygame.mixer.Sound.set_volume(sad_snd, .09)
pygame.mixer.Sound.set_volume(bad_bounce, .09)

all_sprites = pygame.sprite.Group()  # preps container for all objs and names it all_sprites
mob_sprites = pygame.sprite.Group()  # preps container for all objs and names it all_sprites
star_sprites = pygame.sprite.Group()  # preps container for all objs and names it all_sprites
platform_sprites = pygame.sprite.Group()  # preps container for all objs and names it all_sprites
bullet_sprites = pygame.sprite.Group()  # preps container for all objs and names it all_sprites4
background_sprites = pygame.sprite.Group()
player = Player()  # creates player sprite named "player"
mob001 = Mob()
bullet = TopBullet()
stars = Stars()
heart = Heart()
sidebullet = BulletR()
sidebullet = BulletL()
background = Background()
backgroundII = BackgroundII()
#explosion = Explosion()

all_sprites.add(background)
all_sprites.add(backgroundII)
all_sprites.add(stars)  # adds player to all_sprites container.
all_sprites.add(heart)  # adds player to all_sprites container.
platform_sprites.add(heart)
star_sprites.add(stars)
mob_sprites.add(mob001)
bullet_sprites.add(bullet)
bullet_sprites.add(sidebullet)
all_sprites.add(player)
#all_sprites.add(explosion)
# Game loop
sfx_control = .09
music_control = .09
running = True
unpaused = 1
pygame.mixer.music.play(loops=-1)

while running:
    playerx = player.rect.x
    playery = player.rect.y
    combo_surface = game_font.render('{}'.format(combo_count), False, (255, 255, 255))
    newalienroll = random.randrange(1, 100)
    counter = counter + 1
    clock.tick(FPS)
    background_sprites.update()

    if player.rect.bottom > HEIGHT - 10:
        combo_count = 0
        bad_bounce.play()
        score = score - 500
    if score < 0:
        score = 0

    if unpaused == -1:
        pygame.mixer.music.set_volume(0)
        pausefont = pygame.font.SysFont('Arial', 80)
        textsurfaceii = pausefont.render('PAUSE?', False, (155, 155, 255))
        screen.blit(textsurfaceii, (WIDTH / 2, HEIGHT / 2))
        pygame.display.flip()

    bullet_pct = bullet_pct + .1
    if bullet_pct > 100:
        bullet_pct = 100
    if bullet_pct < 0:
        bullet_pct = 0
    # Process input (events)
    if counter % 1 == 0:
        stars = Stars()
        all_sprites.add(stars)
    if player.rect.top < 0:
        player.rect.top = 0
    if newalienroll >= 98:
        mob001 = Mob()
        newguy = newalien_snd.play()
        mob_sprites.add(mob001)
        all_sprites.add(mob001)
    if counter % 10 == 0:
        heart = Heart()
        platform_sprites.add(heart)
        all_sprites.add(heart)
    if counter > 360:
        counter = 0
    if counter % 20 == 0:
        flipper = -flipper

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_c] and bullet_pct > 10:
            bullet_pct = bullet_pct - 5
            jump_snd.play()
            bullet = TopBullet()
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)
        if keystate[pygame.K_SPACE] and bullet_pct > 10:
            bullet_pct = bullet_pct - 10
            shootsound = jump_snd.play()
            bullet = BulletR()
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)
            bullet = BulletL()
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)
        if keystate[pygame.K_p]:
            unpaused = unpaused * -1

    # Update

    hits = pygame.sprite.spritecollide(player, mob_sprites, True)
    heart_hits = pygame.sprite.spritecollide(player, platform_sprites, True)
    bullethits = pygame.sprite.groupcollide(bullet_sprites, mob_sprites, True, True)
    powerups = pygame.sprite.groupcollide(bullet_sprites, platform_sprites, True, True)

    if bullethits:
        shoot_snd.play()
        score = int(score + 10 * combo_count)
    if hits:
        player.shield = player.shield - random.randrange(15, 25)
        jump_snd.play()
        sad_snd.play()
        player.acceleration = -player.acceleration - 5
        if player.shield < 0:
            time_up_start = pygame.time.get_ticks()
            time_up_stop = time_up_start + 5000
            while time_up_stop > time_up_start:
                death_snd.play()
                time_up_start = pygame.time.get_ticks()
                game_font = pygame.font.SysFont('Arial', 40)
                text_surface = game_font.render('GOOD GAME', False, (255, 255, 255))
                screen.blit(text_surface, (WIDTH / 2 - 100, HEIGHT / 2))
                score_surface = game_font.render(('YOUR FINAL SCORE: {}'.format(score)), False, (255, 255, 255))
                screen.blit(score_surface, (WIDTH / 2 - 190, HEIGHT / 2 + 50))
                pygame.display.flip()
                player.shield = 0
            running = False
    if heart_hits:
        if player.rect.y <= heart.rect.y:
            player.acceleration = -player.acceleration - 2
        combo_start_display = pygame.time.get_ticks()
        player.fuel = player.fuel + (2 * combo_count)
        combo_count = combo_count + 1
        if player.shield < 95:
            player.shield = player.shield + 2
        score = score + random.randrange(2, 4) * combo_count
        plathit_snd.play()

    if powerups:
        score = score + 5

    # Draw / render
    if len(str(score)) == 1:
        text_surface = score_font.render('SCORE: 000{}'.format(score), False, (255, 255, 255))
    elif len(str(score)) == 2:
        text_surface = score_font.render('SCORE: 00{}'.format(score), False, (255, 255, 255))
    elif len(str(score)) == 3:
        text_surface = score_font.render('SCORE: 0{}'.format(score), False, (255, 255, 255))
    else:
        text_surface = score_font.render('SCORE: {}'.format(score), False, (255, 255, 255))

    all_sprites.draw(screen)
    screen.blit(text_surface, (WIDTH / 2 - 140, 0))
    screen.blit(health_surface, (5, 0))
    screen.blit(fuel_surface, (5, 45))
    screen.blit(bullet_surface, (WIDTH - 125, 0))
    screen.blit(combo_surface, (player.rect.x + 10, player.rect.y - 25))
    all_sprites.update()
    draw_shield_bar(screen, 5, 5, player.shield)
    fuelx = player.rect.x
    fuely = player.rect.y
    draw_fuel_bar(screen, fuelx - 6, fuely + 15, player.fuel)
    draw_big_fuel_bar(screen, 5, 70, player.fuel)
    draw_bullet_bar(screen, WIDTH - 125, 25, bullet_pct)
    pygame.display.flip()
    screen.fill(BLACK)

pygame.quit()
# resize background
# randomize heart size
# rename everything
# cancel "upbounce"
# create levels

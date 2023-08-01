import pygame
import os
import random

PATH = os.getcwd()

pygame.init()
pygame.mixer.init()

# SOUND EFFECT
pygame.mixer.music.load(os.path.join(PATH,'background-music.mp3'))
pygame.mixer.music.play(-1)

explosion = pygame.mixer.Sound(os.path.join(PATH,'explosion.wav'))
laser = pygame.mixer.Sound(os.path.join(PATH,'laser.wav'))
powerup = pygame.mixer.Sound(os.path.join(PATH,'powerup.wav'))
gameover = pygame.mixer.Sound(os.path.join(PATH,'gameover.wav'))
sound_state = True

FPS = 60    
WIDTH = 800
HEIGHT = 700

clock = pygame.time.Clock()

# color RGB
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SCORE = 0
LIVES = 3
LIVES_TIME = pygame.time.get_ticks()
GAMEOVER = False
GAMEOVER_FONT = pygame.time.get_ticks()
GAMEOVER_TIME = pygame.time.get_ticks()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

# game name
pygame.display.set_caption('Spaceship shooting')

# background
bg = os.path.join(PATH,'background.png')
background = pygame.image.load(bg).convert_alpha()
background_rect = background.get_rect() 

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = os.path.join(PATH,'Enemy.png')
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        rand_x = random.randint(self.rect.width/2 , WIDTH - self.rect.width)
        self.rect.center = (rand_x , WIDTH - self.rect.height)
        self.speed_y = random.randint(1,10)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.y = 0
            rand_x = random.randint(self.rect.width/2 , WIDTH - self.rect.width)
            self.rect.x = rand_x
            self.speed_y = random.randint(1,5)

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        img = os.path.join(PATH,'spaceship.png')
        self.image = pygame.image.load(img).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT - self.rect.height)

        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0

        keystate = pygame.key.get_pressed()
        if GAMEOVER != True:  
            if keystate[pygame.K_LEFT] and self.rect.x > 0:
                self.speed_x = -7
            if keystate[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
                self.speed_x = 7
            if keystate[pygame.K_UP] and self.rect.y > 0:
                self.speed_y = -7
            if keystate[pygame.K_DOWN] and self.rect.y < WIDTH - self.rect.height:
                self.speed_y = 7

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            self.rect.y = 0
        if self.rect.top > HEIGHT:
            self.rect.x = 0

    def shoot(self):
        if GAMEOVER != True:
            pygame.mixer.Sound.play(laser)
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            group_bullet.add(bullet)

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.kill()

class Medicpack(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = os.path.join(PATH,'medicpack.png')
        self.last = pygame.time.get_ticks() 
        self.wait = 20000 # milliseconds / 20seconds
        self.run = False

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        rand_x = random.randint(self.rect.width/2 , WIDTH - self.rect.width)
        self.rect.center = (rand_x , -100)
        self.speed_y = random.randint(1,10)

    def update(self):
        now = pygame.time.get_ticks()

        if self.run == True:
            self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            self.run = False
            self.rect.y = -100
            
        if (now - self.last) >= self.wait:
            self.run = True
            self.last = now
            rand_x = random.randint(self.rect.width/2 , WIDTH - self.rect.width)
            self.rect.x = rand_x
            self.speed_y = random.randint(1,10)

font_name = pygame.font.match_font('arial')
def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

all_sprites = pygame.sprite.Group()
group_enemy = pygame.sprite.Group()
group_bullet = pygame.sprite.Group()
group_medicpack = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    group_enemy.add(enemy)

medicpack = Medicpack()
all_sprites.add(medicpack)
group_medicpack.add(medicpack)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    collide_enermy = pygame.sprite.spritecollide(player, group_enemy, True)
    print(collide_enermy)

    if collide_enermy:
        pygame.mixer.Sound.play(explosion)
        enemy = Enemy()
        all_sprites.add(enemy)
        group_enemy.add(enemy)

        now_lives = pygame.time.get_ticks()
        if now_lives - LIVES_TIME >= 2000:
            LIVES -= 1 # LIVES = LIVES - 1
            LIVES_TIME = now_lives

        if LIVES == 0:
            GAMEOVER = True

    collide_medic = pygame.sprite.spritecollide(player, group_medicpack, True)

    if collide_medic:
        pygame.mixer.Sound.play(powerup)
        LIVES += 1
        medicpack = Medicpack()
        all_sprites.add(medicpack)
        group_medicpack.add(medicpack)

    hits = pygame.sprite.groupcollide(group_bullet, group_enemy, True, True)
    for h in hits:
        pygame.mixer.Sound.play(explosion)
        enemy = Enemy()
        all_sprites.add(enemy)
        group_enemy.add(enemy)
        SCORE += 10

    screen.fill(BLACK)
    screen.blit(background,background_rect)

    draw_text(screen, 'SCORE: {}'.format(SCORE) , 30, WIDTH-300, 10)
    draw_text(screen, 'Lives: {}'.format(LIVES) , 20, 100, 10)
    if GAMEOVER == True:
        if sound_state == True:
            powerup = pygame.mixer.Sound.play(gameover)
            sound_state = False

        now_gameover = pygame.time.get_ticks()
        if GAMEOVER_FONT == True:
            draw_text(screen, 'GAME OVER' , 100, 150, 300)
            if now_gameover - GAMEOVER_TIME >= 1000:
                GAMEOVER_FONT = False
                GAMEOVER_TIME = now_gameover
        else:
            draw_text(screen, 'GAME OVER' , 50, 280, 330)
            if now_gameover - GAMEOVER_TIME >= 1000:
                GAMEOVER_FONT = True
                GAMEOVER_TIME = now_gameover

        for enemy in group_enemy:
            enemy.kill()

        for medic in group_medicpack:
            medic.kill()

    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
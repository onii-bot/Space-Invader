import math

import pygame
import random
from pygame import mixer

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
lime = (0, 255, 0)

# Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load("./data/background.png")

# Background Music
background_music = mixer.music.load('./data/background.mp3')
pygame.mixer.music.play(-1)

# Player
playerImg = pygame.image.load('./data/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('./data/enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 1.9
enemyY_change = 40

# Bullet
bulletImg = pygame.image.load('./data/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16,y+10))

def has_collided(enemyX,enemyY,bulleyX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulleyX,2))+(math.pow(enemyY-bulletY,2)))
    if distance <= 27:
        return True
    return False


# game loop
running = True

while running:
    screen.fill(lime)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    laser = mixer.Sound('./data/laser.wav')
                    laser.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # Player Movement
    playerX += playerX_change
    player(playerX, playerY)

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    enemyX += enemyX_change
    if enemyX <= 0 or enemyX >= 736:
        enemyX_change *= -1
        enemyY += enemyY_change
    enemy(enemyX, enemyY)

    # Bullet
    if bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    # Collision
    collision = has_collided(enemyX,enemyY,bulletX,bulletY)

    if collision:
        explosion = mixer.Sound('./data/explosion.mp3')
        explosion.play()
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
        bulletY = 480
        bullet_state = 'ready'


    pygame.display.update()

pygame.quit()
quit()

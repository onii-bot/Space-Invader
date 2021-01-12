import math
import random
import pygame
from pygame import mixer

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
lime = (0, 255, 0)

# Initializng pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Creating background
background = pygame.image.load('./data/background.png')

# Background sound
mixer.music.load('./data/background.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invader 2")
icon = pygame.image.load("./data/ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('./data/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('./data/enemy.png')
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemyX_change = 1.9
enemyY_change = 40

# Bullet

# ready = waiting to get fired
# fire = pressed space
bulletImg = pygame.image.load('./data/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16,y+10))

def has_collided(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance <= 27:
        return True
    return False

def show_score(x,y):
    score = font.render('Score: '+str(score_value),True,lime)
    screen.blit(score,(x,y))


# Game Loop
running = True

while running:

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
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('./data/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change

    # Enemy Movement
    enemyX += enemyX_change

    if enemyX <= 0 or enemyX >= 736:
        enemyX_change *= -1
        enemyY += enemyY_change

    # Border Checking
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = has_collided(enemyX,enemyY,bulletX,bulletY)

    if collision:
        explosion_sound = mixer.Sound('./data/explosion.mp3')
        explosion_sound.play()
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)
        bulletY = 480
        bullet_state = 'ready'
        score_value += 27

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX,textY)
    pygame.display.update()

pygame.quit()
quit()

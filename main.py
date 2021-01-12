import pygame
import random
import math
from pygame import mixer

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
lime = (0, 255, 0)

# initializng pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# creating background
background = pygame.image.load("./data/background.png")

# background sound
mixer.music.load("./data/background.mp3")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./data/ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("./data/player.png")
playerX = 370
playerY = 480
playerX_Change = 0

# Enemy
EnemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("./data/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(1.8)
    enemyY_Change.append(40)

# Bullet

# ready = waiting to get fired
# fire = pressed space
bulletImg = pygame.image.load("./data/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_xChange = 0
bullet_yChange = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def has_collided(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, lime)
    screen.blit(score, (x, y))


def game_over_text():
    with open('./data/high score.txt','r') as f:
        prev_score = f.read()
    if score_value > int(prev_score):
        with open("./data/high score.txt",'w') as f1:
            f1.write(str(score_value))
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True

while running:
    screen.fill(black)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('./data/laser.wav')
                    bullet_sound.play()
                    bullet_x = playerX
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_Change = 0

    playerX += playerX_Change

    # checking boundary of spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] *= -1
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] *= -1
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = has_collided(enemyX[i], enemyY[i], bullet_x, bullet_y)

        if collision:
            explosion_sound = mixer.Sound('./data/explosion.mp3')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 27
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_yChange

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
quit()

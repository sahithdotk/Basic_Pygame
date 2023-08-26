import pygame
import math
import random
from pygame import mixer

# Initialise the pygame.
pygame.init()

# Create the screen. (remember to add a bracket inside the existing bracket.)
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('mainback.jpg')

# background sound
mixer.music.load('background-music.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Bug's Adventure")
icon = pygame.image.load('PLayer.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('Player.png')
playerX = 1
playerY = 500
playerX_change = 0

# Fireball - you cant see the bullet on the screen
# Fire - The fireball is moving.
fireball_img = pygame.image.load('Fireball.png')
fireballX = 0
fireballY = 480
fireballX_change = 0
fireballY_change = 0.4
fireball_state = "ready"

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,770))
    enemyY.append(random.randint(20,80))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Score
score_value = 0
font = pygame.font.Font('dogicapixel.ttf',32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('dogicapixel.ttf',64)

# defining scoreboard
def show_score(x,y):
    score = font.render("Score :" + str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

# defining game over screen
def game_over_text():
    over_text = over_font.render("GAME OVER :(",True, (255,255,255))
    screen.blit(over_text, (200, 250))
    
# defining players
def player(x,y):
    screen.blit(player_img, (x, y))

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x, y))

# defining fireball
def fireball(x,y):
    global fireball_state
    fireball_state = 'fire'
    screen.blit(fireball_img, (x + 10, y + 10))

# define collision system
def isCollision(enemyX, enemyY, fireballX, fireballY):
    distance = math.sqrt(math.pow(enemyX - fireballX,2) + math.pow(enemyY - fireballY,2))
    if distance < 27:
        return True 
    else:
        return False
    
# Game loop
running = True
while running: 
    # Screen contents
    screen.fill((255, 255, 255))
    # background image
    screen.blit(background, (0,0))
    
    # Here the (+) will make the character move towards right, (-) will make the player go the opposite direction
    # playerX += 0.1
    
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    # If a keystroke is pressed, check whether it is right or left.
         if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.3
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.3
                if event.key == pygame.K_SPACE:
                    if fireball_state == 'ready':
                        
                        # get the current x of the player
                        fireballX = playerX
                        fireball(playerX, fireballY)
                    
         if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
    
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change 
       
    # Adding deadzones to the screen so that player stays in the window.   
    if playerX <= 0:
        playerX = 0
    elif playerX >= 770:
        playerX = 770
         
    enemyX += enemyX_change
    
# Enemy movement
    for i in range(num_of_enemies):
        
        # Game Over
        if enemyY[i] > 440:
            for i in range(num_of_enemies):
                enemyY[1] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 770:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        
        # Collision   
        collision = isCollision(enemyX[i], enemyY[i], fireballX, fireballY)
        if collision:
            fireballY = 480
            fireball_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0,770)
            enemyY[i] = random.randint(20,80)
            
        enemy(enemyX[i], enemyY[i], i)
        
    # Bullet movement
    if fireballY <= 0:
        fireballY = 480
        fireball_state = "ready"
    
    if fireball_state == "fire":
        fireball(fireballX, fireballY)
        fireballY -= fireballY_change
         
    player(playerX, playerY)     
    show_score(textX, textY)
    pygame.display.update()


import pygame
import sys
import os
import random
import time

pygame.init()

# Constants for colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants for screen dimensions and game parameters
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# Fonts for displaying text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Loading background image
background = pygame.image.load("AnimatedStreet.png")

# Creating the display surface
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Class for enemy sprites
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("red.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Class for player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("blue.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

# Class for coin sprites
class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_type):
        super().__init__()
        if coin_type == "normal":
            self.image = pygame.image.load("Coin.png")
            self.radius = 15  # Normal coin radius
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(40, SCREEN_HEIGHT - 40),
        )

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                random.randint(40, SCREEN_HEIGHT - 40),
            )

# Creating player instance
P1 = Player()

# Creating enemy instance
E1 = Enemy()

# Creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

# Event to increase speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

collected_coins = 0

# Function to spawn coins
def spawn_coin():
    coins.empty()
    coin_types = ["normal"]  # Define types of coins
    coin_type = random.choice(coin_types)  # Randomly choose a type
    coin = Coin(coin_type)
    coins.add(coin)

spawn_coin()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render("Coins: " + str(collected_coins), True, BLACK)
    DISPLAYSURF.blit(scores, (300, 10))

    # Updating positions and displaying sprites
    for entity in [P1, E1] + coins.sprites():
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision detection with coins
    if pygame.sprite.spritecollideany(P1, coins):
        pygame.mixer.Sound("collectcoin-6075.mp3").play()
        collected_coins += 1
        for coin in coins:
            coin.rect.top = -100
        spawn_coin()

    # Collision detection with enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash-7075.mp3").play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    pygame.time.Clock().tick(60)

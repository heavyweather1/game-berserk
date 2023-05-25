import pygame
import random
from pygame import *

# Initialize Pygame
pygame.init()

# Set the screen size and caption
size = (width, height) = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2D-Game")

# Define colors
WHITE = (255, 255, 255)

# Load images
background_image = pygame.image.load("background.png")
player_image_left = pygame.image.load("player_left.png")
player_image_right = pygame.image.load("player_right.png")
enemy_image1 = pygame.image.load("enemy1.png")
enemy_image2 = pygame.image.load("enemy2.png")
collectible_image = pygame.image.load("collectible.png")

# Load sounds
move_sound = pygame.mixer.Sound("move_sound.wav")
collect_sound = pygame.mixer.Sound("collect_sound.wav")
collision_sound = pygame.mixer.Sound("collision_sound.wav")

# Game variables
player_pos = [100, 100]
player_speed = 5
player_direction = "right"

enemies = []
enemy_speed = 3

collectibles = []
collectible_speed = 4

score = 0
lives = 3

# Function to draw the player character
def draw_player():
    if player_direction == "left":
        screen.blit(player_image_left, player_pos)
    else:
        screen.blit(player_image_right, player_pos)

# Function to draw the enemies
def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy["image"], enemy["pos"])

# Function to draw the collectibles
def draw_collectibles():
    for collectible in collectibles:
        screen.blit(collectible_image, collectible["pos"])

# Function to update the player character
def update_player():
    global player_pos, player_direction

    keys = pygame.key.get_pressed()

    if keys[K_LEFT]:
        player_pos[0] -= player_speed
        player_direction = "left"
        move_sound.play()

    if keys[K_RIGHT]:
        player_pos[0] += player_speed
        player_direction = "right"
        move_sound.play()

    if keys[K_UP]:
        player_pos[1] -= player_speed
        move_sound.play()

    if keys[K_DOWN]:
        player_pos[1] += player_speed
        move_sound.play()

# Function to update the enemies
def update_enemies():
    for enemy in enemies:
        enemy["pos"][1] += enemy_speed
        if enemy["pos"][1] > height:
            enemy["pos"][1] = 0 - enemy["pos"][3]

# Function to update the collectibles
def update_collectibles():
    for collectible in collectibles:
        collectible["pos"][1] += collectible_speed
        if collectible["pos"][1] > height:
            collectible["pos"][1] = 0 - collectible["pos"][3]

# Function to handle collisions between player and enemies
def check_collision():
    global score, lives

    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_image_left.get_width(), player_image_left.get_height())

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy["image"].get_width(), enemy["image"].get_height())

        if player_rect.colliderect(enemy_rect):
            collision_sound.play()
            lives -= 1
            if lives == 0:
                game_over()

    for collectible in collectibles:
        collectible_rect = pygame.Rect(collectible["pos"][0], collectible["pos"][1], collectible_image.get_width(), collectible_image.get_height())

        if player_rect.colliderect(collectible_rect):
            collect_sound.play()
            score += 1
            collectibles.remove(collectible)

# Function to display the current score and lives on the screen
def display_stats():
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, WHITE)
    lives_text = font.render("Lives: " + str(lives), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

# Function to display the start screen
def start_screen():
    font = pygame.font.SysFont(None, 80)
    text = font.render("2D-Game", True, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

# Function to display the game over screen
def game_over():
    global running

    font = pygame.font.SysFont(None, 80)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

    running = False

# Initialize enemies
enemies.append({"image": enemy_image1, "pos": [random.randint(0, width - enemy_image1.get_width()), 0 - enemy_image1.get_height()]})
enemies.append({"image": enemy_image2, "pos": [random.randint(0, width - enemy_image2.get_width()), 0 - enemy_image2.get_height()]})

# Initialize collectibles
collectibles.append({"pos": [random.randint(0, width - collectible_image.get_width()), 0 - collectible_image.get_height()]})

# Start the game
start_screen()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    update_player()
    update_enemies()
    update_collectibles()

    check_collision()

    draw_player()
    draw_enemies()
    draw_collectibles()

    display_stats()

    pygame.display.flip()

    clock.tick(60)

# Quit the game
pygame.quit()
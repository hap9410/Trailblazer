import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trailblazer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player Settings
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# Enemy Settings
enemy_size = 40
enemy_speed = 3
enemy_list = []

# Collectible Settings
token_size = 30
token_list = []

# Game Variables
score = 0
lives = 3
game_over = False

# Fonts
font = pygame.font.Font(None, 36)

# Functions
def create_enemy():
    x = random.randint(0, WIDTH - enemy_size)
    y = random.randint(-100, -40)
    return pygame.Rect(x, y, enemy_size, enemy_size)

def create_token():
    x = random.randint(0, WIDTH - token_size)
    y = random.randint(-100, -40)
    return pygame.Rect(x, y, token_size, token_size)

def draw_text(text, x, y, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Main Game Loop
while True:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

        # Create Enemies and Tokens
        if random.randint(1, 100) < 3:
            enemy_list.append(create_enemy())
        if random.randint(1, 100) < 2:
            token_list.append(create_token())

        # Move Enemies
        for enemy in enemy_list[:]:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemy_list.remove(enemy)
            if player_rect.colliderect(enemy):
                lives -= 1
                enemy_list.remove(enemy)
                if lives == 0:
                    game_over = True

        # Move Tokens
        for token in token_list[:]:
            token.y += 2
            if token.top > HEIGHT:
                token_list.remove(token)
            if player_rect.colliderect(token):
                score += 1
                token_list.remove(token)

    # Draw Everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, player_rect)

    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, enemy)

    for token in token_list:
        pygame.draw.rect(screen, GREEN, token)

    # Display Score and Lives
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", 10, 50)

    if game_over:
        draw_text("Game Over! Press R to Restart", WIDTH // 2 - 150, HEIGHT // 2, RED)

    # Restart Game
    if game_over and pygame.key.get_pressed()[pygame.K_r]:
        score = 0
        lives = 3
        enemy_list.clear()
        token_list.clear()
        game_over = False

    pygame.display.flip()
    clock.tick(FPS)
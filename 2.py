import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define snake properties
BLOCK_SIZE = 20
SNAKE_SPEED_LEVELS = [10, 15, 20, 25, 30]  # Speed for each level
SCORE_TO_PASS_LEVEL = 5  # Score needed to pass each level

# Define initial snake position and direction
snake_pos = [WIDTH // 2, HEIGHT // 2]
snake_body = [[snake_pos[0], snake_pos[1]],
              [snake_pos[0] - BLOCK_SIZE, snake_pos[1]],
              [snake_pos[0] - 2 * BLOCK_SIZE, snake_pos[1]]]
direction = "RIGHT"


# Function to draw snake
def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(WIN, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))


# Function to generate food (medium or large, skipping small)
def generate_food():
    food_sizes = ["medium", "large"]  # Define sizes for food, excluding small
    food_size = random.choice(food_sizes)  # Randomly choose a size
    food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    return food_pos, food_size


# Function to display game over screen
def show_game_over_screen():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Score: {score}", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # Pause for 2 seconds before exiting
    pygame.quit()


# Main game loop
clock = pygame.time.Clock()
food_pos, food_size = generate_food()  # Define food position and size before the main loop
food_timer = 100  # Initial value for food timer
score = 0
level = 1
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    elif keys[pygame.K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"
    elif keys[pygame.K_UP] and direction != "DOWN":
        direction = "UP"
    elif keys[pygame.K_DOWN] and direction != "UP":
        direction = "DOWN"

    # Move the snake
    if direction == "RIGHT":
        snake_pos[0] += BLOCK_SIZE
    elif direction == "LEFT":
        snake_pos[0] -= BLOCK_SIZE
    elif direction == "UP":
        snake_pos[1] -= BLOCK_SIZE
    elif direction == "DOWN":
        snake_pos[1] += BLOCK_SIZE

    # Check for wall collision and adjust snake position
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over = True

    # Check if snake collides with itself
    if snake_pos in snake_body[1:]:
        game_over = True

    # Update snake body
    snake_body.insert(0, list(snake_pos))
    if snake_pos != food_pos:  # Check if snake eats food
        snake_body.pop()  # Remove the last segment of the snake's body when it moves
    else:
        if food_size == "medium":  # Medium food gives 1 point
            score += 1
        elif food_size == "large":  # Large food gives 2 points
            score += 2
        # Generate new food position, size, and timer
        food_pos, food_size = generate_food()
        food_timer = 100  # Reset food timer when new food is generated

    # Update food timer
    food_timer -= 1
    if food_timer == 0:
        food_pos, food_size = generate_food()  # Generate new food position and size
        food_timer = 100  # Reset food timer when new food is generated

    # Draw everything
    WIN.fill(WHITE)
    draw_snake(snake_body)
    if food_size == "medium":
        food_color = RED
    else:  # Large size
        food_color = BLACK
    pygame.draw.rect(WIN, food_color, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Display score and timer
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(score_text, (10, 10))
    timer_text = font.render(f"Timer: {food_timer}", True, BLACK)
    WIN.blit(timer_text, (10, 30))

    pygame.display.update()

    # Display score and level
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    WIN.blit(score_text, (10, 10))

    pygame.display.update()

    # Update game clock
    clock.tick(SNAKE_SPEED_LEVELS[level - 1])

show_game_over_screen()


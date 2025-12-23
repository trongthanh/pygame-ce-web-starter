import pygame
import random
import math

# Module metadata
title = "Breakout Game"
info = "Classic brick-breaking game. Use <strong>LEFT/RIGHT arrow keys</strong> to move the paddle. Break all blocks to win!"

# Game constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Game state variables
game_paused = False
game_over = False
game_won = False

# Create surfaces
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Paddle
paddle_width = 75
paddle_height = 8
paddle_speed = 6
paddle_x = (SCREEN_WIDTH - paddle_width) // 2
paddle_y = SCREEN_HEIGHT - 23

# Ball
ball_size = 6
ball_speed_x = 3
ball_speed_y = -3
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT - 30

# Blocks
block_rows = 5
block_cols = 10
block_width = 38
block_height = 15
block_padding = 4
block_offset_top = 45
block_offset_left = 26

# Create blocks with different colors for different rows
blocks = []
block_colors = [RED, ORANGE, YELLOW, GREEN, CYAN]

for row in range(block_rows):
    for col in range(block_cols):
        block_x = col * (block_width + block_padding) + block_offset_left
        block_y = row * (block_height + block_padding) + block_offset_top
        block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
        blocks.append((block_rect, block_colors[row]))

# Fonts
font_large = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 27)
font_small = pygame.font.Font(None, 18)


def reset_game():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, blocks, game_over, game_won

    # Reset paddle
    paddle_x = (SCREEN_WIDTH - paddle_width) // 2

    # Reset ball
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT - 30
    ball_speed_x = 3 * random.choice([-1, 1])
    ball_speed_y = -3

    # Reset blocks
    blocks = []
    for row in range(block_rows):
        for col in range(block_cols):
            block_x = col * (block_width + block_padding) + block_offset_left
            block_y = row * (block_height + block_padding) + block_offset_top
            block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
            blocks.append((block_rect, block_colors[row]))

    game_over = False
    game_won = False


def set_pause(paused):
    global game_paused
    game_paused = paused


def update():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, game_paused, game_over, game_won

    if not game_paused and not game_over and not game_won:
        # Get keys
        keys = pygame.key.get_pressed()

        # Move paddle
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
            paddle_x += paddle_speed

        # Move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= SCREEN_WIDTH - ball_size:
            ball_speed_x = -ball_speed_x

        # Ball collision with ceiling
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

        if paddle_rect.colliderect(ball_rect) and ball_speed_y > 0:
            ball_speed_y = -ball_speed_y
            # Add some spin based on where the ball hits the paddle
            hit_pos = (ball_x - paddle_x) / paddle_width
            ball_speed_x = 6 * (hit_pos - 0.5)

        # Ball collision with blocks
        blocks_to_remove = []
        for block_rect, color in blocks:
            if block_rect.colliderect(ball_rect):
                ball_speed_y = -ball_speed_y
                blocks_to_remove.append((block_rect, color))
                break  # Only remove one block per frame

        for block in blocks_to_remove:
            blocks.remove(block)

        # Check win condition
        if len(blocks) == 0:
            game_won = True

        # Ball out of bounds (game over)
        if ball_y > SCREEN_HEIGHT:
            game_over = True


def draw():
    # Clear screen
    screen.fill(BLACK)

    # Draw paddle
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    pygame.draw.rect(screen, WHITE, paddle_rect)

    # Draw ball
    ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)
    pygame.draw.rect(screen, WHITE, ball_rect)

    # Draw blocks
    for block_rect, color in blocks:
        pygame.draw.rect(screen, color, block_rect)

    # Draw status text
    if game_paused:
        pause_text = font_large.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, text_rect)
    elif game_over:
        game_over_text = font_large.render("GAME OVER", True, RED)
        restart_text = font_medium.render("Press Reset to play again", True, WHITE)
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        )
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
    elif game_won:
        win_text = font_large.render("YOU WIN!", True, GREEN)
        restart_text = font_medium.render("Press Reset to play again", True, WHITE)
        win_rect = win_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        )
        screen.blit(win_text, win_rect)
        screen.blit(restart_text, restart_rect)

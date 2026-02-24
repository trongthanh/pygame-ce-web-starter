import pygame

# Game metadata
title = "Blank Game"
info = "<p>Use arrow keys to play</p>"

# Display
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game state
game_paused = False


def reset_game():
    pass


def set_pause(paused):
    global game_paused
    game_paused = paused


def update():
    if game_paused:
        return


def draw():
    screen.fill(BLACK)

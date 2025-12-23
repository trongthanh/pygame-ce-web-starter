import pygame

size = width, height = 480, 360
speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)
# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()
# Create a font object
font = pygame.font.Font(None, 18)
text_surface = font.render("Hello World", True, (255, 255, 255))


def update():
    pass


def draw():
    screen.fill(black)
    pygame.draw.circle(screen, white, (50, 50), 20)

    screen.blit(text_surface, (2, 2))

# Interface functions for JavaScript (no-op for demo)
def reset_game():
    pass

def set_pause(paused):
    pass

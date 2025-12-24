import pygame
import random

# Game metadata
title = "Chrome Dino Game"
info = """
<p>Press SPACE or UP ARROW to jump</p>
<p>Avoid the cacti!</p>
"""

# Initialize display
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino")

# Colors
WHITE = (247, 247, 247)
BLACK = (83, 83, 83)
CLOUD_COLOR = (172, 172, 172)

# Game constants
GRAVITY = 0.6
JUMP_STRENGTH = -12
GROUND_HEIGHT = 280
DINO_X = 40
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_DISTANCE = 350

# Helper function for text rendering
def render_pixelated_text(text, size, color):
    """Render clean text with monospace font"""
    # Try to load monospace fonts (Menlo, SF Mono, or Consolas)
    font = None
    for font_name in ['Menlo', 'SF Mono', 'Consolas', 'Monaco', 'Courier New']:
        try:
            font = pygame.font.SysFont(font_name, size)
            break
        except:
            continue

    # Fallback to default if no monospace font found
    if font is None:
        font = pygame.font.Font(None, size)

    # Render with antialiasing for smooth, clean text
    return font.render(text, True, color)

# Drawing functions for pixel art sprites
def draw_dino(surface, x, y, frame_count, is_jumping):
    """Draw T-Rex in pixel art style matching Chrome Dino game"""
    dino_color = BLACK

    # Head - top part
    pygame.draw.rect(surface, dino_color, (x + 22, y, 22, 4))  # Top of head
    pygame.draw.rect(surface, dino_color, (x + 18, y + 4, 26, 4))  # Upper head
    pygame.draw.rect(surface, dino_color, (x + 18, y + 8, 22, 4))  # Mid head

    # Eye
    pygame.draw.rect(surface, WHITE, (x + 30, y + 4, 4, 4))

    # Mouth/Jaw area
    pygame.draw.rect(surface, dino_color, (x + 18, y + 12, 18, 4))  # Jaw line
    pygame.draw.rect(surface, dino_color, (x + 22, y + 16, 10, 4))  # Lower jaw

    # Neck to body transition
    pygame.draw.rect(surface, dino_color, (x + 10, y + 16, 12, 4))
    pygame.draw.rect(surface, dino_color, (x + 6, y + 20, 16, 4))

    # Main body
    pygame.draw.rect(surface, dino_color, (x, y + 24, 18, 4))
    pygame.draw.rect(surface, dino_color, (x, y + 28, 22, 8))

    # Back detail
    pygame.draw.rect(surface, dino_color, (x + 2, y + 20, 4, 4))

    # Tail - curves upward
    pygame.draw.rect(surface, dino_color, (x - 4, y + 28, 4, 4))
    pygame.draw.rect(surface, dino_color, (x - 8, y + 24, 4, 4))
    pygame.draw.rect(surface, dino_color, (x - 10, y + 20, 2, 4))

    # Arms - small T-Rex arms
    pygame.draw.rect(surface, dino_color, (x + 12, y + 24, 4, 2))
    pygame.draw.rect(surface, dino_color, (x + 12, y + 26, 2, 4))

    # Legs with running animation
    if not is_jumping:
        leg_frame = (frame_count // 5) % 2
        if leg_frame == 0:
            # Left leg forward
            pygame.draw.rect(surface, dino_color, (x + 2, y + 36, 6, 4))
            pygame.draw.rect(surface, dino_color, (x + 4, y + 40, 4, 6))
            pygame.draw.rect(surface, dino_color, (x + 2, y + 46, 8, 2))
            # Right leg back
            pygame.draw.rect(surface, dino_color, (x + 12, y + 36, 6, 10))
            pygame.draw.rect(surface, dino_color, (x + 12, y + 46, 8, 2))
        else:
            # Right leg forward
            pygame.draw.rect(surface, dino_color, (x + 12, y + 36, 6, 4))
            pygame.draw.rect(surface, dino_color, (x + 14, y + 40, 4, 6))
            pygame.draw.rect(surface, dino_color, (x + 12, y + 46, 8, 2))
            # Left leg back
            pygame.draw.rect(surface, dino_color, (x + 2, y + 36, 6, 10))
            pygame.draw.rect(surface, dino_color, (x + 2, y + 46, 8, 2))
    else:
        # Both legs together when jumping
        pygame.draw.rect(surface, dino_color, (x + 2, y + 36, 6, 10))
        pygame.draw.rect(surface, dino_color, (x + 2, y + 46, 8, 2))
        pygame.draw.rect(surface, dino_color, (x + 12, y + 36, 6, 10))
        pygame.draw.rect(surface, dino_color, (x + 12, y + 46, 8, 2))

def draw_cactus_small(surface, x, y):
    """Draw small cactus"""
    # Main body
    pygame.draw.rect(surface, BLACK, (x + 4, y, 8, 24))
    # Left arm
    pygame.draw.rect(surface, BLACK, (x, y + 8, 4, 8))
    pygame.draw.rect(surface, BLACK, (x, y + 8, 6, 4))
    # Right arm
    pygame.draw.rect(surface, BLACK, (x + 12, y + 12, 4, 8))
    pygame.draw.rect(surface, BLACK, (x + 10, y + 12, 6, 4))
    return pygame.Rect(x + 2, y, 14, 24)

def draw_cactus_large(surface, x, y):
    """Draw large cactus"""
    # Main body
    pygame.draw.rect(surface, BLACK, (x + 6, y, 8, 32))
    # Left arm high
    pygame.draw.rect(surface, BLACK, (x, y + 4, 6, 12))
    pygame.draw.rect(surface, BLACK, (x, y + 4, 8, 4))
    # Right arm low
    pygame.draw.rect(surface, BLACK, (x + 14, y + 16, 6, 12))
    pygame.draw.rect(surface, BLACK, (x + 12, y + 16, 8, 4))
    return pygame.Rect(x, y, 20, 32)

def draw_cactus_double(surface, x, y):
    """Draw double small cactus"""
    # First cactus
    pygame.draw.rect(surface, BLACK, (x + 4, y, 6, 24))
    pygame.draw.rect(surface, BLACK, (x, y + 8, 4, 8))
    pygame.draw.rect(surface, BLACK, (x, y + 8, 6, 4))

    # Second cactus
    pygame.draw.rect(surface, BLACK, (x + 14, y, 6, 24))
    pygame.draw.rect(surface, BLACK, (x + 20, y + 12, 4, 8))
    pygame.draw.rect(surface, BLACK, (x + 18, y + 12, 6, 4))

    return pygame.Rect(x, y, 24, 24)

def draw_cloud(surface, x, y):
    """Draw a cloud in pixel art style"""
    # Cloud parts
    pygame.draw.rect(surface, CLOUD_COLOR, (x, y + 4, 8, 4))
    pygame.draw.rect(surface, CLOUD_COLOR, (x + 8, y, 12, 8))
    pygame.draw.rect(surface, CLOUD_COLOR, (x + 20, y + 4, 8, 4))

# Game state
class DinoGame:
    def __init__(self):
        self.dino_y = GROUND_HEIGHT - 48
        self.dino_velocity = 0
        self.is_jumping = False
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self.frame_count = 0
        self.ground_offset = 0
        self.cloud_offset = 0

        # Initialize clouds
        for i in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(40, 120)
            })

    def reset(self):
        self.dino_y = GROUND_HEIGHT - 48
        self.dino_velocity = 0
        self.is_jumping = False
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        self.ground_offset = 0
        self.cloud_offset = 0

        # Reset clouds
        self.clouds = []
        for i in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(40, 120)
            })

    def jump(self):
        if not self.is_jumping and not self.game_over:
            self.is_jumping = True
            self.dino_velocity = JUMP_STRENGTH

    def update_game(self):
        if self.paused or self.game_over:
            return

        self.frame_count += 1

        # Update score
        self.score += 1

        # Update dino physics
        self.dino_velocity += GRAVITY
        self.dino_y += self.dino_velocity

        # Ground collision
        if self.dino_y >= GROUND_HEIGHT - 48:
            self.dino_y = GROUND_HEIGHT - 48
            self.dino_velocity = 0
            self.is_jumping = False

        # Update ground scrolling
        self.ground_offset = (self.ground_offset + OBSTACLE_SPEED) % 20

        # Update cloud parallax scrolling (slower than ground)
        cloud_speed = OBSTACLE_SPEED * 0.3
        for cloud in self.clouds:
            cloud['x'] -= cloud_speed
            if cloud['x'] < -40:
                cloud['x'] = SCREEN_WIDTH + random.randint(0, 100)
                cloud['y'] = random.randint(40, 120)

        # Spawn obstacles
        if len(self.obstacles) == 0 or self.obstacles[-1]['x'] < SCREEN_WIDTH - OBSTACLE_SPAWN_DISTANCE:
            spawn_distance = random.randint(300, 450)
            if len(self.obstacles) == 0 or self.obstacles[-1]['x'] < SCREEN_WIDTH - spawn_distance:
                cactus_type = random.choice(['small', 'large', 'double'])
                self.obstacles.append({
                    'x': SCREEN_WIDTH,
                    'type': cactus_type
                })

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle['x'] -= OBSTACLE_SPEED

            # Remove off-screen obstacles
            if obstacle['x'] < -30:
                self.obstacles.remove(obstacle)

            # Collision detection (adjusted for new dino size)
            dino_rect = pygame.Rect(DINO_X + 4, self.dino_y + 8, 36, 38)

            # Get obstacle hitbox based on type
            if obstacle['type'] == 'small':
                obstacle_rect = pygame.Rect(obstacle['x'] + 2, GROUND_HEIGHT - 24, 14, 24)
            elif obstacle['type'] == 'large':
                obstacle_rect = pygame.Rect(obstacle['x'], GROUND_HEIGHT - 32, 20, 32)
            else:  # double
                obstacle_rect = pygame.Rect(obstacle['x'], GROUND_HEIGHT - 24, 24, 24)

            if dino_rect.colliderect(obstacle_rect):
                self.game_over = True

    def draw_game(self):
        # Clear screen
        screen.fill(WHITE)

        # Draw clouds (parallax background)
        for cloud in self.clouds:
            draw_cloud(screen, int(cloud['x']), int(cloud['y']))

        # Draw ground line
        pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

        # Draw ground bumps (for texture)
        for i in range(-1, SCREEN_WIDTH // 20 + 1):
            x = i * 20 - self.ground_offset
            if random.randint(0, 10) < 3:
                pygame.draw.rect(screen, BLACK, (x, GROUND_HEIGHT + 2, 2, 2))

        # Draw dino
        draw_dino(screen, DINO_X, int(self.dino_y), self.frame_count, self.is_jumping)

        # Draw obstacles
        for obstacle in self.obstacles:
            if obstacle['type'] == 'small':
                draw_cactus_small(screen, int(obstacle['x']), GROUND_HEIGHT - 24)
            elif obstacle['type'] == 'large':
                draw_cactus_large(screen, int(obstacle['x']), GROUND_HEIGHT - 32)
            else:  # double
                draw_cactus_double(screen, int(obstacle['x']), GROUND_HEIGHT - 24)

        # Draw score (top right) with pixelated font - larger and bolder
        score_text = render_pixelated_text(f"{self.score:05d}", 42, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH - 120, 15))

        # Draw game over
        if self.game_over:
            game_over_text = render_pixelated_text("G A M E  O V E R", 45, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(game_over_text, text_rect)

            restart_text = render_pixelated_text("Press RESET to restart", 27, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
            screen.blit(restart_text, restart_rect)

        # Draw pause indicator
        if self.paused:
            pause_text = render_pixelated_text("| |", 45, BLACK)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(pause_text, text_rect)

# Create game instance
game = DinoGame()

# Game interface functions
def update():
    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        game.jump()

    game.update_game()

def draw():
    game.draw_game()

def reset_game():
    game.reset()

def set_pause(paused):
    game.paused = paused

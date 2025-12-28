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

# Drawing functions - simplified for sprite replacement
def draw_dino(surface, x, y, frame_count, is_jumping):
    """Draw simplified T-Rex - body as single rect, 2 rects for leg animation"""
    dino_color = BLACK

    # Body (simplified to single rect)
    pygame.draw.rect(surface, dino_color, (x, y, 40, 36))

    # Eye (small white circle)
    pygame.draw.circle(surface, WHITE, (x + 30, y + 10), 3)

    # Legs with running animation (2 rects)
    if not is_jumping:
        leg_frame = (frame_count // 5) % 2
        if leg_frame == 0:
            # Left leg forward, right leg back
            pygame.draw.rect(surface, dino_color, (x + 8, y + 36, 8, 12))
            pygame.draw.rect(surface, dino_color, (x + 24, y + 36, 8, 12))
        else:
            # Right leg forward, left leg back
            pygame.draw.rect(surface, dino_color, (x + 8, y + 36, 8, 12))
            pygame.draw.rect(surface, dino_color, (x + 24, y + 36, 8, 12))
    else:
        # Both legs together when jumping
        pygame.draw.rect(surface, dino_color, (x + 8, y + 36, 8, 12))
        pygame.draw.rect(surface, dino_color, (x + 24, y + 36, 8, 12))

def draw_cactus_small(surface, x, y):
    """Draw small cactus - simplified to single rect"""
    pygame.draw.rect(surface, BLACK, (x, y, 16, 24))
    return pygame.Rect(x, y, 16, 24)

def draw_cactus_large(surface, x, y):
    """Draw large cactus - simplified to single rect"""
    pygame.draw.rect(surface, BLACK, (x, y, 20, 32))
    return pygame.Rect(x, y, 20, 32)

def draw_cactus_double(surface, x, y):
    """Draw double cactus - simplified to single rect"""
    pygame.draw.rect(surface, BLACK, (x, y, 30, 24))
    return pygame.Rect(x, y, 30, 24)

def draw_cloud(surface, x, y):
    """Draw a cloud - simplified to single circle"""
    pygame.draw.circle(surface, CLOUD_COLOR, (int(x + 15), int(y + 6)), 12)

# Game state (module-level variables)
dino_y = GROUND_HEIGHT - 48
dino_velocity = 0
is_jumping = False
game_started = False
obstacles = []
clouds = []
score = 0
game_over = False
paused = False
frame_count = 0
ground_offset = 0
cloud_offset = 0

# Initialize clouds
for i in range(5):
    clouds.append({
        'x': random.randint(0, SCREEN_WIDTH),
        'y': random.randint(40, 120)
    })

def jump():
    global is_jumping, dino_velocity, game_over, game_started
    if not is_jumping and not game_over:
        is_jumping = True
        dino_velocity = JUMP_STRENGTH
        game_started = True  # Start the game on first jump

# Game interface functions
def update():
    global dino_y, dino_velocity, is_jumping, obstacles, score, game_over
    global frame_count, ground_offset, paused, clouds, game_started

    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        jump()

    if paused or game_over:
        return

    frame_count += 1

    # Update dino physics (always update, even before game starts)
    dino_velocity += GRAVITY
    dino_y += dino_velocity

    # Ground collision
    if dino_y >= GROUND_HEIGHT - 48:
        dino_y = GROUND_HEIGHT - 48
        dino_velocity = 0
        is_jumping = False

    # Only update world movement if game has started
    if not game_started:
        return

    # Update score
    score += 1

    # Update ground scrolling
    ground_offset = (ground_offset + OBSTACLE_SPEED) % 20

    # Update cloud parallax scrolling (slower than ground)
    cloud_speed = OBSTACLE_SPEED * 0.3
    for cloud in clouds:
        cloud['x'] -= cloud_speed
        if cloud['x'] < -40:
            cloud['x'] = SCREEN_WIDTH + random.randint(0, 100)
            cloud['y'] = random.randint(40, 120)

    # Spawn obstacles
    if len(obstacles) == 0 or obstacles[-1]['x'] < SCREEN_WIDTH - OBSTACLE_SPAWN_DISTANCE:
        spawn_distance = random.randint(300, 450)
        if len(obstacles) == 0 or obstacles[-1]['x'] < SCREEN_WIDTH - spawn_distance:
            cactus_type = random.choice(['small', 'large', 'double'])
            obstacles.append({
                'x': SCREEN_WIDTH,
                'type': cactus_type
            })

    # Update obstacles
    for obstacle in obstacles[:]:
        obstacle['x'] -= OBSTACLE_SPEED

        # Remove off-screen obstacles
        if obstacle['x'] < -30:
            obstacles.remove(obstacle)

        # Collision detection (adjusted for simplified dino)
        dino_rect = pygame.Rect(DINO_X, dino_y, 40, 48)

        # Get obstacle hitbox based on type
        if obstacle['type'] == 'small':
            obstacle_rect = pygame.Rect(obstacle['x'], GROUND_HEIGHT - 24, 16, 24)
        elif obstacle['type'] == 'large':
            obstacle_rect = pygame.Rect(obstacle['x'], GROUND_HEIGHT - 32, 20, 32)
        else:  # double
            obstacle_rect = pygame.Rect(obstacle['x'], GROUND_HEIGHT - 24, 30, 24)

        if dino_rect.colliderect(obstacle_rect):
            game_over = True

def draw():
    global clouds, obstacles, score, game_over, paused, ground_offset, dino_y, frame_count, is_jumping

    # Clear screen
    screen.fill(WHITE)

    # Draw clouds (parallax background)
    for cloud in clouds:
        draw_cloud(screen, int(cloud['x']), int(cloud['y']))

    # Draw ground line
    pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

    # Draw ground bumps (for texture) - fixed pattern that scrolls
    for i in range(-1, SCREEN_WIDTH // 20 + 2):
        x = i * 20 - ground_offset
        # Calculate the ground tile position (accounts for scrolling)
        tile_pos = (x + int(ground_offset)) // 20
        # Use tile position for deterministic pattern
        if (tile_pos * 7) % 13 < 4:  # Creates a fixed repeating pattern
            pygame.draw.rect(screen, BLACK, (x, GROUND_HEIGHT + 2, 2, 2))

    # Draw dino
    draw_dino(screen, DINO_X, int(dino_y), frame_count, is_jumping)

    # Draw obstacles
    for obstacle in obstacles:
        if obstacle['type'] == 'small':
            draw_cactus_small(screen, int(obstacle['x']), GROUND_HEIGHT - 24)
        elif obstacle['type'] == 'large':
            draw_cactus_large(screen, int(obstacle['x']), GROUND_HEIGHT - 32)
        else:  # double
            draw_cactus_double(screen, int(obstacle['x']), GROUND_HEIGHT - 24)

    # Draw score (top right) with pixelated font - larger and bolder
    score_text = render_pixelated_text(f"{score:05d}", 42, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 120, 15))

    # Draw game over
    if game_over:
        game_over_text = render_pixelated_text("G A M E  O V E R", 45, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(game_over_text, text_rect)

        restart_text = render_pixelated_text("Press RESET to restart", 27, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(restart_text, restart_rect)

    # Draw pause indicator
    if paused:
        pause_text = render_pixelated_text("| |", 45, BLACK)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(pause_text, text_rect)

def reset_game():
    global dino_y, dino_velocity, is_jumping, obstacles, score, game_over
    global frame_count, ground_offset, cloud_offset, clouds, game_started

    dino_y = GROUND_HEIGHT - 48
    dino_velocity = 0
    is_jumping = False
    game_started = False
    obstacles = []
    score = 0
    game_over = False
    frame_count = 0
    ground_offset = 0
    cloud_offset = 0

    # Reset clouds
    clouds = []
    for i in range(5):
        clouds.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(40, 120)
        })

def set_pause(pause_state):
    global paused
    paused = pause_state

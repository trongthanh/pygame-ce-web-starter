import pygame
import math

# Module metadata
title = "Pygame Drawing API Demo"
info = "Demonstrates pygame.draw functions: circles, rectangles, lines, ellipses, polygons, and arcs.<br> Automatically cycles through demos every 3 seconds."

size = width, height = 480, 360
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
cyan = 0, 255, 255
magenta = 255, 0, 255
orange = 255, 165, 0
purple = 128, 0, 128

screen = pygame.display.set_mode(size)
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)

# Animation state
demo_index = 0
frame_counter = 0
demos_per_scene = 180  # frames per demo (3 seconds at 60fps)

# Circle animation
circle_angle = 0

# Rectangle animation
rect_x = 0

# Polygon animation
poly_angle = 0

# Line animation
line_y = 0

# Ellipse animation
ellipse_scale = 1.0

paused = False
paused_demos = False


def update():
    global frame_counter, demo_index, circle_angle, rect_x, poly_angle, line_y, ellipse_scale

    if paused:
        return

    frame_counter += 1

    # Switch demos every 3 seconds
    if frame_counter >= demos_per_scene:
        frame_counter = 0
        demo_index = (demo_index + 1) % 7
        # Reset animation states
        circle_angle = 0
        rect_x = 0
        poly_angle = 0
        line_y = 0
        ellipse_scale = 1.0

    # Update animations
    circle_angle += 0.05
    rect_x = (rect_x + 3) % (width - 50)
    poly_angle += 0.03
    line_y = (line_y + 2) % height
    ellipse_scale = 1.0 + 0.3 * math.sin(circle_angle * 2)


def draw_demo_title(title, subtitle=""):
    screen.fill(black)
    title_surface = font.render(title, True, white)
    screen.blit(title_surface, (10, 10))
    if subtitle:
        sub_surface = small_font.render(subtitle, True, cyan)
        screen.blit(sub_surface, (10, 35))


def draw_circles():
    draw_demo_title("pygame.draw.circle()", "draws circles (filled or outlined)")

    # Static filled circles
    pygame.draw.circle(screen, red, (80, 120), 20)
    pygame.draw.circle(screen, green, (80, 180), 25)
    pygame.draw.circle(screen, blue, (80, 240), 30)

    # Animated orbiting circle
    center_x, center_y = 300, 180
    orbit_radius = 80
    x = center_x + int(orbit_radius * math.cos(circle_angle))
    y = center_y + int(orbit_radius * math.sin(circle_angle))
    pygame.draw.circle(screen, yellow, (center_x, center_y), 10)
    pygame.draw.circle(screen, white, (x, y), 15)
    pygame.draw.line(screen, gray(100), (center_x, center_y), (x, y), 1)


def draw_rectangles():
    draw_demo_title("pygame.draw.rect()", "draws rectangles (filled or outlined)")

    # Static rectangles
    pygame.draw.rect(screen, red, (50, 80, 60, 40))
    pygame.draw.rect(screen, green, (50, 140, 70, 50))
    pygame.draw.rect(screen, blue, (50, 210, 80, 60))

    # Outlined rectangle
    pygame.draw.rect(screen, white, (200, 140, 100, 70), 3)

    # Animated moving rectangle
    pygame.draw.rect(screen, orange, (rect_x, 280, 50, 30))


def draw_lines():
    draw_demo_title("pygame.draw.line()", "draws a line segment")

    # Horizontal lines
    pygame.draw.line(screen, red, (50, 80), (200, 80), 2)
    pygame.draw.line(screen, green, (50, 110), (200, 110), 4)
    pygame.draw.line(screen, blue, (50, 140), (200, 140), 6)

    # Vertical lines
    pygame.draw.line(screen, yellow, (250, 70), (250, 150), 3)
    pygame.draw.line(screen, cyan, (300, 70), (300, 150), 3)
    pygame.draw.line(screen, magenta, (350, 70), (350, 150), 3)

    # Diagonal lines
    pygame.draw.line(screen, white, (50, 180), (200, 250), 2)
    pygame.draw.line(screen, orange, (200, 180), (50, 250), 2)

    # Animated scanning line
    pygame.draw.line(screen, green, (0, line_y), (width, line_y), 2)


def draw_ellipses():
    draw_demo_title("pygame.draw.ellipse()", "draws ellipses inside a bounding rect")

    # Static ellipses
    pygame.draw.ellipse(screen, red, (50, 80, 80, 40))
    pygame.draw.ellipse(screen, green, (50, 140, 60, 60))  # circle is special ellipse
    pygame.draw.ellipse(screen, blue, (50, 220, 100, 30))

    # Outlined ellipse
    pygame.draw.ellipse(screen, white, (200, 130, 120, 80), 3)

    # Animated pulsing ellipse
    center_x, center_y = 350, 250
    base_w, base_h = 60, 40
    w = int(base_w * ellipse_scale)
    h = int(base_h * ellipse_scale)
    pygame.draw.ellipse(screen, yellow, (center_x - w // 2, center_y - h // 2, w, h))


def draw_polygons():
    draw_demo_title("pygame.draw.polygon()", "draws a filled or outlined polygon")

    # Static polygons
    pygame.draw.polygon(screen, red, [(50, 80), (100, 80), (75, 40)])  # triangle
    pygame.draw.polygon(
        screen, green, [(50, 120), (100, 120), (120, 160), (30, 160)]
    )  # trapezoid
    pygame.draw.polygon(
        screen, blue, [(50, 180), (90, 200), (90, 240), (50, 260), (10, 240), (10, 200)]
    )  # hexagon

    # Outlined polygon
    pygame.draw.polygon(
        screen, white, [(200, 100), (280, 100), (300, 150), (240, 200), (180, 150)], 3
    )

    # Animated rotating polygon (pentagon)
    center_x, center_y = 350, 230
    radius = 50
    points = []
    for i in range(5):
        angle = poly_angle + i * (2 * math.pi / 5)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(screen, cyan, points)


def draw_arcs():
    draw_demo_title("pygame.draw.arc()", "draws an arc (portion of ellipse)")

    # Static arcs
    rect1 = pygame.Rect(50, 70, 80, 80)
    pygame.draw.arc(screen, red, rect1, 0, math.pi / 2, 3)
    pygame.draw.arc(screen, green, rect1, math.pi / 2, math.pi, 3)
    pygame.draw.arc(screen, blue, rect1, math.pi, 3 * math.pi / 2, 3)
    pygame.draw.arc(screen, yellow, rect1, 3 * math.pi / 2, 2 * math.pi, 3)

    # Various arc sizes
    pygame.draw.arc(screen, white, pygame.Rect(200, 80, 100, 60), 0, math.pi, 4)
    pygame.draw.arc(screen, cyan, pygame.Rect(200, 160, 60, 100), 0, math.pi * 1.5, 4)

    # Animated arc
    arc_rect = pygame.Rect(300, 200, 80, 80)
    end_angle = circle_angle % (2 * math.pi)
    pygame.draw.arc(screen, orange, arc_rect, 0, end_angle, 5)


def draw():
    demos = [
        draw_circles,
        draw_rectangles,
        draw_lines,
        draw_ellipses,
        draw_polygons,
        draw_arcs,
    ]

    # Show menu if paused
    if paused:
        screen.fill(black)
        title = font.render("Pygame Drawing API Demo", True, white)
        screen.blit(title, (center_text_x(title.get_width(), 0), 30))

        instructions = [
            f"Current demo: {demo_index + 1}/{len(demos)}",
            "Press SPACE to pause/resume demo rotation",
            "Press LEFT/RIGHT to change demo manually",
            "Press R to reset",
        ]

        for i, line in enumerate(instructions):
            text = small_font.render(line, True, cyan)
            screen.blit(text, (center_text_x(text.get_width(), 0), 80 + i * 30))

        # Show preview of current demo
        if paused_demos:
            demos[demo_index % len(demos)]()
    else:
        demos[demo_index % len(demos)]()

        # Show demo indicator
        demo_text = small_font.render(
            f"Demo {demo_index + 1}/{len(demos)}", True, gray(150)
        )
        screen.blit(demo_text, (width - demo_text.get_width() - 10, 10))


def center_text_x(text_width, offset=0):
    return (width - text_width) // 2


def gray(value):
    return (value, value, value)


def reset_game():
    global demo_index, frame_counter, circle_angle, rect_x, poly_angle, line_y, ellipse_scale
    demo_index = 0
    frame_counter = 0
    circle_angle = 0
    rect_x = 0
    poly_angle = 0
    line_y = 0
    ellipse_scale = 1.0


def set_pause(is_paused):
    global paused, paused_demos
    paused = is_paused
    paused_demos = is_paused

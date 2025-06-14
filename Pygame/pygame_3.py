## Projectile motion simulation with angle from vertical
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message
import pygame
import math
import sys

# Get user input
try:
    speed = float(input("Enter initial speed (m/s): "))
    angle_from_vertical = float(input("Enter angle from vertical (degrees, 0=up, 90=horizontal): "))
except:
    speed = 50
    angle_from_vertical = 30

# Convert angle from vertical to radians from horizontal
angle_deg = 90 - angle_from_vertical
angle_rad = math.radians(angle_deg)

# Decompose velocity
vx = speed * math.cos(angle_rad)
vy = speed * math.sin(angle_rad)

# Constants
g = 9.8
dt = 1 / 60

# Theoretical calculations
flight_time = (2 * vy) / g if vy > 0 else 0
range_x = vx * flight_time
max_height = (vy ** 2) / (2 * g) if vy > 0 else 0

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion (Angle from Vertical)")
clock = pygame.time.Clock()

# Colors and Fonts
WHITE = (255, 255, 255)
BG = (20, 20, 40)
AXIS_COLOR = (180, 180, 180)
BALL_COLOR = (255, 100, 100)
PATH_COLOR = (100, 200, 255)
FONT = pygame.font.SysFont("Arial", 20)
TITLE_FONT = pygame.font.SysFont("Arial", 32, bold=True)

# Margins
margin = 60
usable_width = WIDTH - 2 * margin
usable_height = HEIGHT - 2 * margin
scale_x = usable_width / (range_x + 10)
scale_y = usable_height / (max_height + 10)
scale = min(scale_x, scale_y)

origin = (margin, HEIGHT - margin)

def to_screen(x_m, y_m):
    sx = origin[0] + x_m * scale
    sy = origin[1] - y_m * scale
    return int(sx), int(sy)

def draw_axes():
    # X-axis
    pygame.draw.line(screen, AXIS_COLOR, origin, (WIDTH - margin, origin[1]), 2)
    pygame.draw.polygon(screen, AXIS_COLOR, [(WIDTH - margin, origin[1]),
                                             (WIDTH - margin - 10, origin[1] - 5),
                                             (WIDTH - margin - 10, origin[1] + 5)])
    screen.blit(FONT.render("X (m)", True, AXIS_COLOR), (WIDTH - margin + 5, origin[1] - 20))

    # Y-axis
    pygame.draw.line(screen, AXIS_COLOR, origin, (origin[0], margin), 2)
    pygame.draw.polygon(screen, AXIS_COLOR, [(origin[0], margin),
                                             (origin[0] - 5, margin + 10),
                                             (origin[0] + 5, margin + 10)])
    screen.blit(FONT.render("Y (m)", True, AXIS_COLOR), (origin[0] + 10, margin - 10))

    # Tick marks
    for i in range(0, int(range_x) + 10, 10):
        x, y = to_screen(i, 0)
        pygame.draw.line(screen, AXIS_COLOR, (x, y - 5), (x, y + 5))
        label = FONT.render(f"{i}", True, AXIS_COLOR)
        screen.blit(label, (x - label.get_width() // 2, y + 8))

    for i in range(0, int(max_height) + 10, 10):
        x, y = to_screen(0, i)
        pygame.draw.line(screen, AXIS_COLOR, (x - 5, y), (x + 5, y))
        label = FONT.render(f"{i}", True, AXIS_COLOR)
        screen.blit(label, (x - 30, y - 10))

def draw_text_centered(text, x, y, font, color):
    label = font.render(text, True, color)
    screen.blit(label, (x - label.get_width() // 2, y))

# State
x, y = 0.0, 0.0
t = 0.0
path = []
simulation_done = False

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_axes()

    if not simulation_done:
        x = vx * t
        y = vy * t - 0.5 * g * t**2
        if y < 0:
            y = 0
            simulation_done = True
        path.append((x, y))
        t += dt

    for pt in path:
        px, py = to_screen(pt[0], pt[1])
        pygame.draw.circle(screen, PATH_COLOR, (px, py), 2)

    ball_screen = to_screen(x, y)
    pygame.draw.circle(screen, BALL_COLOR, ball_screen, 6)

    # Labels
    draw_text_centered("Projectile Motion Simulation (Angle from Vertical)", WIDTH // 2, 20, TITLE_FONT, WHITE)
    draw_text_centered(f"Speed: {speed:.1f} m/s | Angle from Vertical: {angle_from_vertical:.1f}°", WIDTH // 2, 55, FONT, WHITE)
    draw_text_centered(f"Flight Time: {flight_time:.2f}s | Max Height: {max_height:.2f} m | Range: {range_x:.2f} m",
                       WIDTH // 2, 85, FONT, WHITE)

    pygame.display.flip()

pygame.quit()
sys.exit()

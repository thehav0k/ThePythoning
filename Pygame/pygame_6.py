## Two Object Race Simulation

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message
import pygame
import sys

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Object Race Simulation")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 80)
BLACK = (0, 0, 0)

# Fonts
pygame.font.init()
SMALL_FONT = pygame.font.SysFont("Arial", 16)
FONT = pygame.font.SysFont("Arial", 24)
TITLE_FONT = pygame.font.SysFont("Arial", 32, bold=True)

# Get user input for initial velocity and acceleration
try:
    u1 = float(input("Enter initial velocity for Object 1 (m/s): "))
    a1 = float(input("Enter acceleration for Object 1 (m/s^2): "))
    u2 = float(input("Enter initial velocity for Object 2 (m/s): "))
    a2 = float(input("Enter acceleration for Object 2 (m/s^2): "))
    target_distance = float(input("Enter target distance (meters): "))
except Exception:
    print("Invalid input. Using default values.")
    u1, a1 = 5, 0.5
    u2, a2 = 4, 0.8
    target_distance = 60

# Dynamic scaling to fit the race on screen
left_margin = 50
right_margin = 100
usable_width = WIDTH - left_margin - right_margin
PPM = usable_width / target_distance # Pixels per meter

# Race setup
start_x = left_margin
finish_x = int(start_x + target_distance * PPM)
obj_y1 = HEIGHT // 3
obj_y2 = 2 * HEIGHT // 3
radius = 25

# Initial positions (in meters)
s_m = start_x / PPM
x1_m = s_m
x2_m = s_m

winner = None
paused = False
t = 0  # time in seconds

# Calculate meeting point (if any)
def get_meeting_point(s, u1, a1, u2, a2, target_distance):
    A = 0.5 * (a1 - a2)
    B = u1 - u2
    if abs(A) < 1e-8:
        if abs(B) < 1e-8:
            return None, None  # Always together
        t_meet = None  # Parallel, never meet
    else:
        t_meet = -B / A
        if t_meet <= 0:
            t_meet = None
    if t_meet:
        x_meet = s + u1 * t_meet + 0.5 * a1 * t_meet * t_meet
        if x_meet - s > target_distance:
            return None, None  # Meeting point is beyond finish
        return x_meet, t_meet
    return None, None

x_meet, t_meet = get_meeting_point(s_m, u1, a1, u2, a2, target_distance)

def draw_small_text(text, x, y):
    screen.blit(SMALL_FONT.render(text, True, WHITE), (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    screen.fill(BLACK)
    # Draw finish line
    pygame.draw.line(screen, WHITE, (finish_x, 0), (finish_x, HEIGHT), 4)

    # Draw gridlines for distance (x-axis) only
    grid_color = (60, 60, 60)
    grid_dist_step = max(1, int(target_distance // 10))
    for d in range(0, int(target_distance)+1, grid_dist_step):
        xg = int(start_x + d * PPM)
        pygame.draw.line(screen, grid_color, (xg, 0), (xg, HEIGHT), 1)
        draw_small_text(f"{d}m", xg-10, HEIGHT-18)

    # Draw small info texts for displaying object states
    info_y = 10
    info_x = 10
    draw_small_text(f"Obj1: u = {u1} m/s, a ={a1} m/s²", info_x+100, info_y)
    draw_small_text(f"Obj2: u = {u2} m/s, a = {a2} m/s²", info_x+100, info_y + 20)
    draw_small_text(f"Target: {target_distance} m", info_x+100, info_y + 40)
    draw_small_text("SPACE: Pause/Resume", info_x+420, info_y + 20)
    if x_meet and t_meet:
        draw_small_text(f"Meeting: {x_meet - s_m:.2f} m at t = {t_meet:.2f} s", info_x + 100, info_y + 60)

    # Calculate positions (in meters)
    if not paused and not winner:
        t += 1/60
    x1_m = s_m + u1 * t + 0.5 * a1 * t * t
    x2_m = s_m + u2 * t + 0.5 * a2 * t * t
    # Convert to px
    x1 = int(x1_m * PPM)
    x2 = int(x2_m * PPM)

    # Draw objects
    pygame.draw.circle(screen, RED, (x1, obj_y1), radius)
    pygame.draw.circle(screen, GREEN, (x2, obj_y2), radius)

    # Check for winner
    if not winner:
        if x1 >= finish_x - radius:
            winner = "Object 1 (Red)"
        elif x2 >= finish_x - radius:
            winner = "Object 2 (Green)"

    # Announce winner
    if winner:
        msg = f"Winner: {winner}!"
        screen.blit(TITLE_FONT.render(msg, True, WHITE), (WIDTH//2 - 160, HEIGHT//2 - 30))
        draw_small_text("Press ESC to exit", WIDTH//2 - 80, HEIGHT//2 + 30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)

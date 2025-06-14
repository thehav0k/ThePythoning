## Free Fall Simulation: Earth vs Moon

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message
import pygame
import sys
import math

# Ask user for height
try:
    user_height = float(input("Enter drop height in meters (e.g., 100): "))
    if user_height < 1 or user_height > 10000:
        print("Using default height of 100 meters.")
        user_height = 100
except:
    user_height = 100

grid_gap = int(user_height) // 10  # Gap between grid lines in meters

# Constants
g_earth = 9.8  # m/s^2
g_moon = 1.62  # m/s^2
fps = 60
dt = 1 / fps  # Time step per frame (in seconds)

# Theoretical fall times
t_earth_theory = math.sqrt(2 * user_height / g_earth)
t_moon_theory = math.sqrt(2 * user_height / g_moon)

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("পড়ন্ত বস্তু: পৃথিবী vs চাঁদ")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (15, 15, 30)
EARTH_COLOR = (100, 180, 255)
MOON_COLOR = (200, 200, 200)
FONT_COLOR = (255, 255, 255)
GRID_COLOR = (60, 60, 80)

# Ball settings
radius = 20
earth_x = WIDTH // 4
moon_x = 3 * WIDTH // 4
start_y = 80  # Top margin

# Convert meters to pixels
usable_pixels = HEIGHT - start_y - 100  # Leave bottom space
pixels_per_meter = usable_pixels / user_height

# Object state
earth_y_m, earth_v = 0.0, 0.0
moon_y_m, moon_v = 0.0, 0.0
earth_time, moon_time = 0.0, 0.0
earth_done = False
moon_done = False

# Fonts
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 36, bold=True)

def draw_label_centered(text, x, y, font, color):
    label = font.render(text, True, color)
    screen.blit(label, (x - label.get_width() // 2, y))

def draw_grid_lines():
    for i in range(0, int(user_height) + grid_gap, grid_gap):
        y = start_y + i * pixels_per_meter
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
        label = font.render(f"{i} m", True, (100, 100, 100))
        screen.blit(label, (10, y - 10))

running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    draw_grid_lines()

    # Earth physics
    if not earth_done:
        earth_v += g_earth * dt
        earth_y_m += earth_v * dt
        earth_time += dt
        if earth_y_m >= user_height:
            earth_y_m = user_height
            earth_done = True

    # Moon physics
    if not moon_done:
        moon_v += g_moon * dt
        moon_y_m += moon_v * dt
        moon_time += dt
        if moon_y_m >= user_height:
            moon_y_m = user_height
            moon_done = True

    # Draw objects
    earth_y_px = int(start_y + earth_y_m * pixels_per_meter)
    moon_y_px = int(start_y + moon_y_m * pixels_per_meter)

    pygame.draw.circle(screen, EARTH_COLOR, (earth_x, earth_y_px), radius)
    pygame.draw.circle(screen, MOON_COLOR, (moon_x, moon_y_px), radius)

    # Draw titles
    draw_label_centered("Earth", earth_x, earth_y_px - 50, font, EARTH_COLOR)
    draw_label_centered("Moon", moon_x, moon_y_px - 50, font, MOON_COLOR)

    # Draw times
    if earth_done:
        draw_label_centered(f"Simulated: {earth_time:.2f}s", earth_x, earth_y_px + 30, font, FONT_COLOR)
        draw_label_centered(f"Theoretical: {t_earth_theory:.2f}s", earth_x, earth_y_px + 60, font, FONT_COLOR)

    if moon_done:
        draw_label_centered(f"Simulated: {moon_time:.2f}s", moon_x, moon_y_px + 30, font, FONT_COLOR)
        draw_label_centered(f"Theoretical: {t_moon_theory:.2f}s", moon_x, moon_y_px + 60, font, FONT_COLOR)

    # Draw header
    draw_label_centered(f"Free Fall Simulation (for {user_height} m)", WIDTH // 2, 20, title_font, FONT_COLOR)

    pygame.display.flip()

pygame.quit()
sys.exit()

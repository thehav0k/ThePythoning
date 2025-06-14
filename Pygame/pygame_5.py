## Simple Harmonic Motion Simulation

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message
import pygame
import sys
import math

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Harmonic Motion Simulation")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BALL_COLOR = (255, 100, 100)
PATH_COLOR = (100, 255, 100)

# Unit conversion
PX_PER_METER = 10  # 10 px = 1 meter

# Circle parameters
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250  # in px
LENGTH_M = RADIUS / PX_PER_METER  # in meters
SPEED = 1.0  # radians per second

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)
TITLE_FONT = pygame.font.SysFont("Arial", 32, bold=True)

def draw_text_centered(text, x, y, font, color):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def draw_speed_vector(x, y, speed, scale=0.2):
    # Draws a horizontal arrow representing speed at (x, y)
    arrow_length = int(abs(speed) * scale)
    if speed > 0:
        end_x = x + arrow_length
    else:
        end_x = x - arrow_length
    end_y = y
    pygame.draw.line(screen, (100, 100, 255), (int(x), int(y)), (int(end_x), int(end_y)), 4)
    # Arrowhead
    if speed != 0:
        direction = 1 if speed > 0 else -1
        pygame.draw.polygon(screen, (100, 100, 255), [
            (end_x, end_y),
            (end_x - 10 * direction, end_y - 5),
            (end_x - 10 * direction, end_y + 5)
        ])

def main():
    t = 0
    running = True
    path_points = []
    paused = False
    # Pendulum parameters
    pivot = (WIDTH // 4, 200)  # Left quarter of the screen
    L = RADIUS  # String length in px
    L_m = L / PX_PER_METER  # String length in meters
    theta0 = math.radians(45)  # Max angle (45 degrees)
    energy_points = []  # Store (KE, PE) for graph
    time_points = []    # Store time for graph
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Pause/Resume button area (top right)
                if button_x <= mouse_x <= button_x + button_w and button_y <= mouse_y <= button_y + button_h:
                    paused = not paused

        screen.fill((0, 0, 0))
        # Draw pause/resume button at top right
        button_w, button_h = 120, 40
        button_x, button_y = WIDTH - button_w - 20, 20
        pygame.draw.rect(screen, (80, 80, 255), (button_x, button_y, button_w, button_h), border_radius=10)
        if paused:
            draw_text_centered("Resume", button_x + button_w//2, button_y + button_h//2, FONT, WHITE)
        else:
            draw_text_centered("Pause", button_x + button_w//2, button_y + button_h//2, FONT, WHITE)

        # Pendulum angle (SHM approximation)
        theta = theta0 * math.cos(SPEED * t)
        x = pivot[0] + L * math.sin(theta)
        y = pivot[1] + L * math.cos(theta)
        if not paused:
            path_points.append((x, y))

        # Pendulum speed (tangential velocity)
        velocity_m = -L_m * SPEED * theta0 * math.sin(SPEED * t)  # in m/s
        velocity_px = velocity_m * PX_PER_METER  # in px/s

        # Energies (assuming g = 9.81 m/s^2, mass = 1kg)
        g = 9.81
        m = 1.0
        h = L_m * (1 - math.cos(theta))  # height above lowest point
        KE = 0.5 * m * velocity_m**2
        PE = m * g * h
        if not paused:
            energy_points.append((KE, PE))
            time_points.append(t)
        if len(energy_points) > 400:
            energy_points.pop(0)
            time_points.pop(0)

        # Draw string
        pygame.draw.line(screen, WHITE, pivot, (int(x), int(y)), 3)
        # Draw path (arc)
        for pt in path_points:
            pygame.draw.circle(screen, PATH_COLOR, (int(pt[0]), int(pt[1])), 2)
        # Draw bob
        pygame.draw.circle(screen, BALL_COLOR, (int(x), int(y)), 15)
        # Draw pivot
        pygame.draw.circle(screen, (200, 200, 0), pivot, 8)
        # Draw speed vector (tangent to arc)
        tangent_angle = theta + math.pi/2
        arrow_length = 40  # fixed length for clarity
        vx = math.cos(tangent_angle) * arrow_length
        vy = math.sin(tangent_angle) * arrow_length
        arrow_color = (100, 100, 255)
        pygame.draw.line(screen, arrow_color, (int(x), int(y)), (int(x+vx), int(y+vy)), 4)
        # Arrowhead
        ah_x = x + vx
        ah_y = y + vy
        head_size = 12
        left_angle = tangent_angle + math.radians(150)
        right_angle = tangent_angle - math.radians(150)
        left_x = ah_x + head_size * math.cos(left_angle)
        left_y = ah_y + head_size * math.sin(left_angle)
        right_x = ah_x + head_size * math.cos(right_angle)
        right_y = ah_y + head_size * math.sin(right_angle)
        pygame.draw.polygon(screen, arrow_color, [
            (ah_x, ah_y),
            (left_x, left_y),
            (right_x, right_y)
        ])
        # Labels
        draw_text_centered("Simple Harmonic Motion", WIDTH // 2, 30, TITLE_FONT, WHITE)
        draw_text_centered(f"Max Angle: {math.degrees(theta0):.1f}° | Length: {L_m:.1f} m", WIDTH // 2, 70, FONT, WHITE)
        draw_text_centered(f"Speed: {velocity_m:.2f} m/s", WIDTH // 2, 110, FONT, WHITE)

        # Draw energy graph (right half of screen)
        graph_x = WIDTH // 2 + 40
        graph_y = 350
        graph_w = WIDTH // 2 - 80
        graph_h = 200
        pygame.draw.rect(screen, (50, 50, 50), (graph_x, graph_y, graph_w, graph_h), 0)
        pygame.draw.rect(screen, WHITE, (graph_x, graph_y, graph_w, graph_h), 2)
        if energy_points:
            g = 9.81
            m = 1.0
            max_PE = m * g * L_m * (1 - math.cos(theta0))
            total_energy = max_PE
            if total_energy == 0:
                total_energy = 1
            scale = graph_h / total_energy
            for i in range(1, len(energy_points)):
                # Prevent drawing beyond the graph width
                if i >= 400:
                    break
                x1 = graph_x + int((i-1)/400 * graph_w)
                x2 = graph_x + int(i/400 * graph_w)
                y1_ke = graph_y + graph_h - int(energy_points[i-1][0] * scale * 0.372)
                y2_ke = graph_y + graph_h - int(energy_points[i][0] * scale * 0.372)
                y1_pe = graph_y + graph_h - int(energy_points[i-1][1] * scale)
                y2_pe = graph_y + graph_h - int(energy_points[i][1] * scale)
                pygame.draw.line(screen, (255, 80, 80), (x1, y1_ke), (x2, y2_ke), 2)
                pygame.draw.line(screen, (80, 255, 80), (x1, y1_pe), (x2, y2_pe), 2)
            draw_text_centered("Kinetic (Red) & Potential (Green)", graph_x + graph_w//2, graph_y - 20, FONT, WHITE)

        pygame.display.flip()
        clock.tick(60)
        if not paused:
            t += 1/60

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
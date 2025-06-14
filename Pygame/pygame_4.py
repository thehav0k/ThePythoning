## Plane Collision Simulation with Tower Collapse
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message
import pygame
import sys
import random

try:
    plane_height = float(input("Enter initial flight height of plane in meters (e.g., 150): "))
    if not (10 <= plane_height <= 1000):
        print("Using default height of 125 meters.")
        plane_height = 150
except Exception:
    plane_height = 125

# Constants
WIDTH, HEIGHT = 1000, 600
GROUND_LEVEL = HEIGHT - 50
PIXELS_PER_METER = 2
FPS = 60
EXPLOSION_DURATION = 1.5
EXPLOSION_MAX_RADIUS = 60
SHAKE_INTENSITY = 10
DEBRIS_COUNT = 20
SPARK_COUNT = 30
SMOKE_SPAWN_RATE = 0.05
WIND_SPEED = random.uniform(-5, 5)

# Tower settings
TOWERS = [
    {'x': 600, 'base_height': 60, 'top_height': 60, 'width': 60},
    {'x': 800, 'base_height': 80, 'top_height': 50, 'width': 60},
]

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Collision Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# Colors
WHITE = (255, 255, 255)
TEXT = (0, 0, 0)
RED = (200, 0, 0)
PLANE_COLOR = (30, 60, 140)
TOWER_BASE = (100, 100, 140)
TOWER_TOP = (130, 130, 180)
SKY_TOP = (70, 130, 180)
SKY_BOTTOM = (135, 206, 250)
GROUND_BASE = (100, 80, 50)
GROUND_HIGHLIGHT = (120, 100, 60)
EXPLOSION_COLORS = [(255, 120, 0), (255, 80, 0), (255, 200, 0)]  # Orange, red, yellow
SPARK_COLOR = (255, 255, 200)
SMOKE_COLOR = (80, 80, 80)

# Plane state
plane_x = 0
plane_y = GROUND_LEVEL - plane_height * PIXELS_PER_METER
plane_speed_x = 100
collision = False
explosion_time = 0
explosion_x = 0
explosion_y = 0
screen_shake = 0
smoke_time = 0
restart_button_rect = pygame.Rect(WIDTH - 140, 20, 120, 40)
smoke_trail = []
debris_particles = []
spark_particles = []

collapsed_towers = [False for _ in TOWERS]
collapse_progress = [0.0 for _ in TOWERS]  # 0.0 = upright, 1.0 = fully collapsed
COLLAPSE_DURATION = 2.0  # seconds


class Debris:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-150, 150)
        self.vy = random.uniform(-150, 0)
        self.life = random.uniform(1, 2.2)
        self.size = random.uniform(2, 5)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt
        self.life -= dt

    def draw(self, surface, offset_x, offset_y):
        if self.life > 0:
            pygame.draw.circle(surface, (255, 255, 0), (int(self.x + offset_x), int(self.y + offset_y)), int(self.size))

class Spark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-200, 200)
        self.vy = random.uniform(-200, 50)
        self.life = random.uniform(0.3, 0.7)
        self.size = random.uniform(1, 3)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 100 * dt
        self.life -= dt

    def draw(self, surface, offset_x, offset_y):
        if self.life > 0:
            pygame.draw.circle(surface, SPARK_COLOR, (int(self.x + offset_x), int(self.y + offset_y)), int(self.size))

class Smoke:
    def __init__(self, x, y, is_explosion=False):
        self.x = x + random.uniform(-5, 5)
        self.y = y + random.uniform(-3, 3)
        self.radius = random.uniform(5, 10) if is_explosion else random.uniform(3, 7)
        self.alpha = random.uniform(150, 200) if is_explosion else random.uniform(100, 150)
        self.drift_x = WIND_SPEED * 0.1 + random.uniform(-0.3, 0.3)
        self.rise_speed = random.uniform(-0.5, -1.0) if is_explosion else random.uniform(-0.2, -0.5)
        self.growth = random.uniform(0.3, 0.6) if is_explosion else random.uniform(0.1, 0.4)
        self.color = (
            random.randint(60, 100) if is_explosion else random.randint(80, 120),
            random.randint(60, 100) if is_explosion else random.randint(80, 120),
            random.randint(60, 100) if is_explosion else random.randint(80, 120)
        )

    def update(self):
        self.x += self.drift_x
        self.y += self.rise_speed
        self.radius += self.growth
        self.alpha = max(0, int(self.alpha - (3 if self.radius > 10 else 2)))

    def draw(self, surface, offset_x, offset_y):
        if self.alpha > 0:
            smoke_surface = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surface, (*self.color, int(self.alpha)), (int(self.radius), int(self.radius)), int(self.radius))
            surface.blit(smoke_surface, (self.x - self.radius + offset_x, self.y - self.radius + offset_y))

# Drawing functions
def draw_plane(surface, x, y, offset_x, offset_y, angle=0):
    plane_width, plane_height = 60, 25
    plane_surface = pygame.Surface((plane_width + 20, plane_height + 20), pygame.SRCALPHA)
    pygame.draw.rect(plane_surface, PLANE_COLOR, (10, plane_height // 2 - plane_height // 4, plane_width, plane_height // 2))
    pygame.draw.polygon(plane_surface, PLANE_COLOR, [
        (plane_width // 2, plane_height // 2), (10, plane_height // 2 + plane_height), (10, plane_height // 2 - plane_height)
    ])
    pygame.draw.polygon(plane_surface, PLANE_COLOR, [
        (10, plane_height // 2), (0, plane_height // 2 + plane_height // 2), (0, plane_height // 2 - plane_height // 2)
    ])
    rotated_plane = pygame.transform.rotate(plane_surface, angle)
    surface.blit(rotated_plane, (x - plane_width // 2 + offset_x, y - plane_height // 2 + offset_y))

def draw_explosion(surface, x, y, progress, offset_x, offset_y):
    for i, color in enumerate(EXPLOSION_COLORS):
        radius = int(EXPLOSION_MAX_RADIUS * progress * (1 + i * 0.2)) + random.randint(-5, 5)
        alpha = max(0, int(255 * (1 - progress) - i * 50))
        if radius > 0:
            layer = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(layer, (*color, alpha), (radius, radius), radius)
            surface.blit(layer, (x - radius + offset_x, y - radius + offset_y))
    core_radius = int(EXPLOSION_MAX_RADIUS * 0.3 * (1 - progress))
    if core_radius > 0:
        core = pygame.Surface((core_radius * 2, core_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(core, (255, 255, 255, int(255 * (1 - progress))), (core_radius, core_radius), core_radius)
        surface.blit(core, (x - core_radius + offset_x, y - core_radius + offset_y))

def draw_restart_button(surface, offset_x, offset_y):
    rect = restart_button_rect.move(offset_x, offset_y)
    pygame.draw.rect(surface, (180, 180, 180), rect)
    pygame.draw.rect(surface, TEXT, rect, 2)
    label = font.render("Restart", True, TEXT)
    surface.blit(label, (rect.x + 20, rect.y + 10))

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(SKY_TOP)
    offset_x = random.randint(-int(screen_shake), int(screen_shake)) if screen_shake > 0 else 0
    offset_y = random.randint(-int(screen_shake), int(screen_shake)) if screen_shake > 0 else 0


    for y in range(HEIGHT):
        r = SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * y / HEIGHT
        g = SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * y / HEIGHT
        b = SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * y / HEIGHT
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y + offset_y), (WIDTH, y + offset_y))


    pygame.draw.rect(screen, GROUND_BASE, (0, GROUND_LEVEL + offset_y, WIDTH, HEIGHT - GROUND_LEVEL))
    for x in range(0, WIDTH, 20):
        pygame.draw.rect(screen, GROUND_HIGHLIGHT, (x + offset_x, GROUND_LEVEL + offset_y, 10, 5))


    for idx, tower in enumerate(TOWERS):
        bx = tower['x']
        base_px = tower['base_height'] * PIXELS_PER_METER
        top_px = tower['top_height'] * PIXELS_PER_METER
        by = GROUND_LEVEL - base_px
        ty = by - top_px
        tw = tower['width']
        # Collapse animation: rotate and drop the top part
        if collapsed_towers[idx]:
            collapse_progress[idx] = min(1.0, collapse_progress[idx] + dt / COLLAPSE_DURATION)
            angle = 90 * collapse_progress[idx]  # degrees
            # Draw base (cracked)
            pygame.draw.rect(screen, TOWER_BASE, (bx + offset_x, by + offset_y, tw, base_px))
            # Draw top (falling)
            top_surface = pygame.Surface((tw, top_px), pygame.SRCALPHA)
            pygame.draw.rect(top_surface, TOWER_TOP, (0, 0, tw, top_px))
            rotated = pygame.transform.rotate(top_surface, angle)
            rx, ry = rotated.get_rect(center=(bx + tw // 2 + offset_x, ty + top_px // 2 + offset_y)).topleft
            screen.blit(rotated, (rx, ry))
        else:
            pygame.draw.rect(screen, TOWER_BASE, (bx + offset_x, by + offset_y, tw, base_px))
            pygame.draw.rect(screen, TOWER_TOP, (bx + offset_x, ty + offset_y, tw, top_px))
            for y in range(int(by), int(GROUND_LEVEL), 10):
                pygame.draw.line(screen, (80, 80, 120), (bx + offset_x, y + offset_y), (bx + tw + offset_x, y + offset_y))
            for y in range(int(ty), int(by), 10):
                pygame.draw.line(screen, (110, 110, 160), (bx + offset_x, y + offset_y), (bx + tw + offset_x, y + offset_y))
        label_base = font.render(f"Base: {tower['base_height']} m", True, TEXT)
        label_top = font.render(f"Top: {tower['top_height']} m", True, TEXT)
        screen.blit(label_base, (bx + 5 + offset_x, by - 25 + offset_y))
        screen.blit(label_top, (bx + 5 + offset_x, ty - 25 + offset_y))


    if not collision:
        plane_x += plane_speed_x * dt
        smoke_time += dt
        if smoke_time >= SMOKE_SPAWN_RATE:
            smoke_trail.append(Smoke(plane_x, plane_y + 5))
            smoke_time = 0
        if plane_y > GROUND_LEVEL:
            collision = True
            explosion_time = 0
            explosion_x = plane_x
            explosion_y = plane_y
            screen_shake = SHAKE_INTENSITY
            for _ in range(DEBRIS_COUNT):
                debris_particles.append(Debris(explosion_x, explosion_y))
            for _ in range(SPARK_COUNT):
                spark_particles.append(Spark(explosion_x, explosion_y))
            for _ in range(int(SPARK_COUNT * 0.5)):
                smoke_trail.append(Smoke(explosion_x, explosion_y, is_explosion=True))

    if not collision:
        plane_bottom = plane_y + 10
        for idx, tower in enumerate(TOWERS):
            top_y_px = GROUND_LEVEL - (tower['base_height'] + tower['top_height']) * PIXELS_PER_METER
            if tower['x'] <= plane_x <= tower['x'] + tower['width'] and plane_bottom >= top_y_px:
                collision = True
                explosion_time = 0
                explosion_x = plane_x
                explosion_y = plane_y
                screen_shake = SHAKE_INTENSITY
                collapsed_towers[idx] = True  # Mark this tower to collapse
                for _ in range(DEBRIS_COUNT):
                    debris_particles.append(Debris(explosion_x, explosion_y))
                for _ in range(SPARK_COUNT):
                    spark_particles.append(Spark(explosion_x, explosion_y))
                for _ in range(int(SPARK_COUNT * 0.5)):
                    smoke_trail.append(Smoke(explosion_x, explosion_y, is_explosion=True))
                break

    # Update and draw particles
    if collision:
        explosion_time += dt
        progress = min(1.0, explosion_time / EXPLOSION_DURATION)
        screen_shake = max(0, screen_shake - dt * 20)
        draw_explosion(screen, explosion_x, explosion_y, progress, offset_x, offset_y)
        debris_particles = [d for d in debris_particles if d.life > 0]
        spark_particles = [s for s in spark_particles if s.life > 0]
        for d in debris_particles:
            d.update(dt)
            d.draw(screen, offset_x, offset_y)
        for s in spark_particles:
            s.update(dt)
            s.draw(screen, offset_x, offset_y)
        if progress >= 1.0 and not debris_particles and not spark_particles:
            draw_restart_button(screen, offset_x, offset_y)
    else:
        draw_plane(screen, plane_x, plane_y, offset_x, offset_y)

    # Update and draw smoke trail
    smoke_trail = [s for s in smoke_trail if s.alpha > 0]
    for smoke in smoke_trail:
        smoke.update()
        smoke.draw(screen, offset_x, offset_y)

    # Axes
    pygame.draw.line(screen, TEXT, (0, GROUND_LEVEL + offset_y), (WIDTH, GROUND_LEVEL + offset_y), 2)
    for i in range(0, int(HEIGHT / PIXELS_PER_METER), 50):
        y = GROUND_LEVEL - i * PIXELS_PER_METER
        if y < 0:
            break
        pygame.draw.line(screen, TEXT, (0 + offset_x, y + offset_y), (10 + offset_x, y + offset_y), 2)
        label = font.render(f"{i}m", True, TEXT)
        screen.blit(label, (15 + offset_x, y - 10 + offset_y))

    # Displays
    h = (GROUND_LEVEL - plane_y) / PIXELS_PER_METER
    screen.blit(font.render(f"Plane Altitude: {h:.1f} m", True, TEXT), (80 + offset_x, 20 + offset_y))
    screen.blit(font.render(f"Speed: {plane_speed_x:.1f} m/s", True, TEXT), (80 + offset_x, 50 + offset_y))
    screen.blit(font.render(f"Wind Speed: {WIND_SPEED:.1f} m/s", True, TEXT), (80 + offset_x, 80 + offset_y))

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and collision and explosion_time >= EXPLOSION_DURATION and not debris_particles and not spark_particles:
            if restart_button_rect.collidepoint(event.pos):
                plane_x = 0
                plane_y = GROUND_LEVEL - plane_height * PIXELS_PER_METER
                collision = False
                explosion_time = 0
                screen_shake = 0
                smoke_time = 0
                debris_particles.clear()
                spark_particles.clear()
                smoke_trail.clear()
                for i in range(len(collapsed_towers)):
                    collapsed_towers[i] = False
                    collapse_progress[i] = 0.0

pygame.quit()
sys.exit()


# comment korar energy nai
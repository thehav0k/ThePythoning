import turtle as t
import math

# Setup the screen with romantic colors
screen = t.Screen()
screen.bgcolor("#FFF5F7")  # Soft pink background
screen.title("Romantic Flower")
screen.setup(width=900, height=700)
screen.tracer(False)

# Setup turtle
t.speed(0)
t.hideturtle()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def adjust_color(hex_color, factor=0.85):
    r, g, b = hex_to_rgb(hex_color)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return rgb_to_hex((r, g, b))

# Transform a local point (px, py) to global using origin (cx, cy) and heading (deg)
def transform_point(cx, cy, heading_deg, px, py):
    ang = math.radians(heading_deg)
    cos_a, sin_a = math.cos(ang), math.sin(ang)
    gx = cx + px * cos_a - py * sin_a
    gy = cy + px * sin_a + py * cos_a
    return gx, gy

# Cubic Bézier interpolation
def cubic_bezier(p0, p1, p2, p3, tval):
    u = 1 - tval
    x = (u**3)*p0[0] + 3*(u**2)*tval*p1[0] + 3*u*(tval**2)*p2[0] + (tval**3)*p3[0]
    y = (u**3)*p0[1] + 3*(u**2)*tval*p1[1] + 3*u*(tval**2)*p2[1] + (tval**3)*p3[1]
    return x, y

# Draw one realistic petal using two cubic Bézier curves (left and right halves)
def draw_bezier_petal(base_x, base_y, heading, length_, width_, fill_color, outline=None):
    # Control points in local coordinates
    L = length_
    W = width_
    # Left half: base -> tip
    P0L = (0.0, 0.0)
    P1L = (-0.6*W, 0.18*L)
    P2L = (-0.35*W, 0.75*L)
    P3L = (0.0, L)
    # Right half: tip -> base (we will traverse backward to close shape)
    P0R = (0.0, L)
    P1R = (0.35*W, 0.75*L)
    P2R = (0.6*W, 0.18*L)
    P3R = (0.0, 0.0)

    if outline is None:
        outline = adjust_color(fill_color, 0.7)

    t.pensize(2)
    t.color(outline)
    t.fillcolor(fill_color)

    # Move to base without drawing
    gx, gy = transform_point(base_x, base_y, heading, *P0L)
    t.penup()
    t.goto(gx, gy)
    t.pendown()
    t.begin_fill()

    # Draw left half to tip
    steps = 28
    for i in range(1, steps+1):
        px, py = cubic_bezier(P0L, P1L, P2L, P3L, i/steps)
        gx, gy = transform_point(base_x, base_y, heading, px, py)
        t.goto(gx, gy)

    # Draw right half back to base
    for i in range(1, steps+1):
        px, py = cubic_bezier(P0R, P1R, P2R, P3R, i/steps)
        gx, gy = transform_point(base_x, base_y, heading, px, py)
        t.goto(gx, gy)

    t.end_fill()

# Draw a layered rose: multiple rings of petals, offset and scaled
def draw_rose(center_x, center_y):
    # Colors from outer to inner
    outer = "#F7A1B8"   # soft rose
    mid   = "#F06C9B"   # deeper pink
    inner = "#E73E83"   # rich pink
    core  = "#FFD1DC"   # pale blush

    # Outer ring
    R = 90
    petals = 10
    for i in range(petals):
        ang = i * (360/petals)
        bx = center_x + R * math.cos(math.radians(ang))
        by = center_y + R * math.sin(math.radians(ang)) * 0.85  # slight vertical squash for perspective
        heading = ang
        draw_bezier_petal(bx, by, heading, length_=110, width_=70, fill_color=outer)

    # Mid ring (offset)
    R2 = 55
    petals2 = 8
    for i in range(petals2):
        ang = i * (360/petals2) + 360/(petals2*2)
        bx = center_x + R2 * math.cos(math.radians(ang))
        by = center_y + R2 * math.sin(math.radians(ang)) * 0.9
        heading = ang
        draw_bezier_petal(bx, by, heading, length_=85, width_=55, fill_color=mid)

    # Inner ring
    R3 = 28
    petals3 = 6
    for i in range(petals3):
        ang = i * (360/petals3) + 20
        bx = center_x + R3 * math.cos(math.radians(ang))
        by = center_y + R3 * math.sin(math.radians(ang))
        heading = ang
        draw_bezier_petal(bx, by, heading, length_=60, width_=38, fill_color=inner)

    # Core spiral suggestion (small overlapping petals)
    R4 = 6
    for k in range(7):
        ang = k * 28
        bx = center_x + R4 * math.cos(math.radians(ang))
        by = center_y + R4 * math.sin(math.radians(ang))
        heading = ang + 20
        draw_bezier_petal(bx, by, heading, length_=24, width_=16, fill_color=adjust_color(inner, 0.9))

    # Center
    t.penup()
    t.goto(center_x, center_y-6)
    t.pendown()
    t.color("#D98DA0")
    t.fillcolor(core)
    t.begin_fill()
    t.circle(10)
    t.end_fill()

# Function to draw stem and leaves
def draw_stem(x, y, length):
    t.penup()
    t.goto(x, y)
    t.setheading(270)
    t.pendown()
    t.pensize(8)
    t.color("#4E8C5A")
    t.forward(length)

    # Draw leaves
    stem_y = y - length * 0.45

    # Leaf helper (simple Bézier leaf)
    def leaf_at(bx, by, heading, L=80, W=40, fill="#6FB56F"):
        draw_bezier_petal(bx, by, heading, length_=L, width_=W, fill_color=fill, outline=adjust_color(fill, 0.7))

    # Left leaf
    leaf_at(x - 8, stem_y, 210, L=90, W=45, fill="#6FB56F")
    # Right leaf
    leaf_at(x + 8, stem_y - 10, 330, L=80, W=42, fill="#6FB56F")

# Draw composition
# Place the rose above the stem so the base of petals meets stem top
t.pensize(2)
stem_top_x, stem_top_y = 0, -40
flower_center_x, flower_center_y = 0, 120

draw_stem(stem_top_x, stem_top_y, 260)
draw_rose(flower_center_x, flower_center_y)

# Romantic caption (subtle)
t.penup()
t.goto(0, -310)
t.color("#CC3A6A")
t.write("With Love", align="center", font=("Georgia", 22, "italic"))

screen.update()

# Keep the window open
t.done()

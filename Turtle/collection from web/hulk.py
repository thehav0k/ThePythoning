import os
import turtle as t

# Try to import pywhatkit's ASCII art generator; fall back if unavailable
try:
    from pywhatkit import image_to_ascii_art as sac  # type: ignore
except Exception:  # pywhatkit missing or incompatible
    sac = None

# Resolve paths relative to this script's directory
BASE_DIR = os.path.dirname(__file__)
pic = os.path.join(BASE_DIR, 'img.png')
out_base = os.path.join(BASE_DIR, 'hulk')  # Will correspond to out_base + '.txt'
ascii_path = out_base + '.txt'

# Generate ASCII art only if the tool is available and output doesn't already exist
if sac is not None and not os.path.exists(ascii_path):
    if os.path.exists(pic):
        sac(pic, out_base)
    else:
        if not os.path.exists(ascii_path):
            raise FileNotFoundError(f"Source image not found: {pic}")

# Spacing constants
STEP_X = 4  # horizontal spacing per character
STEP_Y = 8  # vertical spacing per line

# Initial drawing origin
a_x = -170
a_y = 350

p = t.Pen()
t.setup(430, 768)
t.bgcolor('black')
# Speed up drawing: turn off animation and hide turtle
try:
    t.tracer(0, 0)
except Exception:
    try:
        t.tracer(False)
    except Exception:
        pass
p.hideturtle()
p.speed(0)
p.up()
p.width(3)


def color_of(c: str) -> str:
    # Map ASCII luminance symbols to colors; default to black for unknowns
    sym = {
        '.': 'green',
        'S': 'black', '#': 'black', '&': 'black', '@': 'black', '$': 'black', '%': 'black', '!': 'black', ':': 'black', '*': 'black',
        '?': 'black', '+': 'black', ';': 'black', ',': 'black', ' ': 'black', '\t': 'black'
    }
    return sym.get(c, 'black')


def draw_line(line: str, y: int) -> None:
    # Draw contiguous runs of the same visible color as single strokes
    n = len(line)
    col = 0
    p.setheading(0)
    while col < n:
        ch = line[col]
        if ch == '\n':
            break
        col_color = color_of(ch)
        if col_color == 'black':
            col += 1
            continue
        # start a run of this color
        start_col = col
        col += 1
        while col < n:
            ch2 = line[col]
            if ch2 == '\n':
                break
            c2 = color_of(ch2)
            if c2 != col_color:
                break
            col += 1
        run_len = col - start_col
        # position and draw once for the whole run
        x_start = a_x + STEP_X * start_col
        p.up()
        p.pencolor(col_color)
        p.goto(x_start, y)
        p.down()
        p.forward(STEP_X * run_len)
        p.up()


# Read the ASCII file (must exist either pre-generated or via pywhatkit)
if not os.path.exists(ascii_path):
    raise FileNotFoundError(
        f"ASCII art file not found: {ascii_path}. Install pywhatkit or provide this file.")

with open(ascii_path, 'r', encoding='utf-8') as text:
    te = text.readlines()

# Render each line using batched strokes
y = a_y
for line in te:
    draw_line(line, y)
    y -= STEP_Y

# Update once at the end if tracer disabled
try:
    t.update()
except Exception:
    pass


t.done()
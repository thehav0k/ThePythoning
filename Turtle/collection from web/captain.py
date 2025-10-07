import turtle
import math

# Create a turtle object
ca = turtle.Turtle()

def func_1(x, y):
    """Move the turtle to the given coordinates and set up initial configuration"""
    ca.penup()
    ca.goto(x, y)
    ca.pendown()
    ca.setheading(0)
    ca.pensize(2)
    ca.speed(10)

def circle(r, color):
    """Draw a circle of the given radius and color"""
    x_point = 0
    y_pont = -r
    func_1(x_point, y_pont)
    ca.pencolor(color)
    ca.fillcolor(color)
    ca.begin_fill()
    ca.circle(r)
    ca.end_fill()

def star(r, color):
    """Draw a star of the given radius and color"""
    func_1(0, 0)
    ca.pencolor(color)
    ca.setheading(162)
    ca.forward(r)
    ca.setheading(0)
    ca.fillcolor(color)
    ca.begin_fill()
    for i in range(5):
        ca.forward(math.cos(math.radians(18)) * 2 * r)  # 2cos18°*r
        ca.right(144)
    ca.end_fill()
    ca.hideturtle()

if __name__ == '__main__':
    # Draw concentric circles with different colors
    circle(288, 'crimson')
    circle(234, 'snow')
    circle(174, 'crimson')
    circle(114, 'blue')

    # Draw a star inside the innermost circle
    star(114, 'snow')

    # Finish drawing and keep the window open
    turtle.done()
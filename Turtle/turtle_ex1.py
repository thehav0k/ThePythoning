import turtle as t

# drawing simple 3D cube
t.bgcolor("black")
t.pensize(3)
t.speed(3)

# Draw front face
t.pencolor("cyan")
for _ in range(4):
    t.forward(100)
    t.left(90)

# Move to back face position (create 3D depth effect)
t.penup()
t.goto(30, 30)
t.pendown()

# Draw back face
t.pencolor("magenta")
for _ in range(4):
    t.forward(100)
    t.left(90)

# Connect front and back faces with edges
t.pencolor("yellow")
# Bottom-left corner
t.penup()
t.goto(0, 0)
t.pendown()
t.goto(30, 30)

# Bottom-right corner
t.penup()
t.goto(100, 0)
t.pendown()
t.goto(130, 30)

# Top-right corner
t.penup()
t.goto(100, 100)
t.pendown()
t.goto(130, 130)

# Top-left corner
t.penup()
t.goto(0, 100)
t.pendown()
t.goto(30, 130)

t.hideturtle()
t.done()

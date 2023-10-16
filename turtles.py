import turtle
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DOT_SIZE = 10
MAX_CONNECTION_DISTANCE = 100

screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.bgcolor("black")

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

dots = [turtle.Turtle() for _ in range(50)]

for dot in dots:
    dot.shape("circle")
    dot.color("white")
    dot.penup()
    dot.speed(0)
    dot.goto(random.randint(-SCREEN_WIDTH/2, SCREEN_WIDTH/2), random.randint(-SCREEN_HEIGHT/2, SCREEN_HEIGHT/2))
    dot.velocity = (random.uniform(-2, 2), random.uniform(-2, 2))

while True:
    for dot in dots:
        x, y = dot.pos()
        
        x += dot.velocity[0]
        y += dot.velocity[1]

        if x > SCREEN_WIDTH / 2:
            x = -SCREEN_WIDTH / 2
        if x < -SCREEN_WIDTH / 2:
            x = SCREEN_WIDTH / 2
        if y > SCREEN_HEIGHT / 2:
            y = -SCREEN_HEIGHT / 2
        if y < -SCREEN_HEIGHT / 2:
            y = SCREEN_HEIGHT / 2

        dot.goto(x, y)

        for other_dot in dots:
            if dot != other_dot:
                dist = distance(dot.pos(), other_dot.pos())
                if dist < MAX_CONNECTION_DISTANCE:
                    turtle.pendown()
                    turtle.color("white")
                    turtle.goto(dot.pos())
                    turtle.goto(other_dot.pos())
                    turtle.penup()
                    turtle.hideturtle()

turtle.done()

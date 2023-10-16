from turtle import width
import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DOT_SIZE = 6
DOT_COLOR = (255, 255, 255)
LINE_COLOR = (255, 255, 255)
MAX_CONNECTION_DISTANCE = 150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connected Dots")

def random_position():
    return (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

dots = [{'pos': random_position(), 'velocity': [random.uniform(-1, .5), random.uniform(-1, .5)]} for _ in range(90)]

# for i in range(50):
#     dots.append({'pos': random_position(),'velocity': (random.uniform(-1, .5), random.uniform(-1, .5)) })

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for dot in dots:
        x, y = dot['pos']

        pygame.draw.circle(screen, DOT_COLOR, (int(x), int(y)), DOT_SIZE)

        x += dot['velocity'][0]
        y += dot['velocity'][1]

        if x < 0 or x > 1920:
            dot['velocity'][0] *= -1
        if y < 0 or y > 1080:
            dot['velocity'][1] *= -1

        dot['pos'] = (x, y)

        for other_dot in dots:
            if dot != other_dot:
                dist = distance(dot['pos'], other_dot['pos'])
                if dist < MAX_CONNECTION_DISTANCE:
                    pygame.draw.line(screen, LINE_COLOR, (int(x), int(y),), (int(other_dot['pos'][0]), int(other_dot['pos'][1]),), width=1)

    pygame.display.flip()

pygame.quit()

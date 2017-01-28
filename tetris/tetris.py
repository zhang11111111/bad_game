import pygame
import sys
import random
from pygame.locals import *


pygame.init()
displaySurf = pygame.display.set_mode((280, 500))
pygame.display.set_caption("tetris")
fallingSurface = pygame.Surface((240, 400))
backSurface = pygame.Surface((280, 500))
moveDirection = "down"
touched = False
land = False

FPS = 7
fpsClock = pygame.time.Clock()

shapes = {1: "o", 2: "s", 3: "z", 4: "i", 5: "l", 6: "j", 7: "t"}
xExtend = {"o": 1, "s": 2, "z": 2, "i": 0, "l": 1, "j": 1, "t": 2}
yExtend = {"o": 1, "s": 1, "z": 1, "i": 3, "l": 2, "j": 2, "t": 1}
lowestValue = {"o": (1, 1, -1), "s": (1, 1, 0), "z": (0, 1, 1), "i": (3, -1, -1), "l": (2, 2, -1), "j": (2, 2, -1), "t": (0, 1, 0)}

white = (255, 255, 255)
black = (  0,   0,   0)
grey  = (127, 127, 127)

fallingSurface.fill(white)
backSurface.fill(black)

shapeY = 0
shapeX = 120
dropping_shape = True
current_shape = "z"


shape = pygame.draw.rect(displaySurf, grey, (120, 20, 20, 20))


def draw_shape(y, x, colour):
    if current_shape == "o":
        pygame.draw.rect(fallingSurface, colour, (x, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y, 20, 20))
    elif current_shape == "s":
        pygame.draw.rect(fallingSurface, colour, (x + 20, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 40, y, 20, 20))
    elif current_shape == "z":
        pygame.draw.rect(fallingSurface, colour, (x, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 40, y + 20, 20, 20))
    elif current_shape == "i":
        pygame.draw.rect(fallingSurface, colour, (x, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 40, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 60, 20, 20))
    elif current_shape == "l":
        pygame.draw.rect(fallingSurface, colour, (x, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 40, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 40, 20, 20))
    elif current_shape == "j":
        pygame.draw.rect(fallingSurface, colour, (x + 20, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 20, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 40, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x, y + 40, 20, 20))
    elif current_shape == "t":
        pygame.draw.rect(fallingSurface, colour, (x, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 40, y, 20, 20))
        pygame.draw.rect(fallingSurface, colour, (x + 20, y + 20, 20, 20))


def drop_shape(a, b):
    redraw = pygame.PixelArray(fallingSurface)
    for i in range(0, 12):
        for o in range(0, 20):
            if fallingSurface.get_at((i * 20, o * 20)) != (155, 0, 0, 255):
                for p in range(0, 20):
                    for q in range(0, 20):
                        redraw[i * 20 + q][o * 20 + p] = white

    del redraw
    draw_shape(a, b, grey)


def stack(x, y):
    draw_shape(y, x, (155, 0, 0))


def landed(x, y):
    for i in range(0, 2):
        if lowestValue[current_shape][i] == -1:
            pass
        else:
            xx = (x + 20 * i)
            yy = (y + (20 * lowestValue[current_shape][i]))
            if yy < 400:
                color = fallingSurface.get_at((xx, yy))
                if color != (155, 0, 0, 255):
                    pass
                else:
                    return True
    return False


def check_rows():
    for Yaxis in range(380, -20, -20):
        full_row = True
        for Xaxis in range(0, 240, 20):
            if fallingSurface.get_at((Xaxis, Yaxis)) == (155, 0, 0, 255) and full_row is True:
                pass
            else:
                full_row = False
        if full_row:
            drop_rows(Yaxis)


def drop_rows(ycoord):
    rowdown = pygame.PixelArray(fallingSurface)
    for Yaxis in range(ycoord, 20):
        for Xaxis in range(0, 12):
            if Yaxis * 20 == 400:
                colour = white
            else:
                colour = fallingSurface.get_at((Xaxis * 20, Yaxis * 20 + 20))
            for p in range (20):
                for q in range(20):
                    rowdown[Xaxis + p][Yaxis + q] = colour
    del rowdown

while True:
    if not dropping_shape:
        if fallingSurface.get_at((120, 20)) == (155, 0, 0, 255):
            break
        else:
            drop_shape(shapeY, shapeX)
            current_shape = shapes[random.randint(1, 7)]
            dropping_shape = True
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveDirection = "left"
            elif event.key == pygame.K_RIGHT:
                moveDirection = "right"
            else:
                moveDirection = "down"
    if dropping_shape:
        if moveDirection == "left" and not touched:
            if shapeX > 0:
                shapeX -= 20
                drop_shape(shapeY, shapeX)
        elif moveDirection == "right":
            if shapeX < (220 - (xExtend[current_shape] * 20)) and not touched:
                shapeX += 20
                drop_shape(shapeY, shapeX)
        else:
            land = landed(shapeX, shapeY+20)
            if land:
                stack(shapeX, shapeY)
                dropping_shape = False
                shapeX = 120
                shapeY = 0
            elif shapeY < (380 - (yExtend[current_shape] * 20)):
                shapeY += 20
                drop_shape(shapeY, shapeX)
            else:
                stack(shapeX, shapeY)
                dropping_shape = False
                shapeX = 120
                shapeY = 0
    check_rows()
    moveDirection = "down"
    displaySurf.blit(fallingSurface, (20, 20))
    pygame.display.update()
    fpsClock.tick(FPS)

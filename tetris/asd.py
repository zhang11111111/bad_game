#Need to do
# Generate shapes 4 days to 21
# Clear rows 4 days to 25
# Rotation 5 days to 30
import pygame
import sys
import random
from pygame.locals import *

boardCoordinates = (0, 0)
pygame.init()
display = pygame.display.set_mode((280, 500))
pygame.display.set_caption("tetris")
fallingSurface = pygame.Surface((240, 400))
backSurface = pygame.Surface((280, 500))
FPS = 4
fpsClock = pygame.time.Clock()
current_shape = "s1"
dropping_shape = False
touched = False
land = False
r_blocked = False
l_blocked = False
rotation_blocked = False
moveDirection = "down"
x_value = 0
y_value = 0
shapes = {1: "o", 2: "s", 3: "z", 4: "i", 5: "l", 6: "j", 7: "t"}
o_shape = {0: ((0, 0), (0, 1), (1, 0), (1, 1)),
           1: ((0, 0), (0, 1), (1, 0), (1, 1)),
           2: ((0, 0), (0, 1), (1, 0), (1, 1)),
           3: ((0, 0), (0, 1), (1, 0), (1, 1))}
i_shape = {0: ((0, 0), (0, 1), (0, 2), (0, 3)),
           1: ((0, 0), (1, 0), (2, 0), (3, 0)),
           2: ((0, 0), (0, 1), (0, 2), (0, 3)),
           3: ((0, 0), (1, 0), (2, 0), (3, 0))}
s_shape = {0: ((1, 0), (0, 1), (1, 1), (2, 0)),
           1: ((0, 0), (0, 1), (1, 1), (1, 2)),
           2: ((1, 0), (0, 1), (1, 1), (2, 0)),
           3: ((0, 0), (0, 1), (1, 1), (1, 2))}
z_shape = {0: ((0, 0), (1, 0), (1, 1), (2, 1)),
           1: ((1, 0), (1, 1), (0, 1), (0, 2)),
           2: ((0, 0), (1, 0), (1, 1), (2, 1)),
           3: ((1, 0), (1, 1), (0, 1), (0, 2))}
l_shape = {0: ((0, 0), (0, 1), (0, 2), (1, 2)),
           1: ((0, 0), (0, 1), (1, 0), (2, 0)),
           2: ((0, 0), (1, 0), (1, 1), (1, 2)),
           3: ((2, 0), (2, 1), (1, 1), (0, 1))}
j_shape = {0: ((0, 2), (1, 0), (1, 1), (1, 2)),
           1: ((0, 0), (0, 1), (1, 1), (2, 1)),
           2: ((0, 0), (1, 0), (0, 1), (0, 2)),
           3: ((0, 0), (1, 0), (2, 0), (2, 1))}
t_shape = {0: ((0, 0), (0, 1), (0, 2), (1, 1)),
           1: ((1, 0), (0, 1), (1, 1), (1, 2)),
           2: ((1, 0), (0, 1), (1, 1), (2, 1)),
           3: ((0, 0), (0, 1), (1, 1), (0, 2))}
shapeX = 5
shapeY = 0
white = (255, 255, 255, 255)
black = (  0,   0,   0, 255)
grey  = (127, 127, 127, 255)
red   = (125,   0,   0, 255)


def draw_shape(x, y, colour):
    form = int(current_shape.lstrip("osziljt"))
    block = shape_dict[form]
    for a in block:
        x_value = convert(x + a[0])
        y_value = convert(y + a[1])
        pygame.draw.rect(fallingSurface, colour, (x_value, y_value, 20, 20))


def drop_shape(a, b):
    redraw = pygame.PixelArray(fallingSurface)
    for k in range(0, 12):
        for p in range(0, 20):
            x_value = convert(k)
            y_value = convert(p)
            if fallingSurface.get_at((x_value, y_value)) != red:
                for w in range(0, 20):
                    for q in range(0, 20):
                        redraw[x_value + q][y_value + w] = white
    del redraw
    draw_shape(a, b, grey)


def landed(x, y):
    form = int(current_shape.lstrip("osziljt"))
    block = shape_dict[form]
    for f in block:
        x_value = convert(x + f[0])
        y_value = convert(y + f[1])
        if y_value + 20 > 380:
            return True
        colour = fallingSurface.get_at((x_value, y_value + 20))
        if colour != white and colour != grey:
            return True
    return False


def convert(coord):
    return coord * 20


def make_shape():
    next_shape = shapes[random.randint(1, 7)]
    next_shape += str(random.randint(0, 3))
    return next_shape


def stack(x, y):
    draw_shape(x, y, red)


def check_rows():
    completed_rows = []
    for y in range(20):
        for x in range(12):
            block = fallingSurface.get_at((convert(x), convert(y )))
            if block != red:
                break
            if x == 11:
                completed_rows.append(y)

    return completed_rows


def clear_rows(completed_rows):
    rows = len(completed_rows)
    print(rows)
    if rows == 0:
        return
    redraw = pygame.PixelArray(fallingSurface)
    for y in range(20, rows, -1):
        for x in range(12, 0, -1):
            block = fallingSurface.get_at((convert(x), convert(y - rows)))
            if x in completed_rows:
                colour = white
            else:
                colour = block
            for p in range(20):
                for q in range(20):
                    redraw[convert(x) + p][convert(y) + q] = colour
    for y in range(convert(rows)):
        for x in range(240):
            redraw[x][y] = white
    del redraw


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveDirection = "left"
            elif event.key == pygame.K_RIGHT:
                moveDirection = "right"
            elif event.key == pygame.K_UP:
                moveDirection = "rotate"
            else:
                moveDirection = "down"
    if dropping_shape:
        form = int(current_shape.lstrip("osziljt"))
        if moveDirection == "left":
            for f in shape_dict[form]:
                x_value = shapeX + int(f[0])
                y_value = shapeY + int(f[1])
                if shapeX < 1:
                    l_blocked = True
                    break
                elif fallingSurface.get_at((convert(x_value - 1), convert(y_value))) == red:
                    l_blocked = True
                    break
            if not l_blocked:
                shapeX -= 1
                drop_shape(shapeX, shapeY)
        elif moveDirection == "right":
            for f in shape_dict[form]:
                x_value = shapeX + int(f[0])
                y_value = shapeY + int(f[1])
                if x_value > 10:
                    r_blocked = True
                    break
                elif fallingSurface.get_at((convert(x_value + 1), convert(y_value))) == red:
                    r_blocked = True
                    break
            if not r_blocked:
                shapeX += 1
                drop_shape(shapeX, shapeY)
        elif moveDirection == "down":
            land = landed(shapeX, shapeY)
            if land:
                stack(shapeX, shapeY)
                dropping_shape = False
                shapeX = 5
                shapeY = 0
            else:
                shapeY += 1
                drop_shape(shapeX, shapeY)
        elif moveDirection == "rotate":
            if form == 3:
                new_form = 0
            else:
                new_form = form + 1
            for a in shape_dict[new_form]:
                x_value = convert(shapeX + a[0])
                y_value = convert(shapeY + a[1])
                if x_value > 220 or y_value > 380:
                    rotation_blocked = True
                    break
                block_location = fallingSurface.get_at((x_value, y_value))
                if block_location != white and block_location != grey:
                    rotation_blocked = True
            if not rotation_blocked:
                form = new_form
                current_shape = current_shape.rstrip("0123") + str(new_form)
                drop_shape(shapeX, shapeY)
            rotation_blocked = False
    else:
        asd = check_rows()
        clear_rows(asd)
        dropping_shape = True
        current_shape = make_shape()
        shape = current_shape.rstrip("0123")
        if shape == "o":
            shape_dict = o_shape
        elif shape == "s":
            shape_dict = s_shape
        elif shape == "z":
            shape_dict = z_shape
        elif shape == "i":
            shape_dict = i_shape
        elif shape == "l":
            shape_dict = l_shape
        elif shape == "j":
            shape_dict = j_shape
        elif shape == "t":
            shape_dict = t_shape
        drop_shape(5, 0)
    display.blit(fallingSurface, (20, 20))
    pygame.display.update()
    r_blocked = False
    l_blocked = False
    moveDirection = "down"
    fpsClock.tick(FPS)
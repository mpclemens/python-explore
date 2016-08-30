#!/usr/bin/env python3
"""Exploring drawing walls and a background/floor for an interactive game"""

import random
import tkinter

WALLSIZE = 32   # pixel size for each wall block
FLOORSIZE = 64  # ditto for the floor tiling (floor is a multiple of the walls)
SCALE = 20      # how big to draw the board

# overall window sizing
WIDTH = WALLSIZE * SCALE
HEIGHT = WALLSIZE * SCALE

tk = tkinter.Tk()
canvas = tkinter.Canvas(tk, width=WIDTH, height=HEIGHT)
canvas.pack()

# elements to display
floor = tkinter.PhotoImage(file="./img/floor.gif")
walls = []

# floor tiling
def draw_floor(canvas):
    """Params: (canvas)
    
    canvas: reference to the Tk canvas"""

    for x in range(0,WIDTH,FLOORSIZE):
        for y in range(0,HEIGHT,FLOORSIZE):
            canvas.create_image(x, y,
                                image=floor,
                                anchor=tkinter.NW)


# wall drawing
def random_wall():
    if 0 == len(walls):
        walls.append(tkinter.PhotoImage(file="./img/wall1.gif"))
        walls.append(tkinter.PhotoImage(file="./img/wall2.gif"))
        walls.append(tkinter.PhotoImage(file="./img/wall3.gif"))
        walls.append(tkinter.PhotoImage(file="./img/wall4.gif"))
        walls.append(tkinter.PhotoImage(file="./img/wall5.gif"))
    return random.choice(walls)

def put_wall(canvas, x, y):
    """Params: (canvas, x, y)
    
    canvas: reference to the Tk canvas
    x, y: game coords, which will be scaled for placement (0,0), (1,0), etc"""

    canvas.create_image(x*WALLSIZE, y*WALLSIZE,
                        image=random_wall(),
                        anchor=tkinter.NW)

draw_floor(canvas)

# draw random walls
for x in range(SCALE):
    for y in range(SCALE):
        if (x % 3 or y % 3):
            pass
        else:
            put_wall(canvas, x, y)
    
tkinter.mainloop()
    

#!/usr/bin/env python3
"""Basic player control, wall/collision sensing, and goal reaching"""

import random
import time

from World import World
from Level import Level
from Player import Player

world = World()
tk = world.root # xxx replace with a world.refresh()-ish method later

level = Level(world)

world.set_level(level) # with the idea that many levels could be established in advance
level.draw_floor()

# outer box of walls
for x in range(world.scale()):
    for y in [0, world.scale()-1]:
        level.put_wall(x, y)
        level.put_wall(y, x)

# some interior walls

for x in range(2, world.scale() ,3):
    for y in range(2, world.scale(), 3):
        level.put_wall(x, y)
        level.put_wall(y, x)

# goal in the bottom right
level.put_goal(world.scale() - 2, world.scale() - 2)

p = Player(world)
game_over = False

while not game_over:
    world.refresh()
    time.sleep(0.1)

    if ((p.x, p.y) in level.goals):
        game_over = True

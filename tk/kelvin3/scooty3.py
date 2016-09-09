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
tk.update() # xxx: world refresh() here

game_over = False

while not game_over:
    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)

    if (p.facing_point() in level.goals):
        p.step_facing()
        tk.update()
        game_over = True
    elif (p.facing_point() in level.walls or
          p.facing in [world.NE(), world.SE(), world.SW(), world.NW()]):
        p.turn_toward(random.choice(Player.DIRECTIONS))
    elif (random.randint(0,100) > 90):
        p.turn_toward(random.choice(Player.DIRECTIONS))
    else:
        p.step_facing()

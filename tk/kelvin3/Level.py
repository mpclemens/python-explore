#!/usr/bin/env python3

import random

class Level:

    def __init__(self, world):
        self.world = world
        self.walls = set()
        self.goals = set()

    # floor tiling
    def draw_floor(self, tile = 0):
        """Draw the specified floor tile on the world's canvas"""

        tiles = self.world.floor_tiles()

        for x in range(0, self.world.width(), self.world.tile_size()):
            for y in range(0, self.world.height(), self.world.tile_size()):
                self.world.canvas.create_image(x, y,
                                               image=tiles[tile],
                                               anchor=self.world.NW())

    # wall drawing
    def put_wall(self, x, y):
        """Draw a wall at the game x,y and remember the location"""

        # Don't bother overdrawing existing walls
        if (x,y) in self.walls:
            return

        icons = self.world.wall_icons();
        
        self.walls.add((x,y))
        self.world.canvas.create_image(x*self.world.icon_size(), y*self.world.icon_size(),
                                       image=random.choice(icons),
                                       anchor=self.world.NW())

    # goal drawing
    def put_goal(self, x, y):
        """Draw a goal at the game x,y and remember the location"""

        # No goals allowed on walls
        if (x,y) in self.walls:
            return

        # Don't overdraw existing goals
        if (x,y) in self.goals:
            return

        icons = self.world.goal_icons();

        self.goals.add((x,y))
        self.world.canvas.create_image(x*self.world.icon_size(), y*self.world.icon_size(),
                                       image=icons[0],
                                       anchor=self.world.NW())



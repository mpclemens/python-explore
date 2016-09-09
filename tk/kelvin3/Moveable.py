#!/usr/bin/env python3

import time

class Moveable:
    """Base class for icons on the lavel that can move, including players and enemies"""

    DIRECTIONS = [] # ordered list of compass points (N, NE, etc.)
    
    def __init__(self, world, icons, facing=None, x=None, y=None):
        """Pass:
        world:  reference to the global game world
        icons:  a dictionary of initialized compass direction-keyed icons
        facing: optional compass direction
        x,y:    optional starting coordinates in world scheme (0,world.scale() - 1)
        """
        
        self.world  = world
        self.icons  = icons
        self.facing = facing
        self.x = x
        self.y = y

        if len(Moveable.DIRECTIONS) == 0:
            Moveable.DIRECTIONS = [world.N(), world.NE(), world.E(), world.SE(),
                                   world.S(), world.SW(), world.W(), world.NW()]

        if facing in icons.keys():
            self.icon = world.canvas.create_image(x*world.icon_size(),
                                                  y*world.icon_size(),
                                                  image=icons[facing],
                                                  anchor=world.NW())

    def turn_toward(self, direction):
        """Orient towards the given direction, cycling through the direction-indexed icons"""

        if direction not in Moveable.DIRECTIONS:
            return

        if self.facing == direction:
            return

        # Pick the shortest turn to face the new direction. The
        # DIRECTIONS array is set up as the consecutive directions to
        # turn right. If the target is more than four turns from the
        # current direction, then wrap around the end of the array to
        # reach the target.
        #
        # Example:
        # DIRECTIONS: [N, NE, E, SE, S, SW, W, NW]
        #
        # If the moveable is facing N and wants to face SW, then the
        # shortest route is counter-clockwise off the bottom of the
        # list and wrapping to the top: N -> NW -> W -> SW

        current_index = Moveable.DIRECTIONS.index(self.facing)
        target_index  = Moveable.DIRECTIONS.index(direction)

        if (target_index > current_index):
            if (target_index - current_index <= 4):
                # clockwise turn
                self._turn_until(current_index, direction, 1)
            else:
                # counter-clockwise turn, off the low end of the array
                self._turn_until(current_index, direction, -1)
        else:
            if (current_index - target_index <= 4):
                # counter-clockwise turn
                self._turn_until(current_index, direction, -1)
            else:
                # clockwise turn, off the high end of the array
                self._turn_until(current_index, direction, -1)
            
    def _turn_until(self, current_index, target_direction, increment):
        """Animate the turn"""
        while self.facing != target_direction:
            time.sleep(0.1) # xxx replace with a call to refresh the world
            current_index = (current_index + increment) % 8
            self.facing = Moveable.DIRECTIONS[current_index]

            if self.facing in self.icons.keys():
                self.world.canvas.itemconfig(self.icon, image=self.icons[self.facing])

    def step_facing(self):
        """Move one step in the current direction, if it is not diagonally"""

        if self.facing == self.world.N():
            self.world.canvas.move(self.icon, 0, -self.world.icon_size())
            self.y -= 1
        elif self.facing == self.world.E():
            self.world.canvas.move(self.icon, self.world.icon_size(), 0)
            self.x += 1
        elif self.facing == self.world.W():
            self.world.canvas.move(self.icon, -self.world.icon_size(), 0)
            self.x -= 1
        elif self.facing == self.world.S():
            self.world.canvas.move(self.icon, 0, self.world.icon_size())
            self.y += 1
        else:
            # No diagonal moves allowed
            pass

    def facing_point(self):
        """Return the coordinates of the space the object is facing"""

        if self.facing == self.world.N():
            return((self.x, self.y-1))
        elif self.facing == self.world.NE():
            return((self.x+1, self.y-1))
        elif self.facing == self.world.E():
            return((self.x+1, self.y))
        elif self.facing == self.world.SE():
            return((self.x+1, self.y+1))
        elif self.facing == self.world.S():
            return((self.x, self.y+1))
        elif self.facing == self.world.SW():
            return((self.x-1, self.y+1))
        elif self.facing == self.world.W():
            return((self.x-1, self.y))
        elif self.facing == self.world.NW():
            return((self.x-1, self.y-1))
        else:
            pass

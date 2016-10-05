#!/usr/bin/env python3

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
                self._turn_until(current_index, direction, 1)
            
    def _turn_until(self, current_index, target_direction, increment):
        """Animate the turn"""
        while self.facing != target_direction:
            self.world.refresh()
            current_index = (current_index + increment) % 8
            self.facing = Moveable.DIRECTIONS[current_index]

            if self.facing in self.icons.keys():
                self.world.canvas.itemconfig(self.icon, image=self.icons[self.facing])

    def facing_point(self):
        """Return the coordinate that the current instance is facing"""

        facing_x = self.x
        facing_y = self.y

        if self.facing in [self.world.NW(), self.world.W(), self.world.SW()]:
            facing_x -= 1

        if self.facing in [self.world.NE(), self.world.E(), self.world.SE()]:
            facing_x += 1

        if self.facing in [self.world.NW(), self.world.N(), self.world.NE()]:
            facing_y -= 1

        if self.facing in [self.world.SW(), self.world.S(), self.world.SE()]:
            facing_y += 1

        return (facing_x, facing_y)

            
    def step_facing(self):
        """Move one step in the current direction, if it is not diagonally"""        

        # diagonal steps are not allowed
        if self.facing not in [self.world.N(), self.world.E(), self.world.S(), self.world.W()]:
            return
        
        new_xy = (new_x, new_y) = self.facing_point()

        if new_xy in self.world.level.walls:
            return

        for step in range(self.world.icon_size()):
            self.world.canvas.move(self.icon, new_x - self.x, new_y - self.y)
            self.world.refresh()

        self.x = new_x
        self.y = new_y


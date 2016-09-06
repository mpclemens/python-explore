#!/usr/bin/env python3
"""Basic player control, wall/collision sensing, and goal reaching"""

###

import tkinter

class World:

    ICONSIZE = 32            # pixel size for each game icon (sprite)
    TILESIZE = ICONSIZE * 2  # pixel size of the floor tiles
    SCALE = 20               # length & width of gameboard, in icon units

    # overall window sizing
    WIDTH = ICONSIZE * SCALE
    HEIGHT = ICONSIZE * SCALE

    # icon containers, initialized lazily once the root Tk object is set up
    FLOOR_TILES = []
    GOAL_ICONS  = []
    WALL_ICONS  = []

    def __init__(self):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=World.WIDTH, height=World.HEIGHT)
        self.canvas.pack()

        if 0 == len(World.FLOOR_TILES):
            World.FLOOR_TILES.append(self.init_image("./img/floor.gif"))

        if 0 == len(World.GOAL_ICONS):
            World.GOAL_ICONS.append(self.init_image("./img/goal.gif"))

        if 0 == len(World.WALL_ICONS):
            World.WALL_ICONS.append(self.init_image("./img/wall1.gif"))
            World.WALL_ICONS.append(self.init_image("./img/wall2.gif"))
            World.WALL_ICONS.append(self.init_image("./img/wall3.gif"))
            World.WALL_ICONS.append(self.init_image("./img/wall4.gif"))
            World.WALL_ICONS.append(self.init_image("./img/wall5.gif"))

    def init_image(self,image_path):
        """Wrap the creation of an image so callers don't need to import tkinter"""
        return tkinter.PhotoImage(file=image_path)
    
    # Accessors for class constants

    def icon_size(self):
        """Accessor for constants: length/width of in-game icons"""
        return World.ICONSIZE

    def goal_icons(self):
        """Accessor for constants: a list of goal icons, index 0 is the default"""
        return World.GOAL_ICONS

    def wall_icons(self):
        """Accessor for constants: a list of wall icons"""
        return World.WALL_ICONS

    def floor_tiles(self):
        """Accessor for constants: a list of floor tile icons, index 0 is the default"""
        return World.FLOOR_TILES

    def tile_size(self):
        """Accessor for constants: length/width of in-game floor"""
        return World.TILESIZE

    def scale(self):
        """Accessor for constants: multiplied by icon_size to get world width and height"""
        return World.SCALE

    def width(self):
        """Accessor for constants: width (in pixels) of the overall world"""
        return World.WIDTH

    def height(self):
        """Accessor for constants: height (in pixels) of the overall world"""
        return World.HEIGHT

    # Accessors for directions, to hide the Tk details

    def N(self):
        return tkinter.N

    def NE(self):
        return tkinter.NE

    def E(self):
        return tkinter.E

    def SE(self):
        return tkinter.SE

    def S(self):
        return tkinter.S

    def SW(self):
        return tkinter.SW

    def W(self):
        return tkinter.W

    def NW(self):
        return tkinter.NW

##

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


##

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
        # turn right. If the goal is more than four turns from the
        # current direction, then wrap around the end of the array to
        # reach the goal.
        #
        # Example:
        # DIRECTIONS: [N, NE, E, SE, S, SW, W, NW]
        #
        #
        # If the character is facing N and wants to face SW, then the
        # shortest route is counter-clockwise off the bottom of the list
        # and wrapping to the top: N -> NW -> W -> SW

        current_index = Moveable.DIRECTIONS.index(self.facing)
        goal_index  = Moveable.DIRECTIONS.index(direction)

        if (goal_index > current_index):
            if (goal_index - current_index <= 4):
                # clockwise turn
                self._turn_until(current_index, direction, 1)
            else:
                # counter-clockwise turn, off the low end of the array
                self._turn_until(current_index, direction, -1)
        else:
            if (current_index - goal_index <= 4):
                # counter-clockwise turn
                self._turn_until(current_index, direction, -1)
            else:
                # clockwise turn, off the high end of the array
                self._turn_until(current_index, direction, -1)
            
    def _turn_until(self, current_index, goal_direction, increment):
        """Animate the turn"""
        while self.facing != goal_direction:
            time.sleep(0.1) # xxx replace with a call to refresh the world
            current_index = (current_index + increment) % 8
            self.facing = Moveable.DIRECTIONS[current_index]

            if self.facing in self.icons.keys():
                self.world.canvas.itemconfig(self.icon, image=self.icons[self.facing])

    def step_facing(self):
        """Move one step in the direction that the player is facing"""

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
        """Return the coordinates of the block the player is facing"""

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

        
##

class Player(Moveable):

    # class constants are initialized lazily in __init__
    #
    ICONS = {}      # stored per compass direction

    # Used to decide how to turn the player

    def __init__(self, world, x=1, y=1):

        # lazy init: when the class is defined, the Tk instance is not ready yet
        if len(Player.ICONS) == 0:
            Player.ICONS[world.N()]  = world.init_image("./img/kelvin_n.gif")
            Player.ICONS[world.NE()] = world.init_image("./img/kelvin_ne.gif")
            Player.ICONS[world.E()]  = world.init_image("./img/kelvin_e.gif")
            Player.ICONS[world.SE()] = world.init_image("./img/kelvin_se.gif")
            Player.ICONS[world.S()]  = world.init_image("./img/kelvin_s.gif")
            Player.ICONS[world.SW()] = world.init_image("./img/kelvin_sw.gif")
            Player.ICONS[world.W()]  = world.init_image("./img/kelvin_w.gif")
            Player.ICONS[world.NW()] = world.init_image("./img/kelvin_nw.gif")

        self.icons = Player.ICONS
        
        super().__init__(world = world,
                         x = x, y = y,
                         facing = world.N(),
                         icons = self.icons);

###

import random

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

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

    def init_image(self,image_file):
        """Wrap the creation of an image so callers don't need to import tkinter"""
        return tkinter.PhotoImage(file=image_file)
    
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

class Player:

    # class constants are initialized lazily in __init__
    #
    DIRECTIONS = [] # ordered array of compass points (N, NE, etc.)
    ICONS = {}      # stored per compass direction

    # Used to decide how to turn the player

    def __init__(self, world, x=1, y=1):
        self.world = world

        # lazy init: when the class is defined, the Tk instance is not ready yet
        if len(Player.ICONS) == 0:
            Player.ICONS[self.world.N()]  = self.world.init_image("./img/kelvin_n.gif")
            Player.ICONS[self.world.NE()] = self.world.init_image("./img/kelvin_ne.gif")
            Player.ICONS[self.world.E()]  = self.world.init_image("./img/kelvin_e.gif")
            Player.ICONS[self.world.SE()] = self.world.init_image("./img/kelvin_se.gif")
            Player.ICONS[self.world.S()]  = self.world.init_image("./img/kelvin_s.gif")
            Player.ICONS[self.world.SW()] = self.world.init_image("./img/kelvin_sw.gif")
            Player.ICONS[self.world.W()]  = self.world.init_image("./img/kelvin_w.gif")
            Player.ICONS[self.world.NW()] = self.world.init_image("./img/kelvin_nw.gif")

        if len(Player.DIRECTIONS) == 0:
            Player.DIRECTIONS = [self.world.N(), self.world.NE(), self.world.E(), self.world.SE(),
                                 self.world.S(), self.world.SW(), self.world.W(), self.world.NW()]

        self.facing = Player.DIRECTIONS[0]
        self.x = x
        self.y = y

        self._img_id = self.world.canvas.create_image(x*self.world.icon_size(), y*self.world.icon_size(),
                                                     image=Player.ICONS[self.facing],
                                                     anchor=self.world.NW())

    def turn_toward(self,direction):
        """Orient the player in the given direction, taking the fewest number of moves possible"""

        if direction not in Player.DIRECTIONS:
            return

        if self.facing == direction:
            return

        # try looking "up" the directions array for the goal: if
        # it's 4 or less steps away from the current position, then
        # stepping positively through the array is the proper choice,
        # otherwise, step negatively "down" through the directions,
        # wrapping at the ends as appropriate

        current_index = Player.DIRECTIONS.index(self.facing)
        goal_index  = Player.DIRECTIONS.index(direction)

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

    def _turn_until(self,current_index, goal_direction, increment):
        """Animate the turn"""
        while self.facing != goal_direction:
            time.sleep(0.1) # xxx replace with a call to refresh the world
            current_index = (current_index + increment) % 8
            self.facing = Player.DIRECTIONS[current_index]
            self.world.canvas.itemconfig(self._img_id, image=Player.ICONS[self.facing])

    def step_facing(self):
        """Move one step in the direction that the player is facing"""

        if self.facing == self.world.N():
            self.world.canvas.move(self._img_id, 0, -self.world.icon_size())
            self.y -= 1
        elif self.facing == self.world.E():
            self.world.canvas.move(self._img_id, self.world.icon_size(), 0)
            self.x += 1
        elif self.facing == self.world.W():
            self.world.canvas.move(self._img_id, -self.world.icon_size(), 0)
            self.x -= 1
        elif self.facing == self.world.S():
            self.world.canvas.move(self._img_id, 0, self.world.icon_size())
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

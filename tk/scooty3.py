#!/usr/bin/env python3
"""Basic player control, wall/collision sensing, and goal reaching"""

###

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
            World.FLOOR_TILES.append(tkinter.PhotoImage(file="./img/floor.gif"))

        if 0 == len(World.GOAL_ICONS):
            World.GOAL_ICONS.append(tkinter.PhotoImage(file="./img/goal.gif"))

        if 0 == len(World.WALL_ICONS):
            World.WALL_ICONS.append(tkinter.PhotoImage(file="./img/wall1.gif"))
            World.WALL_ICONS.append(tkinter.PhotoImage(file="./img/wall2.gif"))
            World.WALL_ICONS.append(tkinter.PhotoImage(file="./img/wall3.gif"))
            World.WALL_ICONS.append(tkinter.PhotoImage(file="./img/wall4.gif"))
            World.WALL_ICONS.append(tkinter.PhotoImage(file="./img/wall5.gif"))

##

class Level:

    def __init__(self, world):
        self.world = world
        self.walls = set()
        self.goals = set()

    # floor tiling
    def draw_floor(self, tile = 0):
        """Draw the specified floor tile on the world's canvas"""
        
        for x in range(0, World.WIDTH, World.TILESIZE):
            for y in range(0, World.HEIGHT, World.TILESIZE):
                self.world.canvas.create_image(x, y,
                                               image=World.FLOOR_TILES[tile],
                                               anchor=tkinter.NW)

    # wall drawing
    def put_wall(self, x, y):
        """Draw a wall at the game x,y and remember the location"""
            
        # Don't bother overdrawing existing walls
        if (x,y) in self.walls:
            return
            
        self.walls.add((x,y))
        self.world.canvas.create_image(x*World.ICONSIZE, y*World.ICONSIZE,
                                       image=random.choice(World.WALL_ICONS),
                                       anchor=tkinter.NW)
            
    # goal drawing
    def put_goal(self, x, y):
        """Draw a goal at the game x,y and remember the location"""

        # No goals allowed on walls
        if (x,y) in self.walls:
            return

        # Don't overdraw existing goals
        if (x,y) in self.goals:
            return

        self.goals.add((x,y))
        self.world.canvas.create_image(x*World.ICONSIZE, y*World.ICONSIZE,
                                       image=World.GOAL_ICONS[0],
                                       anchor=tkinter.NW)
        

##

class Player:

    import tkinter

    ICONS = {}

    # Used to decide how to turn the player
    DIRECTIONS = [tkinter.N, tkinter.NE, tkinter.E, tkinter.SE,
                  tkinter.S, tkinter.SW, tkinter.W, tkinter.NW]
    
    def __init__(self, world):
        self.facing = tkinter.N
        self.x = 1
        self.y = 1
        self.world = world
        
        # lazy init: when the class is defined, the Tk instance is not ready yet
        if len(Player.ICONS) == 0:
            Player.ICONS[tkinter.N]  = tkinter.PhotoImage(file="./img/kelvin_n.gif")
            Player.ICONS[tkinter.NE] = tkinter.PhotoImage(file="./img/kelvin_ne.gif")
            Player.ICONS[tkinter.E]  = tkinter.PhotoImage(file="./img/kelvin_e.gif")
            Player.ICONS[tkinter.SE] = tkinter.PhotoImage(file="./img/kelvin_se.gif")
            Player.ICONS[tkinter.S]  = tkinter.PhotoImage(file="./img/kelvin_s.gif")
            Player.ICONS[tkinter.SW] = tkinter.PhotoImage(file="./img/kelvin_sw.gif")
            Player.ICONS[tkinter.W]  = tkinter.PhotoImage(file="./img/kelvin_w.gif")
            Player.ICONS[tkinter.NW] = tkinter.PhotoImage(file="./img/kelvin_nw.gif")

        self._tk_id = self.world.canvas.create_image(self.x*World.ICONSIZE, self.y*World.ICONSIZE,
                                               image=Player.ICONS[self.facing],
                                               anchor=tkinter.NW)
            
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
            time.sleep(0.1)
            current_index = (current_index + increment) % 8
            self.facing = Player.DIRECTIONS[current_index]
            self.world.canvas.itemconfig(self._tk_id, image=Player.ICONS[self.facing])

    def step_facing(self):
        """Move one step in the direction that the player is facing"""

        if self.facing == tkinter.N:
            self.world.canvas.move(self._tk_id, 0, -World.ICONSIZE)
            self.y -= 1
        elif self.facing == tkinter.E:
            self.world.canvas.move(self._tk_id, World.ICONSIZE, 0)
            self.x += 1
        elif self.facing == tkinter.W:
            self.world.canvas.move(self._tk_id, -World.ICONSIZE, 0)
            self.x -= 1
        elif self.facing == tkinter.S:
            self.world.canvas.move(self._tk_id, 0, World.ICONSIZE)
            self.y += 1
        else:
            # No diagonal moves allowed
            pass

    def facing_point(self):
        """Return the coordinates of the block the player is facing"""

        if self.facing == tkinter.N:
            return((self.x, self.y-1))
        elif self.facing == tkinter.NE:
            return((self.x+1, self.y-1))
        elif self.facing == tkinter.E:
            return((self.x+1, self.y))
        elif self.facing == tkinter.SE:
            return((self.x+1, self.y+1))
        elif self.facing == tkinter.S:
            return((self.x, self.y+1))
        elif self.facing == tkinter.SW:
            return((self.x-1, self.y+1))
        elif self.facing == tkinter.W:
            return((self.x-1, self.y))
        elif self.facing == tkinter.NW:
            return((self.x-1, self.y-1))
        else:
            pass
        
###

import tkinter
import random
import time

world = World()
tk = world.root # xxx replace with a world.refresh()-ish method later

level = Level(world)    
level.draw_floor()

# outer box of walls
for x in range(World.SCALE):
    for y in [0,World.SCALE-1]:
        level.put_wall(x, y)
        level.put_wall(y, x)

# some interior walls

for x in range(2,World.SCALE,3):
    for y in range(2,World.SCALE,3):
        level.put_wall(x, y)
        level.put_wall(y, x)

# goal in the bottom right
level.put_goal(18,18)
        
p = Player(world)
tk.update()

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
          p.facing in [tkinter.NE, tkinter.SE, tkinter.SW, tkinter.NW]):
        p.turn_toward(random.choice(Player.DIRECTIONS))
    elif (random.randint(0,100) > 90):
        p.turn_toward(random.choice(Player.DIRECTIONS))
    else:        
        p.step_facing()

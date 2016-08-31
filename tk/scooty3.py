#!/usr/bin/env python3
"""Basic player control, wall/collision sensing, and goal reaching"""

import random
import tkinter
import time

ICONSIZE = 32            # pixel size for each game icon (sprite)
TILESIZE = ICONSIZE * 2  # pixel size of the floor tiles
SCALE = 20               # length & width of gameboard, in icon units

# overall window sizing
WIDTH = ICONSIZE * SCALE
HEIGHT = ICONSIZE * SCALE

###

class Player:

    import tkinter
    import time
    
    ICONS = {}

    # Used to decide how to turn the player
    DIRECTIONS = [tkinter.N, tkinter.NE, tkinter.E, tkinter.SE,
                  tkinter.S, tkinter.SW, tkinter.W, tkinter.NW]
    
    def __init__(self, canvas):
        self.facing = tkinter.N
        self.x = 1
        self.y = 1
        self.canvas = canvas
        
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

        self._tk_id = self.canvas.create_image(self.x*ICONSIZE, self.y*ICONSIZE,
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
            self.canvas.itemconfig(self._tk_id, image=Player.ICONS[self.facing])

    def step_facing(self):
        """Move one step in the direction that the player is facing"""

        if self.facing == tkinter.N:
            self.canvas.move(self._tk_id, 0, -ICONSIZE)
            self.y -= 1
        elif self.facing == tkinter.E:
            self.canvas.move(self._tk_id, ICONSIZE, 0)
            self.x += 1
        elif self.facing == tkinter.W:
            self.canvas.move(self._tk_id, -ICONSIZE, 0)
            self.x -= 1
        elif self.facing == tkinter.S:
            self.canvas.move(self._tk_id, 0, ICONSIZE)
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

tk = tkinter.Tk()
world = tkinter.Canvas(tk, width=WIDTH, height=HEIGHT)
world.pack()

#player = tkinter.Canvas(tk, width=ICONSIZE, height=ICONSIZE)
#player.pack()

### Graphics init

# lovely background
floor = tkinter.PhotoImage(file="./img/floor.gif")

# where to steer toward
goal = tkinter.PhotoImage(file="./img/goal.gif")

# randomly selected images when placing walls
walls = []
walls.append(tkinter.PhotoImage(file="./img/wall1.gif"))
walls.append(tkinter.PhotoImage(file="./img/wall2.gif"))
walls.append(tkinter.PhotoImage(file="./img/wall3.gif"))
walls.append(tkinter.PhotoImage(file="./img/wall4.gif"))
walls.append(tkinter.PhotoImage(file="./img/wall5.gif"))

# remember the points where things exist, for collision detection
barriers = set()
goals = set()

### Set up world

# floor tiling
def draw_floor(canvas):
    """Params: (canvas)
    
    canvas: reference to the Tk canvas"""

    for x in range(0,WIDTH,TILESIZE):
        for y in range(0,HEIGHT,TILESIZE):
            canvas.create_image(x, y,
                                image=floor,
                                anchor=tkinter.NW)

# wall drawing
def put_wall(canvas, x, y):
    """Params: (canvas, x, y)
    
    canvas: reference to the Tk canvas
    x, y: game coords, which will be scaled for placement (0,0), (1,0), etc"""

    # Don't bother overdrawing existing walls
    if (x,y) in barriers:
        return

    barriers.add((x,y))
    canvas.create_image(x*ICONSIZE, y*ICONSIZE,
                        image=random.choice(walls),
                        anchor=tkinter.NW)

# goal drawing
def put_goal(canvas, x, y):
    """Params: (canvas, x, y)
    
    canvas: reference to the Tk canvas
    x, y: game coords, which will be scaled for placement (0,0), (1,0), etc"""

    # Don't bother overdrawing existing goals
    if (x,y) in goals:
        return

    goals.add((x,y))
    canvas.create_image(x*ICONSIZE, y*ICONSIZE,
                        image=goal,
                        anchor=tkinter.NW)

### main world
    
draw_floor(world)

# outer box of walls
for x in range(SCALE):
    for y in [0,SCALE-1]:
        put_wall(world, x, y)
        put_wall(world, y, x)

# goal in the bottom right
put_goal(world,18,18)
        
p = Player(world)
tk.update()

# tkinter.mainloop()

game_over = False

while not game_over:
    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)

    if (p.facing_point() in goals):
        p.step_facing()
        tk.update()
        game_over = True        
    elif (p.facing_point() in barriers or
          p.facing in [tkinter.NE, tkinter.SE, tkinter.SW, tkinter.NW]):
        p.turn_toward(random.choice(Player.DIRECTIONS))
    elif (random.randint(0,100) > 80):
        p.turn_toward(random.choice(Player.DIRECTIONS))
    else:        
        p.step_facing()


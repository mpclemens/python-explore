#!/usr/bin/env python3

###

import tkinter

class World:
    """Global game information"""

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

    def refresh(self):
        """Called by players and NPCs to update the (graphic) state of the world"""
        self.root.update_idletasks()
        self.root.update()
    
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


    # references to game objects in the world

    def set_player(self, player):
        self.player = player

    def set_level(self, level):
        self.level = level

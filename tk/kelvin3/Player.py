#!/usr/bin/env python3

from Moveable import Moveable

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

        # Bind up WASD and arrow keys for movement
        
        world.root.bind('<W>', self.move_N)
        world.root.bind('<A>', self.move_W)
        world.root.bind('<S>', self.move_S)
        world.root.bind('<D>', self.move_E)
        
        world.root.bind('<w>', self.move_N)
        world.root.bind('<a>', self.move_W)
        world.root.bind('<s>', self.move_S)
        world.root.bind('<d>', self.move_E)

        world.root.bind('<Up>',    self.move_N)
        world.root.bind('<Left>',  self.move_W)
        world.root.bind('<Down>',  self.move_S)
        world.root.bind('<Right>', self.move_E)

        world.set_player(self)
        
    # handlers for keypresses

    def move_N(self, event):
        self.turn_toward(self.world.N())
        if self.facing_point() not in self.world.level.walls:
            self.step_facing()

    def move_E(self, event):
        self.turn_toward(self.world.E())
        if self.facing_point() not in self.world.level.walls:
            self.step_facing()
        
    def move_S(self, event):
        self.turn_toward(self.world.S())
        if self.facing_point() not in self.world.level.walls:
            self.step_facing()

    def move_W(self, event):
        self.turn_toward(self.world.W())
        if self.facing_point() not in self.world.level.walls:
            self.step_facing()

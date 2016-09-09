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

#!/usr/bin/env python

import random

### HiHo - A cherry of a kid's game

class Spinner:


    # Tuples of a text description and number of cherries to add/remove from
    # the player's bucket
    #
    # Class-level variable, we only need one
    #
    # Using leading underscore is Python convention to mean "private"
    #
    _values = [("one cherry.",1),
               ("two cherries.",2),
               ("three cherries.",3),
               ("four cherries: very lucky!",4),
               ("spilled bucket: too bad, so sad.",-10),
               ("hungry bird.",-2),
               ("sneaky dog.",-2)]

    # Special decorator syntax that modifies the method declaration
    #
    # Instead of an instance, the class itself is passed in as a parameter
    # by the calling code
    #
    @classmethod
    def spin(classname):
        return random.choice(classname._values)


class Player:

    # Magic name for constructor method
    def __init__(self,player_name):
        # Declaring attributes on the fly
        self.name = player_name
        self.cherries = 0


    def take_turn(self,spin_result):
        print "%s spins %s" % (self.get_name(),spin_result[0])
        self.cherries += spin_result[1]
        if (self.cherries < 0):
            self.cherries = 0

    def is_winner(self):
        return self.cherries >= 10

    def get_name(self):
        return self.name

### Main program

players = []

print "Enter player names, youngest to oldest, one per line. Enter an empty name when complete."

while (1): # No do...while loop in Python, so break on the end case
    player_name = raw_input()
    if (len(player_name)):
        players.append(Player(player_name))
        print " Welcome, " + player_name
    else:
        break

if (len(players) < 2):
    print "Not enough players, goodbye"
    exit

else:
    player_number = 0
    while (1):
        current_player = players[player_number]
        current_player.take_turn(Spinner.spin())
        if (current_player.is_winner()):
            print current_player.get_name() + " is the winner!"
            break
        player_number = (player_number + 1) % len(players)
        if (0 == player_number):
            print # put a blank line between each round


#!/usr/bin/env python2
"""Tic-Tac-Toe game implementation for two players, using a text display"""

import pickle

try:
    import pymongo
except:
    # If not present, class will save in local pickled ttt*.save files
    pass

### custom in-game exceptions

class NotYourTurnError(Exception):
    pass

class InvalidLocationError(Exception):
    pass

class InvalidUserError(Exception):
    pass

###

class TTT:

    # All winning combinations, used to check for an endgame
    #
    # Tuple members represent game board positions 1-9
    #
    WINNERS = [(1,2,3), (4,5,6), (7,8,9),  # horizontals
               (1,4,7), (2,5,8), (3,6,9),  # verticals
               (1,5,9), (3,5,7)]           # diagonals

    # Cloud storage: insert URL here to use
    #
    MONGODB_URI = ''

    ###
    def __init__(self, channel, player_X, player_O):
        """Set up a new game in the channel"""

        self.channel = channel
        self.player_X = player_X
        self.player_O = player_O
        self.next_turn = player_X
        self.game_over = False
        self.winner = None
        self._moves = [None] * 9

        try:
            self._storage = pymongo.MongoClient(TTT.MONGODB_URI)
        except:
            self._storage = None

    ###
    def get_board(self, show_labels = False):
        """Return the current tic-tac-toe board, optionally labeling the available spaces with numbers"""
        board = """
 {0} | {1} | {2}
---+---+---
 {3} | {4} | {5}
---+---+---
 {6} | {7} | {8}
"""

        # The self._moves list contains some blend of None, "X", and "O"
        # in its nine indices, corresponding to the formatted string of
        # the board. How None is handled is controlled by the show_labels
        # parameter: either a number is shown for user input, or a blank
        # is shown for general in-channel display
        #
        # If there's an X or O in the space already, that always
        # takes precedence
        #
        if show_labels:
            moves = [ self._moves[n] or (n + 1) for n in range(9) ]
        else:
            moves = [ self._moves[n] or " "     for n in range(9) ]

        return board.format(*moves)

    ###
    def play_at(self, player, location):
        """Put the player's symbol at the given location (1-9)"""

        if player not in (self.player_X, self.player_O):
            raise InvalidUserError

        if self.next_turn != player:
            raise NotYourTurnError

        if self._moves[location-1] is not None:
            raise InvalidLocationError

        if self.player_X == player:
            symbol = "X"
            self.next_turn = self.player_O
        else:
            symbol = "O"
            self.next_turn = self.player_X


        # Mark the board with the player's symbol

        self._moves[location-1] = symbol

        # Check for an end-game situation

        if None not in self._moves:
            self.game_over = True

        # Check only the three-in-a-row combinations that contain the
        # move just made: if all three of those cells on the board
        # contain the just-played symbol, then it's a win for the
        # current player

        possibles = filter(lambda t: location in t, TTT.WINNERS)
        for possible in possibles:
            if symbol == self._moves[possible[0]-1] == self._moves[possible[1]-1] == self._moves[possible[2]-1]:
                self.game_over = True
                self.next_turn = None
                self.winner    = player
                break

    ###
    def play(self, location):
        """Convenience wrapper to take the next turn and save the results"""
        self.play_at(self.next_turn, location)
        self.save()

    ###
    def save(self):
        """Put the state of the game in storage, by channel"""

        save_obj = TTT(None, None, None)
        save_obj.__dict__ = self.__dict__.copy()
        save_obj._storage = None

        if self._storage:

            db = self._storage.get_default_database()
            saves = db["ttt_saves"]

            saves.update_one({'team_id'    : self.channel.team_id,
                              'channel_id' : self.channel.channel_id},
                             {'$set' : {'game_data' : pickle.dumps(save_obj,0)}},
                             upsert = True)

        else:
            filename = "ttt-{}-{}.save".format(self.channel.team_id, self.channel.channel_id)
            data_file = open(filename, "w")
            data_file.write(pickle.dumps(self))
            data_file.flush()

    ###
    def load(self):
        """Fetch the state of the game from storage by channel"""

        if self._storage:

            storage = self._storage # for restorating after the unpickled load

            db = self._storage.get_default_database()
            saves = db["ttt_saves"]

            unpickler = lambda d : pickle.loads(d)

            saved = saves.find({'team_id': self.channel.team_id,
                                'channel_id': self.channel.channel_id});

            for s in saved:
                if "game_data" in s.keys():
                    loaded = pickle.loads(s["game_data"])
                    self.__dict__ = loaded.__dict__.copy()
                    self._storage = storage

        else:
            filename = "ttt-{}-{}.save".format(self.channel.team_id, self.channel.channel_id)
            data_file = open(filename, "rb")
            loaded = pickle.load(data_file)
            self.__dict__ = loaded.__dict__.copy()

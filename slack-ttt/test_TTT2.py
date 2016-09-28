#!/usr/bin/env python2
"""Test cases for TTT class"""

import unittest

from TTT2     import (TTT, NotYourTurnError, InvalidLocationError, InvalidUserError)
from User2    import User
from Channel2 import Channel

###

class Test_TTT(unittest.TestCase):

    ### ALICE AND BOB
    ###
    ###
    def test_story_alice_and_bob(self):

        # * Alice wants to play a friendly game of tic-tac-toe with Bob in a Slack channel

        USER_ALICE = 129
        USER_BOB   = 731
        CHANNEL = Channel(926,525)

        # * She sets up a new ttt

        ttt = TTT(channel = CHANNEL, player_X = USER_ALICE, player_O = USER_BOB)

        self.assertEqual(ttt.channel, CHANNEL,
                         "Bad channel init")
        self.assertEqual(ttt.player_X,   USER_ALICE,
                         "Bad X player init")
        self.assertEqual(ttt.player_O,   USER_BOB,
                         "Bad O player init")
        self.assertEqual(ttt.next_turn,  ttt.player_X,
                         "Bad first player setup")
        self.assertFalse(ttt.game_over,
                         "New game should not be over")

        # * Alice looks at the board to see what spaces are available

        labeled = """
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
"""

        self.assertEqual(labeled, ttt.get_board(show_labels = True),
                         "Board does not match")

        # * She naturally takes the center space

        ttt.play_at(USER_ALICE, 5)

        after = """
 1 | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9
"""

        self.assertEqual(after, ttt.get_board(show_labels = True),
                         "Board does not match")

        self.assertEqual(USER_BOB, ttt.next_turn,
                         "Bob should be next")

        # * She logs out, but the game is saved

        ttt.save()
        ttt = None

        # * Observers in the channel can see the state of the game board now that Alice moved
        #

        ttt = TTT(CHANNEL, None, None)
        ttt.load()

        self.assertEqual(ttt.channel,   CHANNEL,
                         "Bad channel after load")
        self.assertEqual(ttt.player_X,  USER_ALICE,
                         "Bad X player after load")
        self.assertEqual(ttt.player_O,  USER_BOB,
                         "Bad O player after load")
        self.assertEqual(ttt.next_turn, USER_BOB,
                         "Bad next player after load")
        self.assertFalse(ttt.game_over,
                         "Just-begun game should not be over")
        
        plain = """
   |   |  
---+---+---
   | X |  
---+---+---
   |   |  
"""

        self.assertEqual(plain, ttt.get_board(show_labels = False),
                         "Board does not match")

        # * Bob plays in an available space

        before = """
 1 | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9
"""

        self.assertEqual(before, ttt.get_board(show_labels = True),
                         "Board does not match before Bob takes a turn")

        ttt.play_at(USER_BOB, 1)

        after = """
 O | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9
"""

        self.assertEqual(after, ttt.get_board(show_labels = True),
                         "Board does not match after Bob takes a turn")

        self.assertEqual(USER_ALICE, ttt.next_turn,
                         "Alice should follow Bob")        
        
        ttt.save()

        # * Alice and Bob alternate turns until a winner is declared

        ttt.play_at(USER_ALICE, 6)
        ttt.save()
        ttt.play_at(USER_BOB, 4)
        ttt.save()
        ttt.play_at(USER_ALICE, 7)
        ttt.save()

        after = """
 O | 2 | 3
---+---+---
 O | X | X
---+---+---
 X | 8 | 9
"""
        self.assertEqual(after, ttt.get_board(show_labels = True),
                         "Board does not match after alternating turns")

        # * Bob accidentally tries to play in an occupied position

        with self.assertRaises(InvalidLocationError) as context:
            ttt.play_at(USER_BOB, 6)

        after = """
 O | 2 | 3
---+---+---
 O | X | X
---+---+---
 X | 8 | 9
"""
        self.assertEqual(after, ttt.get_board(show_labels = True),
                         "Board should be unchanged after exception")

        self.assertEqual(USER_BOB, ttt.next_turn,
                        "Bob should still be the next player after exception")
        
        # Silly Bob! He takes another turn

        ttt.play_at(USER_BOB, 2)
        ttt.save()

        # And Alice swoops in for the victory

        ttt.play_at(USER_ALICE, 3)

        after = """
 O | O | X
---+---+---
 O | X | X
---+---+---
 X | 8 | 9
"""
        self.assertEqual(after, ttt.get_board(show_labels = True),
                         "Board does not match before the end game is tested")
        
        after = """
 O | O | X
---+---+---
 O | X | X
---+---+---
 X |   |  
"""
        self.assertEqual(after, ttt.get_board(show_labels = False),
                         "Unlabeled board does not match before the end game is tested")

        self.assertTrue(ttt.game_over,
                        "Game should be over")

        self.assertEqual(ttt.winner, USER_ALICE,
                         "Alice should be the winner")

        ttt.save()

    ### BOB AND CAROL AND TED AND ALICE
    ###
    ###
    def test_bob_and_carol_and_ted_and_alice(self):

        USER_BOB    = 731
        USER_CAROL  = 205
        USER_TED    = 416
        USER_ALICE  = 129
        
        CHANNEL_1   = Channel(926,136)
        CHANNEL_2   = Channel(525,596)
        
        # * Carol and Bob are going to play

        ttt1 = TTT(channel = CHANNEL_1, player_X = USER_CAROL, player_O = USER_BOB)

        # * Carol gets to use the cleaner API to play: she's X and goes first

        self.assertEqual(USER_CAROL, ttt1.next_turn,
                        "Carol should be playing first")

        # * Bob has to be patient and wait his turn

        with self.assertRaises(NotYourTurnError) as context:
            ttt1.play_at(USER_BOB, 5)
        
        # * Alice tries to sneak into their game, but is shut down, too

        with self.assertRaises(InvalidUserError) as context:
            ttt1.play_at(USER_ALICE, 5)

        # * Fine, says Alice: I'll get my own game going with Bob and he goes first

        ttt2 = TTT(channel = CHANNEL_2, player_X = USER_BOB, player_O = USER_ALICE)
            
        # * Carol plays in her game and quits

        ttt1.play(5)
        ttt1 = None
        
        # * Bob plays in his game with Alice

        ttt2.play(3)

        # * Alice plays, too, and then they both log out
        ttt2.play(9)        
        ttt2 = None

        # * Bob jumps back in to play in Carol's game on his lucky space

        ttt1 = TTT(CHANNEL_1, None, None)
        ttt1.load()
        ttt1.play(3)

        # * Bob checks the progress of his two games so far
        ttt2 = TTT(CHANNEL_2, None, None)
        ttt2.load()

        game_1 = """
   |   | O
---+---+---
   | X |  
---+---+---
   |   |  
"""

        self.assertEqual(game_1, ttt1.get_board(),
                         "Carol and Bob game does not match")
        

        game_2 = """
   |   | X
---+---+---
   |   |  
---+---+---
   |   | O
"""

        self.assertEqual(game_2, ttt2.get_board(),
                         "Bob and Alice game does not match")

        # * Poor Ted, he can't play anywhere
        
        with self.assertRaises(InvalidUserError) as context:
            ttt1.play_at(USER_TED, 1)

        with self.assertRaises(InvalidUserError) as context:
            ttt2.play_at(USER_TED, 1)

        # * Bob and Carol are ruthless, and reach a tie game

        ttt1.play(1) # X
        ttt1.play(2) # O
        ttt1.play(6) # etc.
        ttt1.play(4) 
        ttt1.play(7)
        ttt1.play(9)
        ttt1.play(8)

        game_1 = """
 X | O | O
---+---+---
 O | X | X
---+---+---
 X | X | O
"""

        self.assertEqual(game_1, ttt1.get_board(),
                         "Carol and Bob game does not match")

        self.assertTrue(ttt1.game_over,
                        "Bob and Carol should be out of moves")

        self.assertTrue(ttt1.winner is None,
                        "Neither Bob nor Carol should have won: it's a draw")                

        # * Now Ted can set up a new game on Channel 1
        ttt1 = TTT(channel = CHANNEL_1, player_X = USER_TED, player_O = USER_ALICE)

        # * Bob and Alice play out their game
        ttt2.play(1) # X
        ttt2.play(2) # O
        ttt2.play(6) # etc.
        ttt2.play(7)
        ttt2.play(5)
        ttt2.play(8) 

        game_2 = """
 X | O | X
---+---+---
   | X | X
---+---+---
 O | O | O
"""
        
        self.assertEqual(game_2, ttt2.get_board(),
                         "Bob and Alice game does not match")

        self.assertTrue(ttt2.game_over,
                        "Bob and Alice should be done")

        self.assertEqual(ttt2.winner, USER_ALICE,
                        "Alice won her game")                


    ### TED NOW GOES BY "T.J."
    ###
    ###
    def test_ted_name_change(self):
        # * Ted and Alice start a game

        USER_TED   = User(user_id = 'AB128', user_name = 'Ted')
        USER_ALICE = User(user_id = 'CD256', user_name = 'Alice')
        CHANNEL    = Channel(7890,1234)

        ttt = TTT(channel = CHANNEL, player_X = USER_TED, player_O = USER_ALICE)

        # * Ted and Alice take a turn each

        ttt.play(5) # * Ted puts an X in the middle
        ttt.play(1) # * Alice claims the top left corner

        # * Ted decides that nobody likes him because of his name, so he gets "hip"
        USER_TED.name = "T.J."

        # * Even though his name has changed, he's still the next player, by ID
        ttt.play(2)

        game = """
 O | X |  
---+---+---
   | X |  
---+---+---
   |   |  
"""        
        self.assertEqual(game, ttt.get_board(),
                         "T.J. and Alice game does not match")

        
#

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

class Card:
    """Represent a playing card and its state"""

    def __init__(self, rank:int, suit:int=None, color:int=None, icon:str=None, back:str="\N{PLAYING CARD BACK}"):
        """Set up a new playing card, parameters are:

        rank:  a numeric value, for ordering
        suit:  a numeric value to represent versions, like "hearts", "clubs", etc.
        color: a color value for display, as in "curses" library
        icon:  a Unicode representation of the card when revealed
        back:  an alternate Unicode representation of the card back

        """
        self.rank = rank
        self.suit = suit
        self.color = color
        self.icon = icon
        self.back = back

        self.hide()        # default display of card is face-down
        self.rotate(None)  # assuming no orientation


    def show(self):
        """Present the front of the card"""
        self._hidden = False

    def hide(self):
        """Present the back of the card"""
        self._hidden = True

    def is_hidden(self):
        return(self._hidden)

    def rotate(self, rotation:int):
        """Set the amount of rotation of the card.

        Intepretation of the value is left to a renderer, but
        suggested values are:

        0 = normal portrait orientation
        1 = landscape orientation (tapped)
        2 = inverted portrait orientation (top-down)
        """
        self._rotation = rotation

    def is_rotated(self):
        return(self._rotation is not None and self._rotation != 0)

###

import unittest

class TestCard(unittest.TestCase):

    def test_create(self):
        card = Card(3, 4, 5, "I", "B")
        self.assertEqual(card.rank,  3,  "Rank does not match")
        self.assertEqual(card.suit,  4,  "Suit does not match")
        self.assertEqual(card.color, 5,  "Color does not match")
        self.assertEqual(card.icon, "I", "Icon does not match")
        self.assertEqual(card.back, "B", "Back does not match")
        # whitebox for internals
        self.assertEqual(card._hidden,   True, "Should default hidden")
        self.assertEqual(card._rotation, None, "Should have no default orientation")

        # some params are required
        self.assertRaises(TypeError, Card.__init__, None)

        # only one param required
        card = Card(6)

        self.assertEqual(card.rank,  6,    "Rank does not match")
        self.assertEqual(card.suit,  None, "Suit does not match")
        self.assertEqual(card.color, None, "Color does not match")
        self.assertEqual(card.icon,  None, "Icon does not match")
        self.assertEqual(card.back, "\N{PLAYING CARD BACK}", "Back does not match")


    def test_show_hide(self):
        card = Card(10)
        self.assertEqual(card.is_hidden(), True, "A new card is always hidden")
        card.show()
        self.assertEqual(card.is_hidden(), False, "Should be shown")
        card.hide()
        self.assertEqual(card.is_hidden(), True, "Should be hidden again")

    def test_rotate(self):
        card = Card(10)
        self.assertEqual(card.is_rotated(), False, "A new card is not rotated")
        card.rotate(0)
        self.assertEqual(card.is_rotated(), False, "Rotation of zero is false")
        card.rotate(5)
        self.assertEqual(card.is_rotated(), True,  "Rotation should be true")
        card.rotate(None)
        self.assertEqual(card.is_rotated(), False, "Rotation should have been cleared")

if __name__ == '__main__':
    unittest.main()

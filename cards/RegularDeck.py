#!/usr/bin/env python3

from Deck import Deck, Card

class RegularDeck(Deck):

    CARDS = [Card(rank=r+1,
                  suit=s+1,
                  color=(s % 2),
                  icon=chr(ord("\N{PLAYING CARD ACE OF SPADES}")+s*16+r))
             for s in range(4) for r in range(13)]

    # Unicode defines a "Knight" card between Jack and Queen, so Queens and Kings
    # have the wrong icon by the above generator. Adjusting:

    for s in range(4):
        CARDS[11+13*s].icon = chr(ord("\N{PLAYING CARD QUEEN OF SPADES}")+s*16)
        CARDS[12+13*s].icon = chr(ord("\N{PLAYING CARD KING OF SPADES}")+s*16)

    RANK_ACE   = 1
    RANK_TWO   = 2
    RANK_THREE = 3
    RANK_FOUR  = 4
    RANK_FIVE  = 5
    RANK_SIX   = 6
    RANK_SEVEN = 7
    RANK_EIGHT = 8
    RANK_NINE  = 9
    RANK_TEN   = 10
    RANK_JACK  = RANK_KNAVE = 11
    RANK_QUEEN = 12
    RANK_KING  = 13

    SUIT_SPADE   = 1
    SUIT_HEART   = 2
    SUIT_CLUB    = 3
    SUIT_DIAMOND = 4

###

import unittest

class TestRegularDeck(unittest.TestCase):

    def test_create(self):
        deck = RegularDeck()
        print([(c.rank, c.suit, c.icon) for c in deck.CARDS])

    def test_queens(self):
        deck = RegularDeck()
        print("QUEENS")
        for s in range(4):
            print(deck.CARDS[11+13*s].icon)

    def test_kings(self):
        deck = RegularDeck()
        print("KINGS")
        for s in range(4):
            print(deck.CARDS[12+13*s].icon)

if __name__ == '__main__':
    unittest.main()

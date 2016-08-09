#!/usr/bin/env python3

from Card import Card
from random import shuffle

class Deck:
    """Represent a stack of playing cards, including discards"""

    def __init__(self, cards:Card=[], refresh:bool=False):
        """Set up a new deck of cards, parameters are:

        cards: an iterator of Card instances
        refresh: Boolean to refill deck when empty
        """

        try:
            if (len(cards)):
                self._draw = cards[:] # copy, to be safe
            else:
                self._draw = []
        except TypeError:
            raise TypeError("Deck needs an iterator of Cards")

        self._discard = []
        self.refresh = refresh


    def size(self):
        return len(self._draw)


    def peek(self, qty:int=1):
        """Return the topmost card(s) in the deck without removal"""
        return(self._draw[-1:-1*(qty+1):-1])


    def draw(self, qty:int=1):
        """Return the topmost card(s) in the deck"""
        if (self.refresh and self.size() == 0):
            self._draw = self._discard

        cards = self.peek(qty)
        del self._draw[self.size()-qty:]
        return(cards)


    def discard(self, card:Card):
        """Discard a single card"""
        self._discard.push(card)


    def deal(self, players:int, qty:int):
        """Deal out equal numbers of cards to players, working through
        the available cards such that each successive player is given
        a card in turn.

        Returns list of lists of Cards of equal size, with remaining
        cards left on the deck"""

        dealt = []

        for player in range(players):
            dealt.append(self._draw[-1 - player :  -1 * (players * qty + 1) : -1 * players])

        del self._draw[(-1*players*qty):]
        return(dealt)


    def deal_all(self, players:int):
        """Deal all cards to players, maybe unevenly

        Returns list of lists of Cards"""
        dealt = []

        if (players != 0):
            dealt = self.deal(players, self.size() // players)

        if (self.size()):
            for hand in range(self.size()):
                dealt[hand].append(self._draw[-1*(hand+1)])
            self._draw = []

        return(dealt)


    def shuffle(self):
        """Randomly mix the cards to draw (not discards)"""
        shuffle(self._draw)

###

import unittest

class TestDeck(unittest.TestCase):

    def test_create(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5)]
        deck  = Deck(cards)

        self.assertEqual(deck.size(), len(cards), "Wrong number of cards")

        self.assertEqual(deck.refresh, False, "Deck will not refill itself when empty")
        # whitebox
        self.assertEqual(deck._draw,       cards, "Cards should exist")
        self.assertEqual(deck._discard,    [],    "Discard container is empty")


    def test_peek(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5)]
        deck  = Deck(cards)

        peeked = deck.peek()

        self.assertEqual(peeked[0].rank, 5, "Last card in deck should be on top")
        self.assertEqual(deck.size(), len(cards), "Wrong number of cards")

        peeked = deck.peek(3)
        self.assertEqual([p.rank for p in peeked],
                         [5, 4, 3],
                         "Last cards in deck should be first in result")


    def test_draw(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5)]
        deck  = Deck(cards)

        drawn = deck.draw()
        self.assertEqual(drawn[0].rank, 5, "Last card in deck should be on top")
        self.assertEqual(deck.size(), len(cards)-1, "Wrong number of cards")

        drawn = deck.draw(3)
        self.assertEqual([p.rank for p in drawn],
                         [4, 3, 2],
                         "Remaining last cards in deck should be on top")
        self.assertEqual(deck.size(), len(cards)-1-3, "Wrong number of cards")


    def test_shuffle(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5)]
        deck  = Deck(cards)

        peeked = deck.peek(5)
        deck.shuffle()
        shuffled = deck.peek(5)

        self.assertNotEqual([p.rank for p in peeked],
                            [s.rank for s in shuffled],
                            "Cards should have been mixed")
        self.assertEqual(deck.size(), len(cards), "Wrong number of cards")


    def test_deal_equal(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6)]
        deck  = Deck(cards)

        dealt = deck.deal(qty=3, players=2)
        player1 = dealt[0]
        player2 = dealt[1]

        self.assertEqual(deck.size(), 0, "No cards left in deck")

        self.assertEqual([c.rank for c in player1],
                         [6, 4, 2],
                         "Ranks not correct")

        self.assertEqual([c.rank for c in player2],
                         [5, 3, 1],
                         "Ranks not correct")

    def test_deal_remainder(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6), Card(7), Card(8), Card(9)]
        deck  = Deck(cards)

        dealt = deck.deal(qty=3, players=2)

        self.assertEqual(deck.size(), 3, "Cards left in deck")

        self.assertEqual([c.rank for c in deck.peek(deck.size())],
                         [3, 2, 1],
                         "Ranks not correct")


    def test_deal_remainder_more(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6), Card(7), Card(8), Card(9), Card(10), Card(11), Card(12), Card(13)]
        deck  = Deck(cards)

        dealt = deck.deal(qty=4, players=3)
        player1 = dealt[0]
        player2 = dealt[1]
        player3 = dealt[2]

        self.assertEqual(deck.size(), 1, "Cards left in deck")

        self.assertEqual([c.rank for c in player1],
                         [13, 10, 7, 4],
                         "Ranks not correct")

        self.assertEqual([c.rank for c in player2],
                         [12, 9, 6, 3],
                         "Ranks not correct")

        self.assertEqual([c.rank for c in player3],
                         [11, 8, 5, 2],
                         "Ranks not correct")


    def test_deal_all(self):
        cards = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6), Card(7), Card(8), Card(9), Card(10), Card(11), Card(12), Card(13)]
        deck  = Deck(cards)

        dealt = deck.deal_all(players=3)
        player1 = dealt[0]
        player2 = dealt[1]
        player3 = dealt[2]

        self.assertEqual(deck.size(), 0, "Cards should be all dealt")

        self.assertEqual([c.rank for c in player1],
                         [13, 10, 7, 4, 1],
                         "Ranks not correct")

        self.assertEqual([c.rank for c in player2],
                         [12, 9, 6, 3],
                         "Ranks not correct")

        self.assertEqual([c.rank for c in player3],
                         [11, 8, 5, 2],
                         "Ranks not correct")


if __name__ == '__main__':
    unittest.main()


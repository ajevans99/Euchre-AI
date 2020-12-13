from .card import Card
from .suit import Suit

import random
from functools import reduce


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit.all():
            for value in Card.RANKS:
                self.cards.append(Card(suit, value))

    def __str__(self):
        return reduce(lambda lhs, rhs: f'{lhs} {rhs}', self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number):
        return [self.cards.pop() for _ in range(number)]

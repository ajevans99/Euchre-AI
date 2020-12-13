from enum import Enum
import random

class Suit(Enum):
    CLUBS = 0
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 4

    def __str__(self):
        return self._unicode_character_map[self.name]

    def color(self):
        return COLORS[self]

    @staticmethod
    def all():
        return list(Suit.__members__.values())

    @staticmethod
    def random_suit():
        return random.choice(Suit.all())

    def matching_color_suit(self):
        for suit, color in COLORS.items():
            if suit != self and self.color() == color:
                return suit
        raise ValueError(f'Matching color for suit {self} not found')

Suit._unicode_character_map = {
    'CLUBS': '♣',
    'SPADES': '♠',
    'HEARTS': '♥',
    'DIAMONDS': '♦'
}

COLORS = {
    Suit.CLUBS: 'black',
    Suit.SPADES: 'black',
    Suit.HEARTS: 'red',
    Suit.DIAMONDS: 'red'
}

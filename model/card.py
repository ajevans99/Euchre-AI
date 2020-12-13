from .suit import Suit
from .utils import sort_by_bower, sort_by_rank, sort_by_trump


class Card:
    # In order by highest to lowest card value
    RANKS = ['A', 'K', 'Q', 'J', '10', '9']

    def __init__(self, suit, rank):
        assert isinstance(suit, Suit)
        self.suit = suit

        assert rank in self.RANKS
        self.rank = rank

    def __str__(self):
        return f'{self.rank}{self.suit}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return ord(self.rank[0]) + self.suit.value

    def is_greater(self, other_card, trump_suit):
        ordered_cards = sorted([self, other_card], key=lambda card: (
            sort_by_bower(card, trump_suit),
            sort_by_trump(card, trump_suit),
            sort_by_rank(card),
        ))
        return self == ordered_cards[0]

from .card import Card
from .suit import Suit
import logging


def generate_heuristics(lead_suit, trump_suit):
    heuristics = {
        suit: {
            rank:
                value * 100
                if suit == trump_suit else
                value * 10
                if suit == lead_suit else
                value
            for value, rank in enumerate(Card.RANKS[::-1], 1)
        }
        for suit in Suit.all()
    }

    heuristics[trump_suit]['J'] = 1500                          # Right bower
    heuristics[trump_suit.matching_color_suit()]['J'] = 1000    # Left bower

    # logging.debug(heuristics)

    return heuristics

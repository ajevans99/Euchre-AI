import logging
from .suit import Suit
from .utils import sort_by_bower, sort_by_rank, sort_by_trump


class Trick:
    def __init__(self, players):
        self.players = players
        self.cards = []

    @staticmethod
    def generate_trump():
        return Suit.random_suit()

    def determine_winner(self, trump_suit):
        """
        Returns player of winning team
        """
        ordered_cards = sorted(self.cards, key=lambda card: (
            sort_by_bower(card[0], trump_suit),
            sort_by_trump(card[0], trump_suit),
            sort_by_rank(card[0]),
        ))
        return ordered_cards[0][1]

    def play(self, trump_suit, cards_played):
        lead_suit = None
        for player in self.players:
            logging.debug(f'{player} Trick:')
            logging.debug(f'Pick card: {player.name()}')
            card = player.play(lead_suit, trump_suit, self.cards, cards_played)
            player.remove_card(card)
            cards_played.append(card)
            self.cards.append((card, player))
            if lead_suit is None:
                # Check for situation were left bower is lead
                # i.e. Hearts are trump, J♦ is lead meaning
                # lead_suit should actually be hearts
                if card.suit.color() == trump_suit.color() and card.rank == 'J':
                    lead_suit = trump_suit
                else:
                    lead_suit = card.suit
            logging.debug(' '.join(map(lambda x: str(x[0]), self.cards)))
            logging.debug(f'Lead suit: {lead_suit}')
            logging.debug(f'Trump suit: {trump_suit}')

            logging.debug(f"Hand: {' '.join(map(str, player.cards))}")
            logging.debug(f'Played: {card}\n')

        return self.determine_winner(trump_suit)

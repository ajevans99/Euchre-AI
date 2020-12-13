from .card import Card
from .deck import Deck
from .heuristics import generate_heuristics
from .utils import cards_that_follow_suit, sort_by_bower, sort_by_rank, sort_by_trump
import random
import logging
from abc import ABC


class Player(ABC):

    def __init__(self, player_id, team_id):
        self.cards = []
        self.team_id = team_id
        self.player_id = player_id

    def __str__(self):
        return f'Player {self.player_id} (Team {self.team_id})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.player_id == other.player_id

    def name(self):
        """
        :return: String representing player type to be
        implemented by subclasses
        """
        raise NotImplemented()

    def give_cards(self, cards):
        """
        Takes list of 5 cards in the player's hand
        """
        assert len(cards) == 5
        assert all(isinstance(card, Card) for card in cards)
        self.cards = cards

    def remove_card(self, card):
        self.cards.remove(card)

    def play(self, lead_suit, trump_suit, previous_cards_in_trick, previous_cards_in_hand):
        raise NotImplemented()


class RandomPlayer(Player):
    def name(self):
        return "RANDOM"

    def play(self, lead_suit, trump_suit, previous_cards_in_trick, previous_cards_in_hand):
        if lead_suit is None:
            return random.choice(self.cards)

        cards_that_follow_lead_suit = cards_that_follow_suit(self.cards, lead_suit, trump_suit)

        if len(cards_that_follow_lead_suit) > 0 and len(previous_cards_in_trick) > 0:
            return random.choice(cards_that_follow_lead_suit)

        return random.choice(self.cards)


class HighPlayer(Player):
    def name(self):
        return "HIGH"

    def play(self, lead_suit, trump_suit, previous_cards_in_trick, previous_cards_in_hand):
        ordered_cards = sorted(self.cards, key=lambda card: (
            sort_by_bower(card, trump_suit),
            sort_by_trump(card, trump_suit),
            sort_by_rank(card),
        ))
        logging.debug(f'Ordered: {ordered_cards}')

        cards_that_follow_lead_suit = cards_that_follow_suit(ordered_cards, lead_suit, trump_suit)

        if len(cards_that_follow_lead_suit) > 0 and len(previous_cards_in_trick) > 0:
            return cards_that_follow_lead_suit[0]

        return ordered_cards[0]


class LowPlayer(Player):
    def name(self):
        return "LOW"

    def play(self, lead_suit, trump_suit, previous_cards_in_trick, previous_cards_in_hand):
        ordered_cards = sorted(self.cards, key=lambda card: (
            sort_by_bower(card, trump_suit),
            sort_by_trump(card, trump_suit),
            sort_by_rank(card),
        ))
        ordered_cards.reverse()
        logging.debug(f'Ordered: {ordered_cards}')

        cards_that_follow_lead_suit = cards_that_follow_suit(ordered_cards, lead_suit, trump_suit)

        if len(cards_that_follow_lead_suit) > 0 and len(previous_cards_in_trick) > 0:
            return cards_that_follow_lead_suit[0]

        return ordered_cards[0]


class HighCautionPlayer(Player):
    def name(self):
        return "HIGH!"

    def play(self, lead_suit, trump_suit, previous_cards_in_trick, previous_cards_in_hand):
        ordered_cards = sorted(self.cards, key=lambda card: (
            sort_by_bower(card, trump_suit),
            sort_by_trump(card, trump_suit),
            sort_by_rank(card),
        ))

        previous_cards_ordered = sorted(previous_cards_in_trick, key=lambda card: (
            sort_by_bower(card[0], trump_suit),
            sort_by_trump(card[0], trump_suit),
            sort_by_rank(card[0]),
        ))

        is_partner_winning = False
        if len(previous_cards_ordered) > 2:
            partner = next(p for _, p in previous_cards_in_trick if p.team_id == self.team_id)
            is_partner_winning = previous_cards_ordered[0][1] == partner

        logging.debug(f'Is partner winning?: {is_partner_winning}')

        cards_that_follow_lead_suit = cards_that_follow_suit(ordered_cards, lead_suit, trump_suit)

        highest_card = ordered_cards[0]

        if len(previous_cards_in_trick) == 0:
            logging.debug(f'No cards played yet. Play High.')
            return highest_card

        can_beat_previous_cards = all(
            highest_card.is_greater(card, trump_suit)
            for card, _ in previous_cards_in_trick
        )

        if len(cards_that_follow_lead_suit) > 0:
            logging.debug(f'Must follow suit.')
            if is_partner_winning or not can_beat_previous_cards:
                logging.debug(f'Dump.')
                return cards_that_follow_lead_suit[-1]
            else:
                logging.debug(f'High.')
                return cards_that_follow_lead_suit[0]

        if is_partner_winning:
            logging.debug(f'Dump.')
            return ordered_cards[-1]

        if can_beat_previous_cards:
            logging.debug(f'Can win. High.')
            return highest_card

        logging.debug(f'Cannot win. Dump.')
        return ordered_cards[-1]


class MDPPlayer(Player):
    def name(self):
        return "MDP"

    def play(self, lead_suit, trump_suit, previous_cards_in_trick, previous_cards_in_hand):
        heuristics = generate_heuristics(lead_suit, trump_suit)
        deck = set(Deck().cards) - set(previous_cards_in_hand)

        points_played_hand = sum(heuristics[card.suit][card.rank] for card in previous_cards_in_hand)
        points_deck = sum(heuristics[card.suit][card.rank] for card in deck)

        points_played_trick = sum(heuristics[card[0].suit][card[0].rank] for card in previous_cards_in_trick)
        points_in_hand = sum(heuristics[card.suit][card.rank] for card in self.cards)

        deck_value = points_deck - points_played_hand
        self_value = points_in_hand - points_played_trick

        probability = self_value / deck_value if deck_value != 0 else 0

        logging.debug(f'{points_deck} - {points_played_hand} = {deck_value}')
        logging.debug(f'{points_in_hand} - {points_played_trick} = {self_value}')

        logging.debug(f'Probability {probability}')

        ordered_cards = sorted(self.cards, key=lambda card: (
            sort_by_bower(card, trump_suit),
            sort_by_trump(card, trump_suit),
            sort_by_rank(card),
        ))
        logging.debug(f'Ordered: {ordered_cards}')

        cards_that_follow_lead_suit = cards_that_follow_suit(ordered_cards, lead_suit, trump_suit)

        if probability >= 0.25:
            logging.debug('play high')
            if len(cards_that_follow_lead_suit) > 0 and len(previous_cards_in_trick) > 0:
                return cards_that_follow_lead_suit[0]
            return ordered_cards[0]
        else:
            logging.debug('play low')
            if len(cards_that_follow_lead_suit) > 0 and len(previous_cards_in_trick) > 0:
                return cards_that_follow_lead_suit[-1]
            return ordered_cards[-1]

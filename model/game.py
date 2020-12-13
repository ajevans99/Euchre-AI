from .heuristics import *
import logging
from .deck import Deck
from .player import RandomPlayer, HighPlayer, HighCautionPlayer, LowPlayer, MDPPlayer
from .trick import Trick


class Game:
    def __init__(self):
        # self.generate_trick()
        self.player_types = [
            MDPPlayer, HighPlayer, MDPPlayer, HighPlayer
        ]
        assert len(self.player_types) == 4, 'Invalid number of players'

    def play_tricks(self):
        deck = Deck()
        deck.shuffle()

        def create_player(player_details):
            # Creates instances of Player with specified player type
            player_id, player_type = player_details
            team_id = player_id % 2
            return player_type(player_id=player_id, team_id=team_id)

        # Order matters
        # Dealer -> 1st -> 2nd -> 3rd
        players = list(map(create_player,
                           enumerate(self.player_types)))

        for player in players:
            player.give_cards(deck.deal(5))
            logging.debug(f'Player {player.player_id}: {list(map(str, player.cards))}')

        kitty = deck.cards
        logging.debug(f'Kitty: {list(map(str, kitty))}')

        team0_score = 0
        team1_score = 0

        cards_played = []

        for _ in range(5):
            trick = Trick(players)
            trump = trick.generate_trump()
            logging.debug(f"New trump: {trump}\n")

            winner = trick.play(trump, cards_played)
            logging.debug(f'Winner: {winner}\n')

            if winner.team_id == 0:
                team0_score += 1
            else:
                team1_score += 1

            winning_player_index = players.index(winner)
            players = players[winning_player_index:] + players[:winning_player_index]

        logging.debug("Trick set complete.")
        logging.debug(f"Team 0: {team0_score}")
        logging.debug(f"Team 1: {team1_score}")

        return team0_score, team1_score

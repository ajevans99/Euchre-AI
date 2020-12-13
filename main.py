import logging
import sys
from model import game
from model.player import RandomPlayer, HighPlayer, HighCautionPlayer, LowPlayer, MDPPlayer
import progressbar


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.WARN)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

GAMES_TO_PLAY = 1000

game = game.Game([MDPPlayer, RandomPlayer, MDPPlayer, RandomPlayer])

team0_wins, team1_wins = 0, 0
team0_points, team1_points = 0, 0
number_games_played = 0

progressbar.streams.wrap_stderr()
configure_logging()

for _ in progressbar.progressbar(range(GAMES_TO_PLAY), redirect_stdout=True):
    hands0, hands1 = 0, 0
    points0, points1 = 0, 0

    while points0 < 10 and points1 < 10:
        result = game.play_tricks()
        hands0 += result[0]
        hands1 += result[1]
        if result[0] > result[1]:
            points0 += 2 if result[0] == 5 else 1
        else:
            points1 += 2 if result[1] == 5 else 1

    logging.info(f'Team 0 hand wins: {hands0}')
    logging.info(f'Team 1 hand wins: {hands1}')
    logging.info(f'Team 0 points: {points0}')
    logging.info(f'Team 1 points: {points1}')

    if points0 > points1:
        team0_wins += 1
    else:
        team1_wins += 1

    team0_points += points0
    team1_points += points1

    number_games_played += 1

    logging.info(f'Team {0 if points0 > points1 else 1} won')

print(f'Team 0 wins: {team0_wins}')
print(f'Team 1 wins: {team1_wins}')
print(f'Team 0 point average: {team0_points / number_games_played}')
print(f'Team 1 point average: {team1_points / number_games_played}')

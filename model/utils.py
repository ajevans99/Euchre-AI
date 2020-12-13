import model.card


def does_follow_suit(card, suit, trump):
    """
    A card follows suit if it has the same suit as `suit` or
    it is the J of same color
    """
    return card.suit == suit or (
        (card.suit.color() == trump.color()) and card.rank == 'J'
    )


def cards_that_follow_suit(cards, suit, trump):
    """
    Determine which cards follow suit
    :param cards: Cards to check
    :param suit: Suit to follow
    :param trump: Suit of trump
    :return: List of cards that follow suit
    """
    return list(filter(lambda card: does_follow_suit(card, suit, trump),
                       cards))


def sort_by_bower(card, trump):
    """
    Returns -2 if right bower, -1 if left bower, 0 else
    """
    if card.rank == 'J' and card.suit.color() == trump.color():
        return -2 if card.suit == trump else -1
    return 0


def sort_by_trump(card, trump):
    """
    Returns -1 if trump, 0 otherwise
    """
    return -1 if card.suit == trump else 0


def sort_by_rank(card):
    return model.card.Card.RANKS.index(card.rank)

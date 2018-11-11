import typing
import random
from src import card as card_mod
# XXX could have ALL zones inherit zone object, (even battlefield/exile/etc?)
# ^- especially useful for type checking in zone.remove(index), or so
# playing/casting from field or exiled, etc are shared so it may be a little tricky....


class Deck:
    def __init__(self):
        self.deck: typing.List[card_mod.Card] = []

    def add_top(self, card):
        self.deck.append(card)

    def remove_top(self):
        return self.deck.pop()

    def shuffle(self):
        random.shuffle(self.deck)

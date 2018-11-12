import typing
import random
from src import zone
from src import card as card_mod
# XXX could have ALL zones inherit zone object, (even battlefield/exile/etc?)
# ^- especially useful for type checking in zone.remove(index), or so
# playing/casting from field or exiled, etc are shared so it may be a little tricky....


class Deck(zone.Zone):
    def __init__(self):
        super().__init__()
        self.deck: typing.List[card_mod.Card] = []

    def add(self, card):
        # XXX good not to keep this separate with add_top (not the same)?
        self.add_top(card)

    def remove(self, id_num):
        # XXX this just ignores id_num, is that good practice?
        # ^ should we do something diff with deck so as to not "waste" param?
        # self.re
        pass

    def add_top(self, card):
        self.deck.append(card)

    def remove_top(self):
        return self.deck.pop()

    def shuffle(self):
        random.shuffle(self.deck)

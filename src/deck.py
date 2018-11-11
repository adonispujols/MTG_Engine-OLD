import typing
import random
from src import card as card_mod


class Deck:
    def __init__(self):
        self.deck: typing.List[card_mod.Card] = []

    def add_top(self, card):
        self.deck.append(card)

    def remove_top(self):
        return self.deck.pop()

    def shuffle(self):
        random.shuffle(self.deck)

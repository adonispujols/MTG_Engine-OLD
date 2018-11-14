import random


class Deck:
    def __init__(self):
        self._deck = []

    def __repr__(self):
        return str(self._deck)

    def push(self, card):
        self._deck.append(card)

    def shuffle(self):
        random.shuffle(self._deck)

    def pop(self):
        return self._deck.pop()

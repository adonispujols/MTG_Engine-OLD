import random


class Deck:
    def __init__(self):
        self.deck = []

    def __repr__(self):
        return str(self.deck)

    def add_top(self, card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def remove_top(self):
        return self.deck.pop()

    def to_string(self):
        return str(self.deck)

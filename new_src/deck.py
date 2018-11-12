import random


class Deck:
    def __init__(self):
        self.deck = []

    def add_top(self, card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

import tkinter as tk
from convert import card as card_mod


class Hand:
    def __init__(self, game, hand_row):
        self._hand = []
        self.hand_buttons = []
        self._game = game
        self._hand_row = hand_row
        self._open_column = 0

    def __repr__(self):
        return str(self._hand)

    def add(self, card: "card_mod.Card"):
        self._hand.append(card)
        # TODO append to buttons array
        card_button = tk.Button(self._game, text=str(card))
        card_button.grid(row=self._hand_row, column=self._open_column)
        self.hand_buttons.append(card_button)
        self._open_column += 1

    def size(self):
        return len(self._hand)

    def get(self, index):
        return self._hand[index]

    def remove(self, index):
        del self._hand[index]

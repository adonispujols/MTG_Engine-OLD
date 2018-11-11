import typing
from src import card as card_mod


class Stack:
    def __init__(self):
        self.stack: typing.List[card_mod.Card] = []

    def push(self, card):
        self.stack.append(card)

    def pop(self):
        return self.stack.pop()

    def empty(self):
        # returns false if stack is empty, the "pythonic" way
        return not self.stack

    def resolve_next(self):
        self.pop().resolve()

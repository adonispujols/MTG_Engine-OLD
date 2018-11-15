class Stack:
    def __init__(self):
        self._stack = []

    def empty(self):
        return not self._stack

    def push(self, card):
        self._stack.append(card)

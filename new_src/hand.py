class Hand:
    def __init__(self):
        self._hand = []

    def __repr__(self):
        return str(self._hand)

    def add(self, card):
        self._hand.append(card)

    def size(self):
        return len(self._hand)

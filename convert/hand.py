class Hand:
    def __init__(self):
        self._hand = []
        # self._hand

    def __repr__(self):
        return str(self._hand)

    def add(self, card):
        self._hand.append(card)

    def size(self):
        return len(self._hand)

    def get(self, index):
        return self._hand[index]

    def remove(self, index):
        del self._hand[index]

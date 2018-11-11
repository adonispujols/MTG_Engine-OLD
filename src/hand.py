class Hand:
    def __init__(self):
        self.hand = []

    def size(self):
        return len(self.hand)

    def add(self, card):
        self.hand.append(card)

    def remove(self, index):
        return self.hand.pop(index)

    def get(self, index):
        return self.hand[index]

class Hand:
    def __init__(self):
        self.hand = []

    def __repr__(self):
        return str(self.hand)

    def add(self, card):
        self.hand.append(card)

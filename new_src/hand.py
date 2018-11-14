class Hand:
    def __init__(self):
        self._hand = []

    def __repr__(self):
        return str(self._hand)

    # named generic add since we don't care where it's added
    # ^ (the zone is unordered anyways)
    def add(self, card):
        self._hand.append(card)

    def size(self):
        return len(self._hand)

    def get(self, index):
        return self._hand[index]

    # XXX POP describes MUCH better what's happening then remove!
    # ^ while remove may or may not return stuff, we KNOW pop (in whatever context)
    # ^ actually DOES! <- that's how the python method works, too!
    # def pop(self, index):
    #     # keep in mind this is 0(n) (everything to right of delete shifts left)
    #     return self._hand.pop(index)

    def remove(self, index):
        del self._hand[index]

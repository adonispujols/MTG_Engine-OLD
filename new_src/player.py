from new_src import deck
from new_src import hand
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


class Player:
    deck: "deck.Deck"
    hand: "hand.Hand"

    def __init__(self):
        self.deck = None
        self._life = 20
        self.max_hand_size = 7
        self.hand = None
        self.active = False
        self._lands_played = 0
        self._land_limit = 1

    def draw(self):
        self.hand.add(self.deck.pop())

    def make_active(self):
        self.active = True

    def make_inactive(self):
        self.active = False

    def under_land_limit(self):
        return self._lands_played < self._land_limit

from convert import hand
from convert import mana_pool
from convert import lands_played as lp
from convert import deck


class Player:
    deck: "deck.Deck"
    hand: "hand.Hand"

    def __init__(self):
        self.deck = None
        self._life = 20
        self.max_hand_size = 7
        self.hand = None
        self.active = False
        self.lands_played = lp.LandsPlayed()
        self._land_limit = 1
        self.mana_pool = mana_pool.ManaPool()

    def draw(self):
        self.hand.add(self.deck.pop())

    def make_active(self):
        self.active = True

    def make_inactive(self):
        self.active = False

    def under_land_limit(self):
        return int(self.lands_played) < self._land_limit

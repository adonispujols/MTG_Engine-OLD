from new_src import deck
from new_src import hand
# XXX avoid importing just for type checking (risks cyclic importing)


class Player:
    hand: hand.Hand
    def __init__(self):
        # XXX hard setting attributes is not ideal. once finished:
        # ^ we'll clean it up/enforce definition where needed
        # ^ or create the object here, if needed
        self.deck = None
        self._life = 20
        self._max_hand_size = 7
        self.hand = None
        self._active = False
        self._lands_played = 0
        self._lands_limit = 1

    def get_max_hand_size(self):
        return self.max_hand_size

    def draw(self):
        self.hand.add(self.deck.remove_top())

    def make_active(self):
        self.active = True

    def make_inactive(self):
        self.active = False

    def is_active(self):
        return self.active

    def met_land_limit(self):
        return self.lands_played < self.lands_limit

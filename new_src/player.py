from new_src import deck
from new_src import hand
# XXX avoid importing just for type checking (risks cyclic importing)


class Player:
    hand: hand.Hand
    deck: deck.Deck

    def __init__(self):
        # XXX hard setting attributes is not ideal. once finished:
        # ^ we'll clean it up/enforce definition where needed
        # ^ or create the object here, if needed
        self.deck = None
        self.life = 20
        self.maximum_hand_size = 7
        self.hand = None
        self.active = False
        # self.priority = False

    def draw(self):
        self.hand.add(self.deck.remove_top())

    def make_active(self):
        self.active = True

    # def make_inactive(self):
    #     self.active = False

    def is_active(self):
        return self.active

    # def give_priority(self):
    #     # sba's are checked
    #     self.priority = True
    #
    # def lose_priority(self):
    #     self.priority = False
    #
    # def has_priority(self):
    #     return self.priority

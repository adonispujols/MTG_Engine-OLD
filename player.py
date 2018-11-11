import hand
import mana_pool


class Player:
    def __init__(self, deck, index):
        self.deck = deck
        self.index = index
        self.hand = hand.Hand()
        self.mana_pool = mana_pool.ManaPool()
        self.maximum_hand_size = 7
        self.max_lands_per_turn = 1
        self.lands_played = 0
        self.has_priority = False
        self.active = False
        self.paying_mana_cost = False

    def active(self):
        return self.active

    def due_priority(self):
        pass

    def has_priority(self):
        return self.has_priority

    def index(self):
        return self.index

    def gain_priority(self):
        # state based actions check goes here, BEFORE they get priority
        self.has_priority = True

    def lose_priority(self):
        self.has_priority = False

    def make_active(self):
        self.active = True

    def make_nonactive(self):
        self.active = False

    def paying_mana_cost(self):
        return self.paying_mana_cost

    def started_paying_mana_cost(self):
        self.paying_mana_cost = True

    def stopped_paying_mana_cost(self):
        self.paying_mana_cost = False

    def draw(self, amount):
        for i in range(amount):
            self.hand.add(self.deck.remove_top())

    # def untap_all_permanents(self, permanents):
    #     for card in permanents:
    #         card.untap()

    def pay_costs(self, costs):
        for cost in costs:
            if not cost.pay():
                raise RuntimeError("ERROR: Failed to pay cost. Player: ", self.index())
                # XXX useful to know WHICH cost triggered this
        return True

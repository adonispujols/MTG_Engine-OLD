class Player:
    def __init__(self):
        # XXX hard setting attributes is not ideal. once finished:
        # ^ we'll clean it up/enforce definition where needed
        # ^ or create the object here, if needed
        self.deck = None
        self.life = 20
        self.maximum_hand_size = 7
        self.hand = None

# dummy for type checking
class Signal:
    NAME = None


class ChooseStartingPlayer(Signal):
    NAME = "ChooseStartingPlayer"

    def __init__(self, index):
        self.index = index

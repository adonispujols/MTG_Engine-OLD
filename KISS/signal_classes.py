class Signal:
    NAME = None


class ChoosingPlayer(Signal):
    NAME = "ChoosePlayer"

    def __init__(self, index):
        self.index = index


class InPriority(Signal):
    NAME = "InPriority"

    def __init__(self, index):
        self.index = index

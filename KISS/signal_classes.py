class Signal:
    def __init__(self, name):
        self.name = name


class ChoosingPlayer(Signal):
    def __init__(self, index):
        super().__init__("ChoosePlayer")
        self.index = index


class InPriority(Signal):
    def __init__(self, index):
        super().__init__("InPriority")
        self.index = index

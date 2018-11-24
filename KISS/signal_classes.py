# dummy for type checking
class Signal:
    def __init__(self, name):
        self.name = name


class ChoosePlayer(Signal):
    def __init__(self, index):
        super().__init__("ChoosePlayer")
        self.index = index

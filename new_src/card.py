class Card:
    def __init__(self, name):
        self._name = name
        self._tapped = False
        self.type = "Land"

    def __repr__(self):
        return self._name

    def untap(self):
        if self._tapped:
            self._tapped = False
            return True
        else:
            return False

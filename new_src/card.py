class Card:
    def __init__(self, name):
        self._name = name
        self._tapped = False
        self.type = "Land"
        self.ability = "{T}: Add G"

    def __repr__(self):
        return self._name

    def tap(self):
        if self._tapped:
            return False
        self._tapped = True
        return True

    def untap(self):
        if self._tapped:
            self._tapped = False
            return True
        return False

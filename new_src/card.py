class Card:
    def __init__(self, name):
        self._name = name
        self.tapped = False
        self.type = "Land"

    def __repr__(self):
        return self._name

    def untap(self):
        if self.tapped:
            self.tapped = False
            return True
        else:
            return False

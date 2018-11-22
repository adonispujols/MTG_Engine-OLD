class Card:
    def __init__(self, name, card_type):
        self._name = name
        self._tapped = False
        self.card_type = card_type
        self.ability = "{T}: Add G"

    def __repr__(self):
        return "{} {}".format(self._name, "T" if self._tapped else "F")

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

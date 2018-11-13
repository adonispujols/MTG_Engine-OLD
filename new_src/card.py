class Card:
    def __init__(self, name):
        self._name = name
        self._tapped = False
        self._type = "Land"

    def __repr__(self):
        return self._name

    def type(self):
        return self._type

    def _is_tapped(self):
        return self._tapped

    def untap(self):
        if self._is_tapped():
            self._tapped = False
            return True
        else:
            return False

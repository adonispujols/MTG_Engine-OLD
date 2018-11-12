class Card:
    def __init__(self, name):
        self.name = name
        self.tapped = False

    def __repr__(self):
        return self.name

    def is_tapped(self):
        return self.tapped

    def untap(self):
        if self.is_tapped():
            self.tapped = False
            return True
        else:
            return False

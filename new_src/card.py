class Card:
    def __init__(self, name):
        self.name = name
        self.tapped = False
        self.type = "Land"

    def __repr__(self):
        return self.name

    def get_type(self):
        return self.type

    def is_tapped(self):
        return self.tapped

    def untap(self):
        if self.is_tapped():
            self.tapped = False
            return True
        else:
            return False

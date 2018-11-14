class Battlefield:
    def __init__(self):
        self.field = []

    def __repr__(self):
        return str(self.field)

    def add(self, card, player_idx):
        self.field.append(card, player_idx)

    def size(self, player_idx):
        return len(self.field[player_idx])

    def get(self, player_idx, index):
        return self.field[player_idx][index]

    def remove(self, index, player_idx):
        del self.field[index]

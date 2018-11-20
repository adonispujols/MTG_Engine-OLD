from convert import mana_types as mt


class ManaPool:
    def __init__(self):
        self._pool = [0, 0, 0, 0, 0, 0]

    def add(self, m_type):
        self._pool[m_type] += 1

    def empty(self):
        self._pool = [0 for _ in self._pool]

    def remove(self, mana: "mt.ManaTypes"):
        index = mana.value
        if self._pool[index] > 0:
            self._pool[index] -= 1
            return True
        return False

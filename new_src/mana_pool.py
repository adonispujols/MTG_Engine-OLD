class ManaPool:
    def __init__(self):
        self._pool = [0, 0, 0, 0, 0, 0]

    def add(self, m_type):
        self._pool[m_type] += 1

    def empty(self):
        for i in self._pool:
            self._pool[i] = 0

    def remove(self, mana):
        index = mana.value
        if self._pool[index] > 0:
            self._pool[index] -= 1
            return True
        return False

class ManaPool:
    def __init__(self):
        self._pool = [0, 0, 0, 0, 0, 0]

    def add(self, m_type):
        # XXX this might fail if mana_types' values change (in type or meaning)
        self._pool[m_type] += 1

    def empty(self):
        for i in self._pool:
            self._pool[i] = 0

class Passes:
    def __init__(self):
        self._count = 0

    def __int__(self):
        return self._count

    def inc(self):
        self._count += 1

    def reset(self):
        self._count = 0

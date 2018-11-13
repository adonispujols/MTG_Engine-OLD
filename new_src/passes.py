class Passes:
    def __init__(self):
        self._passes = 0

    def inc(self):
        self._passes += 1

    def reset(self):
        self._passes = 0

    def count(self):
        return self._passes

class Passes:
    def __init__(self):
        self.count = 0

    def __int__(self):
        return self.count

    def inc(self):
        self.count += 1

    def reset(self):
        self.count = 0

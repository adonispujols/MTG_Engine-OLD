class Passes:
    def __init__(self):
        self.passes = 0

    def inc(self):
        self.passes += 1

    def reset(self):
        self.passes = 0

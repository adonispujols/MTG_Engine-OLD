import collections

# dummy for type checking
class Signal:
    NAME = None


class ChooseStartingPlayer(Signal):
    NAME = "ChooseStartingPlayer"

    def __init__(self, index):
        self.index = index

d = collections.deque()
d.append(ChooseStartingPlayer(2))
d.append(1)
d.append(2)
d.append(3)
d.append(4)
new_signal = d.popleft()
print(type(new_signal))


def choose_start(signal: ChooseStartingPlayer):
    print(signal.index)


def process_signal(signal: Signal):
    dct[signal.NAME](signal)


dct = {ChooseStartingPlayer.NAME: choose_start}

process_signal(new_signal)

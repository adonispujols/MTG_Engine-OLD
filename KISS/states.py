import abc
import random
import collections
from KISS import game as game_mod
from KISS import events as ev
from KISS import signal_classes as sgn


class State(abc.ABC):
    def __init__(self, signals: "collections.deque", signal: "sgn.Signal"):
        signals.append(signal)

    @abc.abstractmethod
    def process(self, event):
        pass


class ChoosingPlayer(State):
    def __init__(self, signals, game: "game_mod.Game", context):
        super().__init__(signals, sgn.ChoosingPlayer(random.randrange(len(game.players))))
        self._context = context

    def process(self, event):
        self._context(event)


class InPriority(State):
    def __init__(self, signals, game: "game_mod.Game", index):
        super().__init__(signals, sgn.InPriority(index))
        self._game = game
        self._index = index

    def process(self, event):
        if event == ev.Events.PASS.value:
            self._game.pass_priority(self._index)
        elif event == ev.Events.PLAY.value:
            pass



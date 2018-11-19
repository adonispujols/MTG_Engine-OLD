import tkinter as tk
import abc
import random
import functools
import typing
from convert import game as game_mod
from convert import turn_parts as tp
from convert import bindings as bnd


class State(abc.ABC):
    @abc.abstractmethod
    def run(self, message):
        pass

    @abc.abstractmethod
    def next(self, event):
        pass


class ChoosingStartingPlayer(State):
    _choose_btns: typing.List["tk.Button"]

    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self._choose_btns = []

    def run(self, _):
        # [CR 103.2]
        index = random.randrange(len(self._game.players))
        player_label = tk.Label(self._game,
                                text="P{}, who goes first?".format(index + 1))
        player_label.grid()
        # for user to choose (and in debug)
        for i in range(len(self._game.players)):
            choose_btn = tk.Button(self._game,
                                   text=i, command=functools.partial(self._game.advance, event=i))
            self._choose_btns.append(choose_btn)
            choose_btn.grid()
        # TODO give AI ability to choose

    def next(self, starting_player):
        for btn in self._choose_btns:
            btn.destroy()
        self._choose_btns.clear()
        # [CR 103.7]
        return OnFirstUntap(self._game, starting_player)


class OnUntap(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.UNTAP
        self._game.players[self.switch_active()].make_active()
        self._game.reset_lands_played()
        self._game.untap_all_of_active()
        self._game.empty_mana_pools()
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, event):
        return self._game.on_upkeep

    def switch_active(self):
        prev_active = self._game.active_index()
        self._game.players[prev_active].make_inactive()
        return (prev_active + 1) % len(self._game.players)


class OnFirstUntap(OnUntap):
    def __init__(self, game: "game_mod.Game", starting_player):
        super().__init__(game)
        self._starting_player = starting_player

    def switch_active(self):
        return self._starting_player


class OnUpkeep(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.UPKEEP
        # send priority event, letting them know which player
        # game.give_player_priority(game.active_index())

    def next(self, event):
        self._game.on_give_priority.index = event
        return OnGivePriority


class OnGivePriority(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self.index = None

    def run(self, _):
        # TODO check for state based actions (perhaps make into separate state)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, event):
        self._game.in_priority.index = self.index
        pass


class InPriority(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game
        # TODO should delay this
        self._init_gui()
        self.index = None

    def _init_gui(self):
        button = tk.Button(self._game, text="pass")
        button.bind()
        button.grid()

    def run(self, _):
        # TODO Again, need to give AI options
        pass

    def next(self, event):
        # TODO react based on option
        pass

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
    def run(self):
        pass

    @abc.abstractmethod
    def next(self, event):
        pass


# According to [CR 103]
class ChoosingStartingPlayer(State):
    _choose_btns: typing.List["tk.Button"]

    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self._choose_btns = []

    def run(self):
        # [CR 103.2]
        index = random.randrange(len(self._game.players))
        player_label = tk.Label(self._game,
                                text="P{}, who goes first?".format(index + 1))
        player_label.grid()
        # for user to choose (and in debug)
        for i in self._game.players:
            choose_btn = tk.Button(self._game,
                                   text=i, command=functools.partial(self._game.advance, i))
            self._choose_btns.append(choose_btn)
            choose_btn.grid()
        # TODO give AI option/ability to choose

    def next(self, event):
        for btn in self._choose_btns:
            btn.destroy()
        self._choose_btns.clear()
        # [CR 103.7]
        self._game.on_first_untap.new_active = event  # event = p index chosen
        return self._game.on_first_untap


class OnUntap(State):
    def __init__(self, game: "game_mod.Game"):
        self.game = game
        self.new_active = None

    def run(self):
        self.game.step_or_phase = tp.TurnParts.UNTAP
        self.switch_active()
        self.game.players[self.new_active].make_active()
        self.game.reset_lands_played()
        self.game.untap_all_of_active()
        self.game.empty_mana_pools()
        self.game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, event):
        return self.game.on_upkeep

    def switch_active(self):
        prev_active = self.game.active_index()
        self.game.players[prev_active].make_inactive()
        self.new_active = (prev_active + 1) % len(self.game.players)


class OnFirstUntap(OnUntap):
    # dummy
    def switch_active(self):
        pass


class OnUpkeep(State):
    def __init__(self, game: "game_mod.Game"):
        self.game = game

    def run(self):
        self.game.step_or_phase = tp.TurnParts.UPKEEP
        # send priority event, letting them know which player
        # game.give_player_priority(game.active_index())

    def next(self, event):
        self.game.on_give_priority
        return OnGivePriority
        # todo return give priority


class OnGivePriority(State):
    def __init__(self, game: "game_mod.Game"):
        self.game = game
        self.index = None

    def run(self):
        # TODO check for state based actions
        self.game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, event):
        # return inpriority
        pass

# TODO Again, need to give AI options
# for prioirty
# class
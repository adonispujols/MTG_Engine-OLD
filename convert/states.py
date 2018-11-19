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
    choose_btns: typing.List["tk.Button"]

    def __init__(self, game: "game_mod.Game"):
        self.game = game
        self.choose_btns = []

    def run(self):
        # [CR 103.2]
        index = random.randrange(len(self.game.players))
        player_label = tk.Label(self.game,
                                text="P{}, who goes first?".format(index + 1))
        player_label.grid()
        # for user to choose (and in debug)
        for i in self.game.players:
            choose_btn = tk.Button(self.game,
                                   text=i, command=functools.partial(self.game.advance, i))
            self.choose_btns.append(choose_btn)
            choose_btn.grid()
        # TODO give AI option/ability to choose

    def next(self, event):
        for btn in self.choose_btns:
            btn.destroy()
        self.choose_btns.clear()
        # [CR 103.7]
        self.game.first_untap.starting_player = event  # event = p index chosen
        return self.game.first_untap


class FirstUntap(State):
    def __init__(self, game: "game_mod.Game"):
        self.game = game
        self.starting_player = None

    def run(self):
        self.game.step_or_phase = tp.TurnParts.UNTAP
        self.game.players[self.starting_player].make_active()
        self.game.reset_lands_played()
        self.game.untap_all_of_active()
        self.game.empty_mana_pools()
        self.game.event_generate(bnd.Bindings.START_NEXT_STEP_OR_PHASE.value, when="tail")

    def next(self, event):
        # return first upkeep step
        pass

class
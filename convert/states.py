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
        self.game.on_first_untap.new_active = event  # event = p index chosen
        return self.game.on_first_untap


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
        self.game.event_generate(bnd.Bindings.START_NEXT_STEP_OR_PHASE.value, when="tail")

    def next(self, event):
        # next upkeep
        pass

    def switch_active(self):
        prev_active = self.game.active_index()
        self.game.players[prev_active].make_inactive()
        self.new_active = (prev_active + 1) % len(self.game.players)



class OnFirstUntap(OnUntap):
    def next(self, event):
        # return first upkeep step
        pass

    # dummy
    def switch_active(self):
        pass

class OnUpkeep(State):
    def __init__(self, game: "game_mod.Game"):
        self.game = game

    def run(self):
        self.game.step_or_phase = tp.TurnParts.UPKEEP
        # send priority event
        # game.give_player_priority(game.active_index())

    def next(self, event):
        pass
        # return give priority

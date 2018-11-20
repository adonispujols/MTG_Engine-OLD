import tkinter as tk
import abc
import random
import functools
import typing
from convert import game as game_mod
from convert import turn_parts as tp
from convert import bindings as bnd
from convert import events as ev


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
        # for user to choose (choose for ai in debug)
        for i in range(len(self._game.players)):
            choose_btn = tk.Button(self._game,
                                   text=i, command=functools.partial(self._game.advance, message=i))
            self._choose_btns.append(choose_btn)
            choose_btn.grid()
        # TODO give AI ability to choose and add debug choice to override

    def next(self, _):
        for btn in self._choose_btns:
            btn.destroy()
        self._choose_btns.clear()
        # [CR 103.4]
        for player in self._game.players:
            for _ in range(player.max_hand_size):
                player.draw()
        # [CR 103.7]
        return self._game.on_untap


class OnUntap(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self.first_untap = True

    def run(self, starting_player):
        self._game.step_or_phase = tp.TurnParts.UNTAP
        if self.first_untap:
            self._game.players[starting_player].make_active()
            self.first_untap = False
        else:
            prev_active = self._game.active_index()
            self._game.players[prev_active].make_inactive()
            new_active = (prev_active + 1) % len(self._game.players)
            self._game.players[new_active].make_active()
        self._game.reset_lands_played()
        self._game.untap_all_of_active()
        self._game.empty_mana_pools()
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.on_upkeep


class OnUpkeep(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.UPKEEP
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class InPriority(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self._init_gui()
        self.index = None

    def _init_gui(self):
        self._pass_button = tk.Button(self._game,
                                      text="pass", command=functools.partial(self._game.advance, event=ev.Events.PASS))

    def run(self, _):
        # TODO recall: need to give AI options here and elsewhere
        self._pass_button.grid()

    def next(self, event):
        self._pass_button.grid_remove()
        if event == ev.Events.PASS:
            return self._game.pass_priority(self.index)


# TODO need to skip on first turn of game
class OnDraw(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.DRAW
        self._game.active_player().draw()
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnPrecombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.PRECOMBAT_MAIN
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnBeginCombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.BEGIN_COMBAT
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


# TODO skip to end combat (or postcombat phase?) if none
class OnDeclareAttackers(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.DECLARE_ATTACKERS
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnDeclareBlockers(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.DECLARE_BLOCKERS
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


# TODO skip if none
class OnFirstStrikeDamage(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.FIRST_STRIKE_DAMAGE
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnCombatDamage(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.COMBAT_DAMAGE
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnEndCombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.END_COMBAT
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnPostcombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.POSTCOMBAT_MAIN
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnEndStep(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.END_STEP
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnCleanup(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.CLEANUP
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.on_untap

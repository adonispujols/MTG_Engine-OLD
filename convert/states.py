import tkinter as tk
import abc
import random
import functools
import typing
from convert import game as game_mod
from convert import turn_parts as tp
from convert import bindings as bnd
from convert import events as ev
from convert import hand as hand_mod

class State(abc.ABC):
    @abc.abstractmethod
    def run(self, message):
        pass

    @abc.abstractmethod
    def next(self, event):
        pass


class InPriority(State):
    card_buttons: typing.List["tk.Button"]

    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self._init_gui()
        self.index = None
        self.card_buttons = None

    def _init_gui(self):
        self._pass_button = tk.Button(self._game,
                                      text="pass", command=functools.partial(self._game.advance, event=ev.Events.PASS))

    def run(self, buttons_array):
        # TODO recall: need to give AI options here and elsewhere
        self._pass_button.grid()
        # XXX only passes hand index
        for i, button in enumerate(self.card_buttons):
            button.config(command=functools.partial(self._game.advance, event=ev.Events.PLAY, message=i))
        for button in self.card_buttons:
            button.config(state=tk.NORMAL)

    def next(self, event):
        self._pass_button.grid_remove()
        for button in self.card_buttons:
            button.config(state=tk.DISABLED)
        if event == ev.Events.PASS:
            return self._game.pass_priority(self.index)
        elif event == ev.Events.PLAY:
            self._game.playing_card.hand = self._game.players[self.index].hand
            self._game.playing_card.index = self.index
            return self._game.playing_card


class PlayingCard(State):
    hand: "hand_mod.Hand"

    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self.hand = None
        self.index = None

#     def _play(self, zone, card_index, p_index, p):
    #         card: "card_mod.Card" = zone.get(card_index)
    #         active = p.active
    #         if card.card_type == "Land":
    #             self._play_land(card, zone, card_index, p_index, active, p.under_land_limit(), p.lands_played)
    #         elif card.card_type == "Creature":
    #             self._cast_creature(card, zone, card_index, active, p.mana_pool)
    #     def _play_land(self, card, zone, card_index, player_index, active, under_land_limit, lands_played):
    #         # TODO ensure [CR 305.2b] and [CR 305.3]; NO effect bypasses "play land" restrictions.
    #         # ^ It's ok to increase max lands [CR 305.2], or "put" on battlefield [CR 305.4].
    #         # [CR 115.2a].2
    #         if self._met_land_restrictions(active, under_land_limit):
    #             # [CR 115.2a].1
    #             zone.remove(card_index)
    #             self.battlefield[player_index].append(card)
    #             lands_played.inc()
    #     def _met_land_restrictions(self, active, under_land_limit):
    #         return self._sorcery_speed(active) and under_land_limit
    # XXX card index restricted to hand
    # XXX many many other stuff missing
    def run(self, card_index):
        card = self.hand.get(card_index)
        player = self._game.players[self.index]
        # XXX this is just the "play land" code
        if self._game._met_land_restrictions(player.active, player.under_land_limit()):
            self.hand.remove(card_index)
            self._game.battlefield[self.index].append(card)
            player.lands_played.inc()
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, event):
        # XXX assuming player who played the stuff had priority
        return self._game.give_priority(self.index)


class ChoosingStartingPlayer(State):
    _player_label: "tk.Label"
    _choose_btns: typing.List["tk.Button"]

    def __init__(self, game: "game_mod.Game"):
        self._game = game
        self._choose_btns = []
        self._player_label = None

    def run(self, _):
        # [CR 103.2]
        index = random.randrange(len(self._game.players))
        self._player_label = tk.Label(self._game,
                                text="P{}, who goes first?".format(index))
        self._player_label.grid()
        # for user to choose (choose for ai in debug)
        for i in range(len(self._game.players)):
            choose_btn = tk.Button(self._game,
                                   text=i, command=functools.partial(self._game.advance, message=i))
            self._choose_btns.append(choose_btn)
            choose_btn.grid()
        # TODO give AI ability to choose and add debug choice to override

    def next(self, _):
        self._player_label.destroy()
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
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
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
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


# TODO need to skip on first turn of game
class OnDraw(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.DRAW
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.active_player().draw()
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnPrecombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.PRECOMBAT_MAIN
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnBeginCombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.BEGIN_COMBAT
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


# TODO skip to end combat (or postcombat phase?) if none
class OnDeclareAttackers(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.DECLARE_ATTACKERS
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnDeclareBlockers(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.DECLARE_BLOCKERS
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


# TODO skip if none
class OnFirstStrikeDamage(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.FIRST_STRIKE_DAMAGE
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnCombatDamage(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.COMBAT_DAMAGE
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnEndCombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.END_COMBAT
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnPostcombat(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.POSTCOMBAT_MAIN
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnEndStep(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.END_STEP
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.give_priority(self._game.active_index())


class OnCleanup(State):
    def __init__(self, game: "game_mod.Game"):
        self._game = game

    def run(self, _):
        self._game.step_or_phase = tp.TurnParts.CLEANUP
        self._game.step_or_phase_label.config(text=self._game.step_or_phase.name)
        self._game.event_generate(bnd.Bindings.ADVANCE.value, when="tail")

    def next(self, _):
        return self._game.on_untap

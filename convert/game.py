import typing
import collections
from convert import stack
from convert import hand
from convert import passes
from convert import deck
from convert import player as player_mod
from convert import card as card_mod
from convert import turn_parts as tp
from convert import mana_types as mt
from convert import states


class Game:
    players: typing.List["player_mod.Player"]
    battlefield: typing.List[typing.List["card_mod.Card"]]
    step_or_phase: "tp.TurnParts"
    _current_state: "states.State"

    def __init__(self, signals: collections.deque):
        self.signals = signals
        self._debug = True
        self._ai_only = False
        self.players = [player_mod.Player(), player_mod.Player()]
        self.battlefield = []
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # initially none until 1st turn
        self.step_or_phase = None
        self._init_game()
        self.in_priority = states.InPriority(self)
        self.playing_card = states.PlayingCard(self)
        self.on_untap = states.OnUntap(self)
        self.on_upkeep = states.OnUpkeep(self)
        self.on_draw = states.OnDraw(self)
        self.on_precombat = states.OnPrecombat(self)
        self.on_begin_combat = states.OnBeginCombat(self)
        self.on_declare_attackers = states.OnDeclareAttackers(self)
        self.on_declare_blockers = states.OnDeclareBlockers(self)
        self.on_first_strike_damage = states.OnFirstStrikeDamage(self)
        self.on_combat_damage = states.OnCombatDamage(self)
        self.on_end_combat = states.OnEndCombat(self)
        self.on_post_combat = states.OnPostcombat(self)
        self.on_end_step = states.OnEndStep(self)
        self.on_cleanup = states.OnCleanup(self)
        self._ON_STEP_OR_PHASE_STATES = (
            self.on_untap, self.on_upkeep, self.on_draw, self.on_precombat, self.on_begin_combat,
            self.on_declare_attackers, self.on_declare_blockers, self.on_first_strike_damage,
            self.on_combat_damage, self.on_end_combat, self.on_post_combat, self.on_end_step, self.on_cleanup)
        self._current_state = states.ChoosingStartingPlayer(self)
        self._current_state.run()

    def _init_game(self):
        self.players[0].deck = deck.Deck()
        self.players[0].hand = hand.Hand()
        self.players[1].deck = deck.Deck()
        self.players[1].hand = hand.Hand()
        for i in range(20):
            self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
            self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
        # for i in range(10):
            # self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
            # self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))
        for _ in self.players:
            self.battlefield.append([])
        # [CR 103.1], 1st part of starting game
        for player in self.players:
            player.deck.shuffle()

    def advance(self, event=None, message=None):
        # with deck
        # print("State: {}\nP0 HAND:\n{}\nP0 DECK\n{}\nP1 HAND:\n{}\nP1 DECK".format(
        #     self._current_state.__class__.__name__, self.players[0].hand, self.players[0].deck,
        #     self.players[1].hand, self.players[1].deck))
        # just field
        print("STATE: {}\nP0 HAND:\n{}\nP0 FIELD:\n{}\nP1 HAND:\n{}\nP1 FIELD:\n{}".format(
            self._current_state.__class__.__name__, self.players[0].hand, self.battlefield[0],
            self.players[1].hand, self.battlefield[1]))
        self._current_state = self._current_state.next(event)
        self._current_state.run(message)

    # main logic
    def active_index(self):
        for i, player in enumerate(self.players):
            if player.active:
                return i

    def active_player(self):
        return self.players[self.active_index()]

    def untap_all_of_active(self):
        for card in self.battlefield[self.active_index()]:
            card.untap()

    def reset_lands_played(self):
        for player in self.players:
            player.lands_played.reset()

    def empty_mana_pools(self):
        for player in self.players:
            player.mana_pool.empty()

    def give_priority(self, index):
        # TODO check for state based actions (perhaps make into separate state)
        self.in_priority.index = index
        # XXX can only play cards of player with priority
        return self.in_priority

    def pass_priority(self, index):
        self._passes.inc()
        next_player = (index + 1) % len(self.players)
        # TODO take into account actions + stack being empty.
        if self.players[next_player].active:
            if int(self._passes) == len(self.players):
                self._passes.reset()
                self.empty_mana_pools()
                # TODO will induce bug if we call while in cleanup step
                # ^ Could just directly call untap (clearer than a wrap around % here)
                return self._ON_STEP_OR_PHASE_STATES[self.step_or_phase.value + 1]
            self._passes.reset()
        return self.give_priority(next_player)
    #
    # def give_player_priority(self, index):
    #     def user_has_priority():
    #         while True:
    #             choice = input(print_u.player_prompt(index, self.players[index])).split()
    #             # TODO Include more general options for player (regardless of priority)
    #             # ^ such as simply looking at board state
    #             if not choice:
    #                 self._pass_priority(index)
    #                 break
    #             # TODO implement user-limited commands
    #             elif choice[0] == "play":
    #                 # TODO support playing from other zones
    #                 try:
    #                     card_index = int(choice[1])
    #                 except ValueError:
    #                     print("ERROR: Invalid integer")
    #                 except IndexError:
    #                     print("ERROR: Need 1 player # parameter, given 0")
    #                 else:
    #                     card_index -= 1
    #                     p = self.players[index]
    #                     if 0 <= card_index < p.hand.size():
    #                         self._play(p.hand, card_index, index, p)
    #                     else:
    #                         print("ERROR: Invalid card #")
    #             elif choice[0] == "act":
    #                 # TODO support for activating from other zones
    #                 try:
    #                     card_index = int(choice[1])
    #                 except ValueError:
    #                     print("ERROR: Invalid integer")
    #                 except IndexError:
    #                     print("ERROR: Need 1 player # parameter, given 0")
    #                 else:
    #                     card_index -= 1
    #                     p_field = self.battlefield[index]
    #                     if 0 <= card_index < len(p_field):
    #                         self._activate(p_field, card_index, self.players[index].mana_pool)
    #                     else:
    #                         print("ERROR: Invalid card #")
    #             elif choice[0] == "field":
    #                 print_u.print_field(self.battlefield)
    #             elif self._debug:
    #                 if choice[0] == "hand":
    #                     try:
    #                         p_index = int(choice[1])
    #                     except ValueError:
    #                         print("ERROR: Invalid integer")
    #                     except IndexError:
    #                         print("ERROR: Need 1 player # parameter, given 0")
    #                     else:
    #                         p_index -= 1
    #                         if 0 <= p_index < len(self.players):
    #                             print_u.print_hand(p_index, self.players[p_index])
    #                         else:
    #                             print("ERROR: Invalid player #")
    #                 else:
    #                     print("ERROR: Invalid input")
    #             else:
    #                 print("ERROR: Invalid input")
    #     if index == 0:
    #         if not self._ai_only:
    #             user_has_priority()
    #         else:
    #             # TODO continue adding AI options in future!
    #             # ai is making choice
    #             pass
    #     else:
    #         if self._debug:
    #             user_has_priority()
    #         else:
    #             pass

    def _in_main_phase(self):
        return (self.step_or_phase == tp.TurnParts.PRECOMBAT_MAIN
                or self.step_or_phase == tp.TurnParts.POSTCOMBAT_MAIN)

    def _sorcery_speed(self, active):
        return active and self._in_main_phase() and self._stack.empty()

    def _met_land_restrictions(self, active, under_land_limit):
        return self._sorcery_speed(active) and under_land_limit

    def _met_creature_restrictions(self, active):
        # [CR 302.1].?
        return self._sorcery_speed(active)

    def _play(self, zone, card_index, p_index, p):
        card: "card_mod.Card" = zone.get(card_index)
        active = p.active
        if card.card_type == "Land":
            self._play_land(card, zone, card_index, p_index, active, p.under_land_limit(), p.lands_played)
        elif card.card_type == "Creature":
            self._cast_creature(card, zone, card_index, active, p.mana_pool)

    def _cast_creature(self, card, zone, card_index, active, mana_pool):
        # TODO [CR 601.3a] to [CR 601.3b] (exceptions to casting restrictions)
        # TODO check for legality at [CR 601.2e], not before!
        # XXX can add somewhat-accurate hints (warn sorcery/instant, etc), but
        # - allow user to try (until completely accurate).
        # TODO deque for actions (resolve as queue, undo as stack)
        # ^ Try bluff (no-sde effect) payments, "undo" by doing reverse, and then
        # "do real" in queue order once all costs are payed.
        # [CR 601.2e]
        if self._met_creature_restrictions(active):
            # [CR 601.2a]
            zone.remove(card_index)
            self._stack.push(card)
            # TODO [601.2g] only part where mana abilities may be activated during cast/act
            # [CR 601.2h] paying total cost
            generic_cost = 1
            specific_types = {mt.ManaTypes.G: 1}
            while True:
                mana_payed = input("Pay Mana: ")
                try:
                    mana_payed = mt.ManaTypes[mana_payed]
                except KeyError:
                    print("ERROR: Invalid input")
                else:
                    if mana_pool.remove(mana_payed):
                        if (mana_payed in specific_types) and (specific_types[mana_payed] > 0):
                            specific_types[mana_payed] -= 1
                        elif generic_cost > 0:
                            generic_cost -= 1
                        else:
                            # TODO use LBYL and/or try "reversing" illegal actions
                            raise ValueError("ILLEGAL ACTION: Mana removed for improper type (generic costs payed).")
                            # print("ERROR: Generic costs payed. Missing specific type.")
                        if all(i == 0 for i in specific_types.values()) and (generic_cost == 0):
                            break
                    else:
                        print("ERROR: You can't pay that mana.")
            # [CR 601.2i] successfully cast

    def _play_land(self, card, zone, card_index, player_index, active, under_land_limit, lands_played):
        # TODO ensure [CR 305.2b] and [CR 305.3]; NO effect bypasses "play land" restrictions.
        # ^ It's ok to increase max lands [CR 305.2], or "put" on battlefield [CR 305.4].
        # [CR 115.2a].2
        if self._met_land_restrictions(active, under_land_limit):
            # [CR 115.2a].1
            zone.remove(card_index)
            self.battlefield[player_index].append(card)
            lands_played.inc()

    # noinspection PyMethodMayBeStatic
    def _activate(self, zone, card_index, mana_pool):
        # TODO [CR 605.3c] mana ability must resolve completely before activating it again
        card: "card_mod.Card" = zone[card_index]
        if card.ability == "{T}: Add G":
            # [CR 605.3] -> [CR 602.2b] -> TODO [CR 601.2b]
            # [CR 601.2h] paying costs
            if card.tap():
                # [CR 601.2i] successfully activated
                # [CR 605.3a] resolve immediately after activation
                mana_pool.add(mt.ManaTypes.G)
                # TODO [CR 116.3c] ONLY receive priority after cast/act/action IF had it before

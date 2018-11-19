import tkinter as tk
import typing
from convert import stack
from convert import hand
from convert import passes
from convert import deck
from convert import player as player_mod
from convert import card as card_mod
from convert import turn_actions
from convert import turn_parts as tp
from convert import mana_types as mt
from convert import states
from convert import bindings as bnd

class Game(tk.Frame):
    players: typing.List["player_mod.Player"]
    battlefield: typing.List[typing.List["card_mod.Card"]]
    step_or_phase: "tp.TurnParts"
    current_state: "states.State"

    def __init__(self, parent=None):
        # gui
        super().__init__(parent)
        self.parent = parent
        self.init_gui()
        # main logic
        self.debug = True
        self.ai_only = False
        self.players = [player_mod.Player(), player_mod.Player()]
        self.battlefield = []
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # initially none until 1st turn
        self.step_or_phase = None
        # state machine
        self.choosing_starting_player = states.ChoosingStartingPlayer(self)
        self.on_first_untap = states.OnFirstUntap(self)
        self.on_upkeep = states.OnUpkeep(self)
        self.on_give_priority = states.OnGivePriority(self)
        self.current_state = self.choosing_starting_player
        self.init_game()

    # gui
    def init_gui(self):
        self.grid()
        # noinspection PyAttributeOutsideInit
        self.test_btn = tk.Button(self, text="test", command=None)
        # alt definition of parameters (might only work BEFORE mainloop() starts)
        # self.hi_there["text"] = "test"
        self.test_btn.grid()
        # root.bind("<<Foo>>", okay)
        self.bind(bnd.Bindings.ADVANCE.value, self.advance())

    # state machine
    def advance(self, event=None):
        self.current_state = self.current_state.next(event)
        self.current_state.run()

    # main logic
    def init_game(self):
        self.players[0].deck = deck.Deck()
        self.players[0].hand = hand.Hand()
        self.players[1].deck = deck.Deck()
        self.players[1].hand = hand.Hand()
        for i in range(10):
            self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
            self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
        for i in range(10):
            self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
            self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))
        for _ in self.players:
            self.battlefield.append([])
        # [CR 103.1], 1st part of starting game
        for player in self.players:
            player.deck.shuffle()

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

    # TODO Obviously horrible, doesn't end, and needs a touch up:
    def _pass_priority(self, index):
        self._passes.inc()
        next_player = self.players[(index + 1) % len(self.players)]
        # TODO take into account actions + stack being empty.
        if next_player.active:
            if int(self._passes) == len(self.players):
                self._passes.reset()
                self.empty_mana_pools()
                turn_actions.start_next_step_or_phase(self, self.step_or_phase)
            self._passes.reset()
        else:
            self.give_player_priority((index + 1) % len(self.players))

    def give_player_priority(self, index):
        def user_has_priority():
            while True:
                choice = input(print_u.player_prompt(index, self.players[index])).split()
                # TODO Include more general options for player (regardless of priority)
                # ^ such as simply looking at board state
                if not choice:
                    self._pass_priority(index)
                    break
                # TODO implement user-limited commands
                elif choice[0] == "play":
                    # TODO support playing from other zones
                    try:
                        card_index = int(choice[1])
                    except ValueError:
                        print("ERROR: Invalid integer")
                    except IndexError:
                        print("ERROR: Need 1 player # parameter, given 0")
                    else:
                        card_index -= 1
                        p = self.players[index]
                        if 0 <= card_index < p.hand.size():
                            self._play(p.hand, card_index, index, p)
                        else:
                            print("ERROR: Invalid card #")
                elif choice[0] == "act":
                    # TODO support for activating from other zones
                    try:
                        card_index = int(choice[1])
                    except ValueError:
                        print("ERROR: Invalid integer")
                    except IndexError:
                        print("ERROR: Need 1 player # parameter, given 0")
                    else:
                        card_index -= 1
                        p_field = self.battlefield[index]
                        if 0 <= card_index < len(p_field):
                            self._activate(p_field, card_index, self.players[index].mana_pool)
                        else:
                            print("ERROR: Invalid card #")
                elif choice[0] == "field":
                    print_u.print_field(self.battlefield)
                elif self.debug:
                    if choice[0] == "hand":
                        try:
                            p_index = int(choice[1])
                        except ValueError:
                            print("ERROR: Invalid integer")
                        except IndexError:
                            print("ERROR: Need 1 player # parameter, given 0")
                        else:
                            p_index -= 1
                            if 0 <= p_index < len(self.players):
                                print_u.print_hand(p_index, self.players[p_index])
                            else:
                                print("ERROR: Invalid player #")
                    else:
                        print("ERROR: Invalid input")
                else:
                    print("ERROR: Invalid input")
        if index == 0:
            if not self.ai_only:
                user_has_priority()
            else:
                # TODO continue adding AI options in future!
                # ai is making choice
                pass
        else:
            if self.debug:
                user_has_priority()
            else:
                pass

    def empty_mana_pools(self):
        for player in self.players:
            player.mana_pool.empty()

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
                mana_pool.add(mt.ManaTypes.G.value)
                # TODO [CR 116.3c] ONLY receive priority after cast/act/action IF had it before

# import typing
# from new_src.convert import passes
# from new_src.convert import turn_actions
# from new_src.convert import turn_parts as tp
# from new_src.convert import player as player_mod
# from new_src.convert import stack
# from new_src.convert import card as card_mod
# from new_src.convert import print_utils as print_u
# from new_src.convert import mana_types as mt
# from new_src.convert import deck
# from new_src.convert import hand
#
#
# class Game:
#     step_or_phase: "tp.TurnParts"
#     battlefield: typing.List[typing.List["card_mod.Card"]]
#     players: typing.List["player_mod.Player"]
#
#     def __init__(self):
#         self.debug = True
#         self.ai_only = False
#         self.players = [player_mod.Player(), player_mod.Player()]
#         self.players[0].deck = deck.Deck()
#         self.players[0].hand = hand.Hand()
#         self.players[1].deck = deck.Deck()
#         self.players[1].hand = hand.Hand()
#         self._fill_decks()
#         self.battlefield = []
#         self._init_battlefield()
#         self._stack = stack.Stack()
#         self._passes = passes.Passes()
#         # initially none until 1st turn
#         self.step_or_phase = None
#
#     def _fill_decks(self):
#         for i in range(10):
#             self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
#             self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
#         for i in range(10):
#             self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
#             self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))
#
#     def _init_battlefield(self):
#         for _ in self.players:
#             self.battlefield.append([])
#
#     def _print_hand_and_decks(self):
#         for i, player in enumerate(self.players):
#             print("P" + str(i + 1), "HAND:\n", player.hand,
#                   "\nP" + str(i + 1), "DECK:\n", player.deck)
#
#     def _in_main_phase(self):
#         return (self.step_or_phase == tp.TurnParts.PRECOMBAT_MAIN
#                 or self.step_or_phase == tp.TurnParts.POSTCOMBAT_MAIN)
#
#     def _sorcery_speed(self, active):
#         return active and self._in_main_phase() and self._stack.empty()
#
#     def _met_land_restrictions(self, active, under_land_limit):
#         return self._sorcery_speed(active) and under_land_limit
#
#     def _met_creature_restrictions(self, active):
#         # [CR 302.1].?
#         return self._sorcery_speed(active)
#
#     def active_index(self):
#         for i, player in enumerate(self.players):
#             if player.active:
#                 return i
#
#     def active_player(self):
#         return self.players[self.active_index()]
#
#     def untap_all_of_active(self):
#         for card in self.battlefield[self.active_index()]:
#             card.untap()
#
#     def reset_lands_played(self):
#         for player in self.players:
#             player.lands_played.reset()
#
#     # TODO Obviously horrible, doesn't end, and needs a touch up:
#     def _pass_priority(self, index):
#         self._passes.inc()
#         next_player = self.players[(index + 1) % len(self.players)]
#         # TODO take into account actions + stack being empty.
#         if next_player.active:
#             if int(self._passes) == len(self.players):
#                 self._passes.reset()
#                 self.empty_mana_pools()
#                 turn_actions.start_next_step_or_phase(self, self.step_or_phase)
#             self._passes.reset()
#         else:
#             self.give_player_priority((index + 1) % len(self.players))
#
#     def give_player_priority(self, index):
#         def user_has_priority():
#             while True:
#                 choice = input(print_u.player_prompt(index, self.players[index])).split()
#                 # TODO Include more general options for player (regardless of priority)
#                 # ^ such as simply looking at board state
#                 if not choice:
#                     self._pass_priority(index)
#                     break
#                 # TODO implement user-limited commands
#                 elif choice[0] == "play":
#                     # TODO support playing from other zones
#                     try:
#                         card_index = int(choice[1])
#                     except ValueError:
#                         print("ERROR: Invalid integer")
#                     except IndexError:
#                         print("ERROR: Need 1 player # parameter, given 0")
#                     else:
#                         card_index -= 1
#                         p = self.players[index]
#                         if 0 <= card_index < p.hand.size():
#                             self._play(p.hand, card_index, index, p)
#                         else:
#                             print("ERROR: Invalid card #")
#                 elif choice[0] == "act":
#                     # TODO support for activating from other zones
#                     try:
#                         card_index = int(choice[1])
#                     except ValueError:
#                         print("ERROR: Invalid integer")
#                     except IndexError:
#                         print("ERROR: Need 1 player # parameter, given 0")
#                     else:
#                         card_index -= 1
#                         p_field = self.battlefield[index]
#                         if 0 <= card_index < len(p_field):
#                             self._activate(p_field, card_index, self.players[index].mana_pool)
#                         else:
#                             print("ERROR: Invalid card #")
#                 elif choice[0] == "field":
#                     print_u.print_field(self.battlefield)
#                 elif self.debug:
#                     if choice[0] == "hand":
#                         try:
#                             p_index = int(choice[1])
#                         except ValueError:
#                             print("ERROR: Invalid integer")
#                         except IndexError:
#                             print("ERROR: Need 1 player # parameter, given 0")
#                         else:
#                             p_index -= 1
#                             if 0 <= p_index < len(self.players):
#                                 print_u.print_hand(p_index, self.players[p_index])
#                             else:
#                                 print("ERROR: Invalid player #")
#                     else:
#                         print("ERROR: Invalid input")
#                 else:
#                     print("ERROR: Invalid input")
#         if index == 0:
#             if not self.ai_only:
#                 user_has_priority()
#             else:
#                 # TODO continue adding AI options in future!
#                 # ai is making choice
#                 pass
#         else:
#             if self.debug:
#                 user_has_priority()
#             else:
#                 pass
#
#     def empty_mana_pools(self):
#         for player in self.players:
#             player.mana_pool.empty()
#
#     def _play(self, zone, card_index, p_index, p):
#         card: "card_mod.Card" = zone.get(card_index)
#         active = p.active
#         if card.card_type == "Land":
#             self._play_land(card, zone, card_index, p_index, active, p.under_land_limit(), p.lands_played)
#         elif card.card_type == "Creature":
#             self._cast_creature(card, zone, card_index, active, p.mana_pool)
#
#     def _cast_creature(self, card, zone, card_index, active, mana_pool):
#         # TODO [CR 601.3a] to [CR 601.3b] (exceptions to casting restrictions)
#         # TODO check for legality at [CR 601.2e], not before!
#         # XXX can add somewhat-accurate hints (warn sorcery/instant, etc), but
#         # - allow user to try (until completely accurate).
#         # TODO deque for actions (resolve as queue, undo as stack)
#         # ^ Try bluff (no-sde effect) payments, "undo" by doing reverse, and then
#         # "do real" in queue order once all costs are payed.
#         # [CR 601.2e]
#         if self._met_creature_restrictions(active):
#             # [CR 601.2a]
#             zone.remove(card_index)
#             self._stack.push(card)
#             # TODO [601.2g] only part where mana abilities may be activated during cast/act
#             # [CR 601.2h] paying total cost
#             generic_cost = 1
#             specific_types = {mt.ManaTypes.G: 1}
#             while True:
#                 mana_payed = input("Pay Mana: ")
#                 try:
#                     mana_payed = mt.ManaTypes[mana_payed]
#                 except KeyError:
#                     print("ERROR: Invalid input")
#                 else:
#                     if mana_pool.remove(mana_payed):
#                         if (mana_payed in specific_types) and (specific_types[mana_payed] > 0):
#                             specific_types[mana_payed] -= 1
#                         elif generic_cost > 0:
#                             generic_cost -= 1
#                         else:
#                             # TODO use LBYL and/or try "reversing" illegal actions
#                             raise ValueError("ILLEGAL ACTION: Mana removed for improper type (generic costs payed).")
#                             # print("ERROR: Generic costs payed. Missing specific type.")
#                         if all(i == 0 for i in specific_types.values()) and (generic_cost == 0):
#                             break
#                     else:
#                         print("ERROR: You can't pay that mana.")
#             # [CR 601.2i] successfully cast
#
#     def _play_land(self, card, zone, card_index, player_index, active, under_land_limit, lands_played):
#         # [CR 115.2a].2
#         if self._met_land_restrictions(active, under_land_limit):
#             # [CR 115.2a].1
#             zone.remove(card_index)
#             self.battlefield[player_index].append(card)
#             lands_played.inc()
#
#     # noinspection PyMethodMayBeStatic
#     def _activate(self, zone, card_index, mana_pool):
#         # TODO [CR 605.3c] mana ability must resolve completely before activating it again
#         card: "card_mod.Card" = zone[card_index]
#         if card.ability == "{T}: Add G":
#             # [CR 605.3] -> [CR 602.2b] -> TODO [CR 601.2b]
#             # [CR 601.2h] paying costs
#             if card.tap():
#                 # [CR 601.2i] successfully activated
#                 # [CR 605.3a] resolve immediately after activation
#                 mana_pool.add(mt.ManaTypes.G.value)
#                 # TODO [CR 116.3c] ONLY receive priority after cast/act/action IF had it before

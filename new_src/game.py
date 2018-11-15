import typing
from new_src import passes
from new_src import turn_actions
from new_src import turn_parts as tp
from new_src import player as player_mod
from new_src import stack
from new_src import card as card_mod
from new_src import print_utils as print_u
from new_src import mana_types as mt


class Game:
    step_or_phase: "tp.TurnParts"
    battlefield: typing.List[typing.List["card_mod.Card"]]
    players: typing.List["player_mod.Player"]

    def __init__(self):
        self.debug = False
        self.ai_only = False
        self.players = None
        self.battlefield = None
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # initially none until 1st turn
        self.step_or_phase = None

    def _print_hand_and_decks(self):
        for i, player in enumerate(self.players):
            print("P" + str(i + 1), "HAND:\n", player.hand,
                  "\nP" + str(i + 1), "DECK:\n", player.deck)

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

    # XXX Make index a player property? <- Need to track deaths, then
    # XXX make card index a property?
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

    def give_player_priority(self, index):
        # TODO WRONG WRONG WRONG!
        # ONLY CHECKPASSES IF ACTUALLY PASSED PRIORITY
        # TODO WRONG WRONG WRONG!
        # ONLY CHECKPASSES IF ACTUALLY PASSED PRIORITY
        # TODO WRONG WRONG WRONG!
        # ONLY CHECKPASSES IF ACTUALLY PASSED PRIORITY
        # MAKE A PASS PRIORITY FUNCTION SEPARATE FROM THIS!
        if (int(self._passes) == len(self.players)) and self._stack.empty():
            # TODO only move forward if stack is empty, otherwise resolve top.
            self._passes.reset()
            self.empty_mana_pools()
            turn_actions.start_next_step_or_phase(self, self.step_or_phase)
        else:
            def user_has_priority():
                while True:
                    choice = input(print_u.player_prompt(index, self.players[index])).split()
                    # TODO Include more general options for player (regardless of priority)
                    # ^ such as simply looking at board state
                    if not choice:
                        self._passes.inc()
                        self.give_player_priority((index + 1) % len(self.players))
                        break
                    # TODO implement user-limited commands
                    # TODO play(card)
                    elif choice[0] == "play":
                        # TODO allow for playing from other zones
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
                    # TODO activate ability
                    elif choice[0] == "act":
                        # TODO allow for activating from other zones
                        try:
                            card_index = int(choice[1])
                        except ValueError:
                            print("ERROR: Invalid integer")
                        except IndexError:
                            print("ERROR: Need 1 player # parameter, given 0")
                        else:
                            card_index -= 1
                            # TODO activation from other zones support
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
                                p_index = int(choice[1]) - 1
                            except ValueError:
                                print("ERROR: Invalid integer")
                            except IndexError:
                                print("ERROR: Need 1 player # parameter, given 0")
                            else:
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
            self._play_land(card, zone, card_index, p_index, active, p.under_land_limit, p.lands_played)
        elif card.card_type == "Creature":
            self._play_creature(card, zone, card_index, active, p.mana_pool)

    def _play_creature(self, card, zone, card_index, active, mana_pool):
        zone.remove(card_index)
        self._stack.push(card)
        # [CR 601.2e]
        if self._met_creature_restrictions(active):
            payed_costs = False
            # XXX make mana types more verbose "Green" and simpler?
            generic_cost = 1
            specific_types = {mt.ManaTypes.G.name: 1}
            while not payed_costs:
                mana_payed = input("Pay Mana: ")
                if mana_payed in mt.ManaTypes.__members__:
                    if mana_pool.remove(mana_payed):
                        if (mana_payed in specific_types) and (specific_types[mana_payed] > 0):
                            specific_types[mana_payed] -= 1
                        elif generic_cost > 0:
                            generic_cost -= 1
                        else:
                            print("ERROR: Generic costs payed. Missing specific type.")
                        if all(i == 0 for i in specific_types.values()) and (generic_cost == 0):
                            break
                    else:
                        print("ERROR: You can't pay that mana.")
                else:
                    print("ERROR: Invalid input")
            # [CR 601.2i] successfully cast

    def _play_land(self, card, zone, card_index, player_index, active, under_land_limit, lands_played):
        # [CR 115.2a].2
        if self._met_land_restrictions(active, under_land_limit):
            # [CR 115.2a].1
            zone.remove(card_index)
            self.battlefield[player_index].append(card)
            lands_played.inc()

    def _activate(self, zone, card_index, mana_pool):
        # TODO [CR 605.3c] mana ability must resolve completely before activating it again
        card: "card_mod.Card" = zone[card_index]
        if card.ability == "{T}: Add G":
            # [CR 605.3] -> [CR 602.2b] -> TODO [CR 601.2b]
            # TODO [601.2g] only part where mana abilities may be activated
            # [CR 601.2h] paying costs
            if card.tap():
                # [CR 601.2i] officially activated
                # [CR 605.3a] resolve immediately after activation
                mana_pool.add(mt.ManaTypes.G.value)
                # TODO [CR 116.3c] ONLY receive priority after cast/act/action IF had it before

import typing
from KISS import stack
from KISS import hand
from KISS import passes
from KISS import deck
from KISS import player as player_mod
from KISS import card as card_mod
from KISS import turn_parts as tp
from KISS import turn_actions
from KISS import mana_types as mt
from KISS import signals
from KISS import signal_handler as signal_handler_mod


class Game:
    players: typing.List["player_mod.Player"]
    battlefield: typing.List[typing.List["card_mod.Card"]]
    step_or_phase: "tp.TurnParts"

    def __init__(self, signal_handler: "signal_handler_mod.SignalHandler"):
        self.signal_handler = signal_handler
        self._debug = True
        self._ai_only = False
        self.players = [player_mod.Player(), player_mod.Player()]
        self.battlefield = []
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        self.step_or_phase = None
        self.players[0].deck = deck.Deck()
        self.players[0].hand = hand.Hand()
        self.players[1].deck = deck.Deck()
        self.players[1].hand = hand.Hand()
        for i in range(20):
            self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
            self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
        # for i in range(10):
        #     self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
        #     self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))
        for _ in self.players:
            self.battlefield.append([])

    def start_game(self):
        # [CR 103.1], official 1st part of starting game
        for player in self.players:
            player.deck.shuffle()
        # [CR 103.2]
        self.signal_handler.emit_signal(signals.ChooseStartingPlayer(self.finish_starting, len(self.players)))

    def finish_starting(self, starting_player):
        # [CR 103.4]
        for player in self.players:
            for _ in range(player.max_hand_size):
                player.draw()
        # [CR 103.7]
        turn_actions.first_untap(self, starting_player)
            
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
        self.signal_handler.emit_signal(signals.InPriority(self, index))

    def pass_priority(self, index):
        self._passes.inc()
        next_player = (index + 1) % len(self.players)
        # TODO take into account stack being empty and have actions reset count
        if self.players[next_player].active:
            if int(self._passes) == len(self.players):
                self._passes.reset()
                self.empty_mana_pools()
                turn_actions.start_next_step_or_phase(self, self.step_or_phase)
            self._passes.reset()
        # TODO MUST BE ELSE! IF TURN IS SWITCHING, THEN TURN ACTIONS TAKES CARE OF PRIORITY!
        # ^ WITHOUT THIS ELSE, WE'RE GIVING PRIORITY TWICE! (or overriding effect of turn actions)!!!
        else:
            self.give_priority(next_player)

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

    # XXX have zone/index in zone be in card?
    # ^ Makes it easier for us to just pass the card itself, but may be more complicated...
    def play(self, zone, card_index, p_index):
        card: "card_mod.Card" = zone.get(card_index)
        player: "player_mod.Player" = self.players[p_index]
        if card.card_type == "Land":
            self._play_land(card, zone, card_index, p_index, player)
        elif card.card_type == "Creature":
            self._cast_creature(card, zone, card_index, player)

    def _cast_creature(self, card, zone, card_index, player):
        # TODO [CR 601.3a] to [CR 601.3b] (exceptions to casting restrictions)
        # TODO check for legality at [CR 601.2e], not before! <- We kinda have this going.
        # XXX can add somewhat-accurate hints (warn sorcery/instant, etc), but
        # - allow user to try (until completely accurate).
        # TODO deque for actions (resolve as queue, undo as stack)
        # ^ Try bluff (no-sde effect) payments, "undo" by doing reverse, and then
        # "do real" in queue order once all costs are payed.
        # [CR 601.2a]
        zone.remove(card_index)
        self._stack.push(card)
        # [CR 601.2e]
        if self._met_creature_restrictions(player.active):
            # TODO PAYING COSTS STATE!!!!!!!!!
            # TODO PAYING COSTS STATE!!!!!!!!!
            # TODO PAYING COSTS STATE!!!!!!!!!
            # TODO GETTING PRIORITY BACK!!!!!!
            # TODO GETTING PRIORITY BACK!!!!!!
            # TODO GETTING PRIORITY BACK!!!!!!
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
                    if player.mana_pool.remove(mana_payed):
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
        else:
            raise ValueError("ILLEGAL ACTION: Casting spell without proper timing")
        # TODO [CR 116.3c] receive priority after cast/act/action IF had it before

    def _play_land(self, card, zone, card_index, player_index, player):
        # TODO ensure [CR 305.2b] and [CR 305.3]; NO effect bypasses "play land" restrictions.
        # ^ It's ok to increase max lands [CR 305.2], or "put" on battlefield [CR 305.4].
        # [CR 115.2a].2
        if self._met_land_restrictions(player.active, player.under_land_limit()):
            # [CR 115.2a].1
            # TODO need general zone object?
            zone.remove(card_index)
            self.battlefield[player_index].append(card)
            player.lands_played.inc()
        # TODO [CR 116.3c] receive priority after cast/act/action IF had it before

    # noinspection PyMethodMayBeStatic
    def _activate(self, zone, card_index, player: "player_mod.Player"):
        # TODO [CR 605.3c] mana ability must resolve completely before activating it again
        card: "card_mod.Card" = zone[card_index]
        if card.ability == "{T}: Add G":
            # [CR 605.3] -> [CR 602.2b] -> TODO [CR 601.2b]
            # [CR 601.2h] paying costs
            if card.tap():
                # [CR 601.2i] successfully activated
                # [CR 605.3a] resolve immediately after activation
                player.mana_pool.add(mt.ManaTypes.G)
                # TODO [CR 116.3c] ONLY receive priority after cast/act/action IF had it before

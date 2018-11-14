import typing
from new_src import passes
from new_src import turn_actions
from new_src import turn_parts as tp
from new_src import player as player_mod
from new_src import stack
from new_src import card as card_mod
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


class Game:
    battlefield: typing.List[typing.List["card_mod.Card"]]
    players: typing.List["player_mod.Player"]

    def __init__(self):
        self.debug = False
        self.ai_only = False
        self.players = None
        self.battlefield = None
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # Initially none since game isn't at untap yet (officially)
        self.step_or_phase = None

    def _print_hand_and_decks(self):
        # XXX Use ID when comparing objects (as you should)
        for i, player in enumerate(self.players):
            print("P" + str(i + 1), "HAND:\n", player.hand,
                  "\nP" + str(i + 1), "DECK:\n", player.deck)

    def _print_hand(self, index):
        print("P" + str(index + 1), "HAND:\n", self.players[index].hand)

    def _player_prompt(self, index):
        return "{} P{:d}: ".format(("A" if self.players[index].active else "N"), index + 1)

    def _in_main_phase(self):
        return (self.step_or_phase == tp.TurnParts.PRECOMBAT_MAIN
                or self.step_or_phase == tp.TurnParts.POSTCOMBAT_MAIN)

    def _sorcery_speed(self, is_active):
        return is_active and self._in_main_phase() and self._stack.is_empty()

    def _met_land_restrictions(self, index):
        return self._sorcery_speed(self.players[index].active)\
               and self.players[index].under_land_limit()

    def active_index(self):
        # XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
        for i, player in enumerate(self.players):
            if player.active:
                return i

    def active_player(self):
        return self.players[self.active_index()]

    def untap_all_of_active(self):
        for card in self.battlefield[self.active_index()]:
            card.untap()

    def give_player_priority(self, index):
        if int(self._passes) != len(self.players):
            def user_has_priority():
                while True:
                    choice = input(self._player_prompt(index)).split()
                    # TODO here is where we add more choices for player
                    # ^ either actions requiring priority (play, activate, pass, etc)
                    # ^ OR ability to look at game state
                    # ^^ XXX could organize ALL input asks such that:
                    # ^^ user may always look at the board state before a choice
                    if not choice:
                        self._passes.inc()
                        self.give_player_priority((index + 1) % len(self.players))
                        break
                    # TODO implement user-limited commands (no debug)
                    # ^ normally, user's knowledge of game is limited
                    # ^ he can't just randomly search through hands, decks, etc
                    # ^ EX: "hand-self" prints own hand of player
                    # TODO play(card)
                    elif choice[0] == "play":
                        # TODO allow for playing from other zones
                        # player chooses a card from a zone (just hand for now)
                        try:
                            # enter card # in hand (counting left to right)
                            card_index = int(choice[1]) - 1
                        except ValueError:
                            print("ERROR: Invalid integer")
                        except IndexError:
                            print("ERROR: Need 1 player # parameter, given 0")
                        else:
                            # XXX maybe we should push this player def. up?
                            # Should we keep direct access to players or so?
                            # ^ Is that even possible (if not using array)?
                            p = self.players[index]
                            if 0 <= card_index < p.hand.size():
                                self.play(p.hand, card_index, index)
                    elif self.debug:
                        # XXX Our code ignores extra input after what is understood
                        # ^ I.e., "hand 0 asdf" is translated as "hand 0"
                        if choice[0] == "hand":
                            # XXX make a general "valid player index" method?
                            try:
                                p_index = int(choice[1]) - 1
                            except ValueError:
                                print("ERROR: Invalid integer")
                            except IndexError:
                                print("ERROR: Need 1 player # parameter, given 0")
                            else:
                                # XXX Apply EAFP ONLY when validating input, NOT LOGIC!
                                # ^ I.e., checking for int/params is FINE! BUT we
                                # ^ can't allow for irreversible game states by allowing
                                # ^ invalid actions to run until error is caught!!!
                                # - Essentially: Preemptively stop illegal game states
                                # - from existing!
                                if 0 <= p_index < len(self.players):
                                    self._print_hand(p_index)
                                else:
                                    print("ERROR: Invalid player #")
                        # could we combine this error message w/ final else?
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
        # TODO need to take into account actions taken in between passes!
        else:
            # MUST RESET PASSES (else we're stuck in infinite loop)
            self._passes.reset()
            turn_actions.start_next_step_or_phase(self, self.step_or_phase)

    # TODO don't pass index if you need the player (modify an attribute)
    def play(self, zone, card_index, player_index):
        card = zone.get(card_index)
        if card.type == "Land":
            if self._met_land_restrictions(player_index):
                # put on battlefield (typically from hand)
                # need to move it from previous zone to battlefield
                zone.remove(card_index)
                self.battlefield[player_index].append(card)
                # TODO ACTUALLT INCREMENT LANDS PLAYED
                # TODO ACTUALLT INCREMENT LANDS PLAYED
                # TODO ACTUALLT INCREMENT LANDS PLAYED
        # if card.type == "Creature"
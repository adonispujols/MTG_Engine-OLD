from new_src import passes
from new_src import turn_actions
import typing
from new_src import player as player_mod
# XXX avoid importing just for type checking (risks cyclic importing)


class Game:
    players: typing.List[player_mod.Player]

    def __init__(self):
        self._debug = False
        self._ai_only = False
        self.players = None
        self._battlefield = None
        # XXX Better to cluster functions to a module, then clutter
        # ^ this namespace with functions related ONLY to that object!
        self._passes = passes.Passes()
        # Initially none since game isn't at untap yet (officially)
        self.step_or_phase = None
        # XXX DO NOT SET STATIC MODULES/CLASSES TO FIELD. JUST CALL IT!
        # We only "init" actual instances, not some helper method/constants!

    # print methods
    def _print_hand_and_decks(self):
        # some objects have __repr__ defined (to simplify printing)
        # XXX Use ID when comparing objects (as you should)
        for i, player in enumerate(self.players):
            print("P" + str(i + 1), "HAND:\n", player.hand,
                  "\nP" + str(i + 1), "DECK:\n", player.deck)

    def _print_hand(self, index):
        print("P" + str(index + 1), "HAND:\n", self.players[index].hand)

    # methods/classes to use during game
    def active_index(self):
        # XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
        for i, player in enumerate(self.players):
            if player.active:
                return i

    def active_player(self):
        return self.players[self.active_index()]

    # untap all of active player's permanents
    def untap_all_of_active(self):
        for card in self._battlefield[self.active_index()]:
            card.untap()

    def give_player_priority(self, index):
        if self._passes.count != len(self.players):
            # ask the user for input
            def user_has_priority():
                while True:
                    # splits choice into string list, separated by whitespaces
                    choice = input("P" + str(index + 1) + ": ").split()
                    # TODO here is where we add more choices for player
                    # ^ either actions requiring priority (play, activate, pass, etc)
                    # ^ OR ability to look at game state
                    # ^^ XXX could organize ALL input asks such that:
                    # ^^ user may always look at the board state before a choice
                    # if just pressed enter (entered no input)
                    if not choice:
                        self._passes.inc()
                        self.give_player_priority((index + 1) % len(self.players))
                        break
                    # list of options available (debugging or not)
                    # TODO implement user-limited commands (no debug)
                    # ^ normally, user's knowledge of game is limited
                    # ^ he can't just randomly search through hands, decks, etc
                    # ^ EX: hand-self prints own hand of player
                    # TODO play(card)
                    elif choice[0] == "TODO":
                        pass
                    elif self._debug:
                        # list of options available only if debugging
                        if choice[0] == "hand":
                            # XXX make a general "valid player index" method?
                            try:
                                # index<_n> are just aliases for player index
                                index_1 = int(choice[1]) - 1
                            except ValueError:
                                print("ERROR: Invalid integer")
                            except IndexError:
                                print("ERROR: Need 1 Player # parameter, given 0")
                            else:
                                # XXX Apply EAFP ONLY when validating input, NOT LOGIC!
                                # ^ I.e., checking for int/params is FINE! BUT we
                                # ^ can't allow for irreversible game states by allowing
                                # ^ invalid actions to run until error is caught!!!
                                # - Essentially: Preemptively stop illegal game states
                                # - from existing!
                                if 0 <= index_1 < len(self.players):
                                    self._print_hand(index_1)
                                else:
                                    print("ERROR: Invalid Player #")
                    else:
                        print("ERROR: Invalid input")

            if index == 0:
                if not self._ai_only:
                    user_has_priority()
                else:
                    # TODO continue adding AI options in future!
                    # ai is making choice
                    pass
            else:
                if self._debug:
                    user_has_priority()
                else:
                    # ai is making choice
                    pass
        # TODO need to take into account actions taken in between passes!
        # "passed in succession"
        else:
            # MUST RESET PASSES (else we're stuck in infinite loop)
            self._passes.reset()
            turn_actions.start_next_step_or_phase(self, self.step_or_phase)

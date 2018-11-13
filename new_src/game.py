from new_src import passes
from new_src import step_or_phase


class Game:
    def __init__(self):
        self._debug = False
        self._ai_only = False
        self._players = None
        self._battlefield = None
        # XXX Better to cluster functions to a module, then clutter
        # ^ this namespace with functions related ONLY to that object!
        self._passes = passes.Passes()
        # Consider making a general "turn_actions" object or so
        # ^ that stores all sorts of turn info so game can just call:
        # ^ turn_actions.start_next or so.
        self._step_or_phase = step_or_phase.StepOrPhase()
        self._START_METHODS = (_upkeep, _draw, _pre_combat, _begin_combat, _declare_attackers,
                 _declare_blockers, _first_strike_damage, _combat_damage,
                 _end_combat, _post_combat, _end, _cleanup, _untap)

    # utility methods
    def _print_hand_and_decks(self):
        # some objects have __repr__ defined (to simplify printing)
        # XXX Use ID when comparing objects (as you should)
        for i, player in enumerate(self._players):
            print("P" + str(i + 1), "HAND:\n", player.hand,
                  "\nP" + str(i + 1), "DECK:\n", player.deck)

    def _print_hand(index):
        print("P" + str(index + 1), "HAND:\n", self._players[index].hand)

    # methods/classes to use during game
    # XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
    def _active_index(self):
        for i, player in enumerate(self._players):
            if player.is_active():
                return i

    def _active_player(self):
        return self.players[self._active_index()]

    # untap all of active player's permanents
    def _untap_all_of_active(self):
        for card in self._battlefield[self._active_index()]:
            card.untap()

    def _give_player_priority(self, index):
        if self._passes.count() != len(self._players):
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
                        passes.inc()
                        self._give_player_priority((index + 1) % len(self._players))
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
                                if 0 <= index_1 < len(self._players):
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
            self._start_next_step_or_phase(self._step_or_phase.index)

    # methods/classes related to (specifically) turn based actions
    def _start_next_step_or_phase(self, index):
        self._START_METHODS[index]()

    # XXX try to make this share code with untap
    def _first_untap_of_game(self, first_player):
        print("Start of First Untap Step")
        step_or_phase.index = 0
        # ^ XXX evil sets? (along with rest of step_or_phase.index = x)
        # at start, no one is active, so we must directly make 1st player active.
        self._players[first_player].make_active()
        print("Active Player:", self._active_index() + 1)
        print("TBA: Untap all")
        self._untap_all_of_active()
        self._upkeep()

    def _untap(self):
        print("Start of Untap Step")
        step_or_phase.index = 0
        # change active player to the next
        prev_active_index = self._active_index()
        self._active_player().make_inactive()
        self._players[(prev_active_index + 1) % len(self._players)].make_active()
        # XXX calling active_index again is slightly inefficient, but HEY,
        # ^ there might be a corner case we need to cover
        # ALWAYS FAVOR SECURITY/CLARITY OVER EFFICIENCY (to reasonable limits)
        print("Active Player:", self._active_index() + 1)
        # TBA = "Turn-Based Action", SBA = "State-Based Action"
        print("TBA: Untap all")
        self._untap_all_of_active()
        self._upkeep()

    def _upkeep(self):
        print("Start of Upkeep Step")
        step_or_phase.index = 1
        give_player_priority(active_index())

    def _draw(self):
        # TODO must skip if 1st player's 1st draw (if 1v1 or 2-headed giant)
        print("Start of Draw Step")
        step_or_phase.index = 2
        print("TBA: Draw")
        active_player().draw()
        print_hand_and_decks()
        give_player_priority(active_index())

    def _pre_combat(self):
        print("Start of Precombat Main Phase")
        step_or_phase.index = 3
        give_player_priority(active_index())

    def _begin_combat(self):
        print("Start of Beginning of Combat Step")
        step_or_phase.index = 4
        give_player_priority(active_index())

    def _declare_attackers(self):
        print("Start of Declare Attackers Step")
        # TODO need to skip to end if no attackers declared
        step_or_phase.index = 5
        give_player_priority(active_index())

    def _declare_blockers(self):
        print("Start of Declare Blockers Step")
        step_or_phase.index = 6
        give_player_priority(active_index())

    def _first_strike_damage(self):
        print("Start of First Strike Damage Step")
        # TODO need to skip to combat damage if no creatures wih first strike
        # ^ on either side of the field
        step_or_phase.index = 7
        give_player_priority(active_index())

    def _combat_damage(self):
        print("Start of Combat Damage Step")
        step_or_phase.index = 8
        give_player_priority(active_index())

    def _end_combat(self):
        print("Start of End of Combat Step")
        step_or_phase.index = 9
        give_player_priority(active_index())

    def _post_combat(self):
        print("Start of Postcombat Main Phase")
        step_or_phase.index = 10
        print("Step or Phase:", step_or_phase.index)
        give_player_priority(active_index())

    def _end(self):
        print("Start of End Step")
        step_or_phase.index = 11
        give_player_priority(active_index())

    def _cleanup(self):
        print("Start of Cleanup Step")
        step_or_phase.index = 12
        untap()

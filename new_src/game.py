from new_src import passes
from new_src import step_or_phase

class Game:
    def __init__(self):
        self._debug = True
        self._ai_only = False
        # private since we only need each player, NOT players[]
        self._players = []
        self._battlefield = []
        # XXX Better to cluster functions to a module, then clutter
        # ^ this namespace with functions related ONLY to that object!
        self._passes = passes.Passes()
        # Consider making a general "turn_actions" object or so
        # ^ that stores all sorts of turn info so game can just call:
        # ^ turn_actions.start_next or so.
        self._step_or_phase = step_or_phase.StepOrPhase()
        self._START_METHODS = (upkeep, draw, pre_combat, begin_combat, declare_attackers,
                 declare_blockers, first_strike_damage, combat_damage,
                 end_combat, post_combat, end, cleanup, untap)

    def debug(self):
        return self._debug

    def ai_only(self):
        return self._ai_only

    def players(self):
        # return generator over players[]
        return (player for player in self._players)

    def shuffle_all(self):
        for player in self.players():
            player.deck.shuffle()

    def choose_first_player(self, index):
        print("P" + str(index + 1) + ", who goes first?")

        # XXX ALWAYS define funcs locally they'll ONLY be used in that context!
        # ask the user for input
        def user_chooses_first_player():
            # must be an int and refer to an actual player
            while True:
                try:
                    choice = int(input("Player #: ")) - 1
                except ValueError:
                    print("ERROR: Invalid int")
                else:
                    if 0 <= choice < len(self.players()):
                        return choice
                    else:
                        print("ERROR: Invalid Player #")
        if index == 0:
            if not self.ai_only():
                first = user_chooses_first_player()
            else:
                # ai is making choice (by default, chooses itself)
                first = index
        else:
            if self.debug():
                first = user_chooses_first_player()
            else:
                # ai is making choice (by default, chooses itself)
                first = index
        print("P" + str(first + 1), "goes first.")
        return first

    def initial_draw(self):
        for player in self.players():
            for n in range(player.max_hand_size()):
                player.draw()


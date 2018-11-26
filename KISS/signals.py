import random
from KISS import game as game_mod


class Signal:
    NAME = None


# TODO THREAD SAFETY: APPENDING SIGNAL BEFORE OBJECT COMPLETELY SET UP?!
# ^ CALL INIT AFTER FOR FUTURE PROOF. BUT PUT IN NOTES!!!
class ChooseStartingPlayer(Signal):
    NAME = "ChooseStartingPlayer"
#         super().__init__(signals, sgn.ChoosingPlayer(random.randrange(len(game.players))))

    def __init__(self, context, players_len):
        # TODO Make sure in C++ edits after append carry over!
        # ^ I.e., LITERAL object/reference is stored
        self._context = context
        self.index = random.randrange(players_len)

    def use_given_index(self, index):
        # XXX could add player index validation here or so (though not needed)
        self._context(index)


class ChoosePlayer(Signal):
    NAME = "ChoosePlayer"

    def __init__(self, context):
        self._context = context

    def use_given_index(self, index):
        self._context(index)


class InPriority(Signal):
    NAME = "InPriority"

    def __init__(self, game: "game_mod.Game", index):
        self._game = game
        self.index = index

    # TODO NOTE THAT WE *HAVE* TO WRAP THIS WAY TO REFERENCE GAME INSTANCE!
    # ^ Makes our lives easier, anyways. Like a partial/lambda wrapper for funcs!
    # def pass_priority(self, index):
    def pass_priority(self):
        self._game.pass_priority(self.index)

    def play(self, zone, card_index):
        self._game.play(zone, card_index, self.index)

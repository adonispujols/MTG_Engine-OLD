import typing
import random
from new_src import player as player_mod
from new_src import deck
from new_src import card as card_mod
from new_src import hand
from new_src import stack as stack_mod
from new_src import game as game_mod


# XXX Don't forget about Planechase! Super fun!
# XXX NEVER "SAFE" DELETE: It makes you *think* you don't need it, but you might of!
# XXX Assume private fields/methods, then make public if needed by OTHER objects
# ^ "Private" = strictly internal. I.e., NEVER USED outside the class or module/file
# ^ THIS INCLUDES INIT! Outside access means it still isn't *STRICTLY internal*!
# XXX Never use straight getters/setters <- use properties!
# XXX Last design failed because you thought too much about "what" and not "how"
# ^ Don't guess ahead of time what's needed! Find out by trying to do it!
# XXX Keep code compatible code with multiplayer & ai vs ai!
# XXX Always let code fail gracefully on invalid input (if reversible)!
# XXX Stay Pythonic! Throw exceptions on actual errors, rather than check ahead!
# XXX Try generalizing ai behavior to a script or so?
# XXX Maintain a complete, solid CLI to depend on during GUI dev.
# ^ This is ALWAYS our main focus, with ports made to GUI when ready.


# methods/classes for setting up game
# (before going through official "Starting the Game" steps [CR 103])
def init_battlefield(game):
    for player in range(len(game.players)):
        game._battlefield.append([])


# methods for officially "Starting the Game" [CR 103], in corresponding order
def fill_decks(game):
    # fill each deck with 60 cards
    for x in range(60):
        # each card must be a new, separate object,
        # else both decks will refer to same object!
        players[0].deck.add_top(card_mod.Card("one"))
        players[1].deck.add_top(card_mod.Card("two"))


def shuffle_all(game):
    for player in players:
        player.deck.shuffle()


def choose_first_player(game, index):
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
                if 0 <= choice < len(players):
                    return choice
                else:
                    print("ERROR: Invalid Player #")
    if index == 0:
        if not ai_only:
            first = user_chooses_first_player()
        else:
            # ai is making choice (by default, chooses itself)
            first = index
    else:
        if debug:
            first = user_chooses_first_player()
        else:
            # ai is making choice (by default, chooses itself)
            first = index
    print("P" + str(first + 1), "goes first.")
    return first


def initial_draw(game):
    for player in players:
        for n in range(player.max_hand_size()):
            player.draw()


# XXX Constantly peeking into game implies this probably should be done by it

# initializations (for set up)
game = game_mod.Game()
# user controls all players (including AI), if true
game._debug = True
# AI controls all players (including player 1), if true
game._ai_only = False
# cards in battlefield[player_index] pertain to that player
game.battlefield = []
init_battlefield(game)
# player 1, the user by default, has index = 0
# player 2+, the ai by default, has index = nth player - 1
game.players = [player_mod.Player(), player_mod.Player()]
# XXX hard setting attributes is not ideal. ( we'll refactor once done)
game.players[0].deck = deck.Deck()
game.players[0].hand = hand.Hand()
game.players[1].deck = deck.Deck()
game.players[1].hand = hand.Hand()
fill_decks(game)

passes = Passes()
step_or_phase = StepOrPhase()
START_METHODS = (upkeep, draw, pre_combat, begin_combat, declare_attackers,
                 declare_blockers, first_strike_damage, combat_damage,
                 end_combat, post_combat, end, cleanup, untap)

# Starting the game [CR 103]
shuffle_all()
# XXX in a match, loser of last game chooses
# randrange is [start, stop) (exclusive)
first_player = choose_first_player(random.randrange(len(players)))
initial_draw()
# print_hand_and_decks()
first_untap_of_game()

# Playing around with play

# need a stack to check if it's empty
stack = stack_mod.Stack()


# the USER/AI plays cards, NOT the player object!
# ^ It's something the actual player DOES on the CARD
# TODO start with playing a land!
# ^ literally just straight up think about how, you would go about playing a land.
# ^ DO NOT WORRY about efficiency/super abstract design.
# ^ we'll refactor/apply proper OOP principles once we're done!
def play(card: card_mod.Card, is_active, met_land_limit):
    if card.type() == "Land":
        # check if at sorcery speed (priority is implied since play can only be
        # ^ be called if had priority)
        sorcery_speed = stack.is_empty() and is_active
        if sorcery_speed and not met_land_limit:
            # put on battlefield (typically from hand)
            pass
        # PASS THE ZONE! PSSS ZONE ND ID/IDENTIFIER FROM THAT ZONE


# to play a land
# check if card is a land:
# ^ this is a special action that requires:
# - sorcery speed (priority (given), stack is empty, is their turn (is active))
# & - lands played < lands limit
# ^ then, you put it onto battlefield (usually from hand)
# ^ no need for stack resolving or passing priority
# !!!!    regain priorirty afterwards

# 10 MINUTES HARD CODING QUICK COMMENTS LET'S GO!

# you can only do stuff when game explicitly tells you you can****
# you CAN'T affect ai doing stuff. you won't have the option to do ANYTHING!
# XXX need to handle times where you CAN play one of your opponents cards

# import abc
#
#
# class Foo(abc.ABC):
#     def __init__(self, x, y, z):
#         super().__init__()
#
#     @abc.abstractmethod
#     def bar(self, x):
#         print(x, "basic functionality")
#
#
# class Test(Foo):
#     def __init__(self, x, y, z):
#         super().__init__(x, y, z)
#
#     def bar(self):
#         super().bar(45)
#         print("legit")
#
#
# f = Test(5, 5, 5)
# f.bar()

# when ready for tkinter:
# import tkinter as tk
#
# root = tk.Tk()
# root.title("test")
# # lift and topmost = true automatically brings window to top
# # topmost = false so it isn't stuck on top
# root.lift()
# root.attributes('-topmost',True)
# root.after_idle(root.attributes,'-topmost',False)
# root.mainloop()

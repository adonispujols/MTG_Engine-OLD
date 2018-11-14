import random
from new_src import player as player_mod
from new_src import deck
from new_src import card as card_mod
from new_src import hand
from new_src import stack as stack_mod
from new_src import game as game_mod
from new_src import turn_actions
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


# XXX Don't forget about Planechase! Super fun!
# XXX Use "_" for basic loops/not using item (not for i in range(len(iter)))
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
# XXX need to handle times where you CAN play one of your opponents cards


# methods/classes for setting up game
# (before going through official "Starting the Game" steps [CR 103])
# methods for officially "Starting the Game" [CR 103], in corresponding order
def fill_decks(game):
    # fill each deck with 60 cards
    for _ in range(60):
        # each card must be a new, separate object,
        # else both decks will refer to same object!
        game.players[0].deck.add_top(card_mod.Card("one"))
        game.players[1].deck.add_top(card_mod.Card("two"))


def init_battlefield(game):
    for _ in game.players:
        game.battlefield.append([])


def shuffle_all(game):
    for player in game.players:
        player.deck.shuffle()


def choose_first_player(game: game_mod.Game, index):
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
                if 0 <= choice < len(game.players):
                    return choice
                else:
                    print("ERROR: Invalid player #")
    if index == 0:
        if not game.ai_only:
            first = user_chooses_first_player()
        else:
            # ai is making choice (by default, chooses itself)
            first = index
    else:
        if game.debug:
            first = user_chooses_first_player()
        else:
            # ai is making choice (by default, chooses itself)
            first = index
    print("P" + str(first + 1), "goes first.")
    return first


def initial_draw(game):
    for player in game.players:
        for _ in range(player.max_hand_size):
            player.draw()


# XXX Constantly peeking into game in is acceptable in THIS case since we're
# ^ basically making a separate helper script for init/start
# ^ Helps declutter the game namespace

# initializations (for set up)
new_game = game_mod.Game()
# user controls all players (including AI), if true
new_game.debug = True
# AI controls all players (including player 1), if true
new_game.ai_only = False
# player 1, the user by default, has index = 0
# player 2+, the ai by default, has index = nth player - 1
new_game.players = [player_mod.Player(), player_mod.Player()]
# XXX hard setting attributes is not ideal. ( we'll refactor once done)
new_game.players[0].deck = deck.Deck()
new_game.players[0].hand = hand.Hand()
new_game.players[1].deck = deck.Deck()
new_game.players[1].hand = hand.Hand()
fill_decks(new_game)
# cards in battlefield[player_index] pertain to that player
new_game.battlefield = []
init_battlefield(new_game)

# Starting the game [CR 103]
shuffle_all(new_game)
# XXX in a match, loser of last game chooses
# randrange is [start, stop) (exclusive)
first_player = choose_first_player(new_game, random.randrange(len(new_game.players)))
initial_draw(new_game)
turn_actions.first_untap_of_game(new_game, first_player)


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

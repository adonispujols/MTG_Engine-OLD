import random
from new_src import player as player_mod
from new_src import deck
from new_src import card as card_mod
from new_src import hand
from new_src import game as game_mod
from new_src import turn_actions
# XXX Always forward reference types (wrap in string) to avoid import errors!
# ^ STILL NEED TO IMPORT FOR THIS TO WORK <- key misunderstanding


# TODO Comments are reserved for ONLY todos and warnings!

# XXX
# 	CREATE SCRIPT TO QUICKLY TAKE YOU TO A POINT IN GAME!
# AUTOMATE CHANGING PLYER WITHOUT THE OLD HACK OF EDITING/COMMENTING CODE
# (won’t work on large codebases/lots of time + effort on stuff that will
# just be deleted afterwards)#
#   Rollout testing suite confirming (on each run) that everything is
# (and still is) okay!!!!!!!!
# XXX

# XXX Don't forget about Planechase! Super fun!
# XXX Use "_" for basic loops/not using item (not for i in range(len(iter)))
# XXX Avoid unnecessary concatenation. Use ',' not '+ " "' for spaces! (without '')
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

# XXX Constantly peeking into game in init/start script is acceptable since
# ^ it's basically just a helper script to help declutter the game namespace

def init_game():
    new_game = game_mod.Game()
    new_game.debug = True
    new_game.ai_only = False
    new_game.players = [player_mod.Player(), player_mod.Player()]
    # XXX hard setting attributes is not ideal. ( we'll refactor once done)
    new_game.players[0].deck = deck.Deck()
    new_game.players[0].hand = hand.Hand()
    new_game.players[1].deck = deck.Deck()
    new_game.players[1].hand = hand.Hand()
    fill_decks(new_game)
    new_game.battlefield = []
    init_battlefield(new_game)
    start_game(new_game)


def fill_decks(game):
    for i in range(60):
        # XXX each card must be a new, separate object,
        # else both decks will refer to same object!
        game.players[0].deck.push(card_mod.Card("one " + str(i)))
        game.players[1].deck.push(card_mod.Card("two " + str(i)))


def init_battlefield(game):
    for _ in game.players:
        game.battlefield.append([])


def start_game(game):
    shuffle_all(game)
    # XXX in a match, loser of last game chooses
    initial_draw(game)
    turn_actions.first_untap_of_game(game, choose_first_player(game))


def shuffle_all(game):
    for player in game.players:
        player.deck.shuffle()


def initial_draw(game):
    for player in game.players:
        for _ in range(player.max_hand_size):
            player.draw()


def choose_first_player(game: game_mod.Game):
    index = random.randrange(len(game.players))
    print("P" + str(index + 1) + ", who goes first?")

    # XXX ALWAYS define funcs locally they'll ONLY be used in that context!
    def user_chooses_first_player():
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
        if game.ai_only:
            first = index
        else:
            first = user_chooses_first_player()
    else:
        if game.debug:
            first = user_chooses_first_player()
        else:
            first = index
    print("P" + str(first + 1), "goes first.")
    return first


init_game()

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

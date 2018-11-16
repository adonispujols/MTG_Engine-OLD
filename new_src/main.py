import random
from new_src import player as player_mod
from new_src import deck
from new_src import card as card_mod
from new_src import hand
from new_src import game as game_mod
from new_src import turn_actions


def init_game(game):
    game.debug = True
    game.ai_only = False
    game.players = [player_mod.Player(), player_mod.Player()]
    # XXX avoid hard setting attributes?
    game.players[0].deck = deck.Deck()
    game.players[0].hand = hand.Hand()
    game.players[1].deck = deck.Deck()
    game.players[1].hand = hand.Hand()
    fill_decks(game)
    game.battlefield = []
    init_battlefield(game)


def fill_decks(game):
    for i in range(10):
        # XXX each should be it's own new object
        game.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
        game.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
    for i in range(10):
        game.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
        game.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))


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


def choose_first_player(game: "game_mod.Game"):
    index = random.randrange(len(game.players))
    print("P" + str(index + 1) + ", who goes first?")

    def user_chooses_first_player():
        while True:
            try:
                choice = int(input("Player #: "))
            except ValueError:
                print("ERROR: Invalid int")
            else:
                choice -= 1
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


new_game = game_mod.Game()
init_game(new_game)
# have your code like this, where init game doesn't stick around forever)
start_game(new_game)

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

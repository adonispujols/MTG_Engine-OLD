from new_src import player
from new_src import deck
from new_src import card
from new_src import hand
import random


# XXX hard setting attributes is not ideal.
# ^ once finished, we'll turn what should be params into params, and what
# ^ should be wrapped in "add" methods, be wrapped
# ^ OR create the object in self.foo, if needed

# we need two players (player "1" is user, player "2" is ai (typically))
player_1 = player.Player()
player_2 = player.Player()

# these players are supposed to have decks
deck_1 = deck.Deck()
deck_2 = deck.Deck()

# lets give it to them
player_1.deck = deck_1
player_2.deck = deck_2

# these decks typically have 60 cards
# we'll just fill them with thuds
for x in range(60):
    # need to make two separate, lest both decks will refer to same object!
    test_card1 = card.Card()
    test_card2 = card.Card()
    # decks need to store cards in an array
    # prob good to define how we add to this array
    player_1.deck.add_top(test_card1)
    player_2.deck.add_top(test_card2)

# decks are supposed to be shuffled
player_1.deck.shuffle()
player_2.deck.shuffle()

# randomly decide who chooses to first
# XXX ^ in a match, loser of last game chooses
# randrange is [start, stop) (exclusive)
player_to_choose = random.randrange(2)

# need to give that player a choice, now, no?
# !!! hold on, who gets to choose? <- only give option to player choosing.
# ^ if user (player_1), ask for input. If ai (player_2) print info, put
# ^ have it automatically choose (no chance for input) UNLESS debug is on
# ^ Otherwise, ask for input as if you /were/ player 2
# ^ same argument if player_1 is ALSO set to ai <- save for later
# XXX don't even think about multiplayer. just focus on one v one
# ^ we can expand later!
debug = True
first_player = 0

print("Player", player_to_choose + 1, ", who goes first?")
if player_to_choose == 0:
    # ask player_1, or user, for input
    choice = input("Player Int: ")
    first_player = int(choice)
elif debug:
    # user controls ai, ask for input like above
    choice = input("Player Int: ")
    first_player = int(choice)
else:
    # ai is making choice (by default, chooses itself)
    first_player = 2
print("Player", first_player, "goes first.")

# we'll continue adding AI options for future!

# players start at 20 life
# * set that as default for players

# each player draws equal to starting hand size (default 7)
# * set default hand size at 7 for players
# so, each player have a hand to "draw" to:
hand_1 = hand.Hand()
hand_2 = hand.Hand()
# XXX ^ could just put constructed object directly in to hand (no alias)

# let's give it to them
player_1.hand = hand_1
player_2.hand = hand_2




# you can only do stuff when game explicitly tells you you can****
# you CAN'T affect ai doing stuff. you won't have the option to do ANYTHING!
# we keep track of player choosing (what to do)
# based on this, we give the option to play stuff relevant to that player!
# XXX ^ need to handle times where you CAN play one of your opponents cards
# XXX ^ how about playing from a different zone???

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

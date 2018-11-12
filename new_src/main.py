import typing
from new_src import player as player_mod
from new_src import deck
from new_src import card as card_mod
from new_src import hand
import random


# XXX hard setting attributes is not ideal.
# ^ once finished, we'll turn what should be params into params, and what
# ^ should be wrapped in "add" methods, be wrapped
# ^ OR create the object in self.foo, if needed

# we need two players (player "1" is user, player "2" is ai (typically))
# BUT in code they are referred to by player_index, or nth player - 1
player_1 = player_mod.Player()
player_2 = player_mod.Player()

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
    test_card1 = card_mod.Card("one")
    test_card2 = card_mod.Card("two")
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


def player_choose_first(player_index):
    first = 0
    print("P" + str(player_index + 1), ", who goes first?")
    if player_index == 0:
        # ask player_1, or user, for input
        choice = input("Player Int: ")
        first = int(choice) - 1
    elif debug:
        # user controls ai, ask for input like above
        choice = input("Player Int: ")
        first = int(choice) - 1
    else:
        # ai is making choice (by default, chooses itself)
        # TODO remember to update code for multiplayer!:
        first = 1
    print("P" + str(first + 1), "goes first.")
    return first


first_player = player_choose_first(player_to_choose)

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

# need to be able to draw. players "Draw" cards
# ^ defined this for player
for n in range(player_1.maximum_hand_size):
    player_1.draw()
for n in range(player_2.maximum_hand_size):
    player_2.draw()

# very useful to give these objects a to string (repr) for time + safety
# ^ XXX Use ID when comparing objects, we'll be replacing repr, now
print("P1 HAND:\n", player_1.hand, "\nP1 DECK:\n", player_1.deck)
print("P2: HAND:\n", player_2.hand, "\nP2 DECK:\n", player_2.deck)


# we need to set up a structure for our various steps and phases
# let's go through steps one by one:
# start of game, go to untap step
# untap all of "active player's" permanents
# ^ so we need: concept of active player, and "permanents"
# ^ also need: public zone battlefield for "permanents", distinguishing between
# ^ what card belongs to whom (just owner for now, no need for controller)
# ^ being "active" is a property of a player

# having players in array makes assigning who's who without many ifs
players = [player_1, player_2]

# set 1st player to active player
players[first_player].make_active()

# first, make battlefield to hold the permanents to untap
# ^ all cards in battlefield[player_index] pertain to that player
battlefield: typing.List[typing.List[card_mod.Card]] = []
# XXX need to warp in fuction, lest our player var sticks around


def create_battlefield():
    for player in range(len(players)):
        battlefield.append([])


create_battlefield()


# XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
# def active_player():
#     for player in players:
#         if player.is_active():
#             return player

# XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
def active_index():
    for i, player in enumerate(players):
        if player.is_active():
            return i


# untap all of active player's permanents
def untap_all_of_active():
    for card in battlefield[active_index()]:
        card.untap()


untap_all_of_active()

# then we move on to upkeep
# active player receives "priority" <- what's that?
# for now, it's the game giving you the right to "pass priority"


# TODO need to take into account actions taken in between passes!
# XXX hacky solution, of course, but better than globals!
# Again, the 50% > 99%, cause the 50% actually exists!
class Passes:
    def __init__(self):
        self.passes = 0

    def inc(self):
        self.passes += 1

    def count(self):
        return self.passes


passes = Passes()

def give_player_priority(player_index):
    if passes.count() != len(players):
        if player_index == 0:
            # ask player_1, or user, for input
            choice = input("P1, Press enter to pass")
            # if just pressed enter (entered no input)
            if not choice:
                passes.inc()
                give_player_priority(player_index + 1)
        elif debug:
            # ask user controlling ai for input (same as above)
            choice = input("P" + str(player_index + 1) + " Press enter to pass")
            if not choice:
                passes.inc()
                give_player_priority((player_index + 1) % len(players))
    # "passed in succession" <- with no care about actions
    else:
        start_next_step_or_phase(step_or_phase)


# since we are in untap at this point, our step/phase is 0
step_or_phase = 0

# give active player priority
give_player_priority(active_index())


def start_next_step_or_phase(step_or_phase, game):


def start_next_step_or_phase(self, index):
    # don't want lots of ifs, so let's have a dictionary and methods
    START_METHODS[step_or_phase]()

# def special_untap(game: game_mod.Game, first_player: player_mod.Player):
#     game.step_or_phase = 0
#     # XXX ^ evil set? (along with rest of step_or_phase = x)
#     # at start, no one is active, so we must directly make first player active.
#     first_player.make_active()
#     game.untap_all_of_player(first_player.index())
#     upkeep(game)


def untap(game: game_mod.Game):
    game.step_or_phase = 0
    game.change_active_player_to_next()
    game.untap_all_of_player(game.active_player().index())
    upkeep(game)


def upkeep(game):
    game.step_or_phase = 1
    game.active_player().gain_priority()


def draw(game: game_mod.Game):
    game.step_or_phase = 2
    game.active_player().draw(1)
    game.active_player().gain_priority()


def pre_combat(game):
    game.step_or_phase = 3
    game.active_player().gain_priority()


def begin_combat(game):
    game.step_or_phase = 4
    game.active_player().gain_priority()


def declare_attackers(game):
    game.step_or_phase = 5
    game.active_player().gain_priority()


def declare_blockers(game):
    game.step_or_phase = 6
    game.active_player().gain_priority()


def first_strike_damage(game):
    game.step_or_phase = 7
    game.active_player().gain_priority()


def combat_damage(game):
    game.step_or_phase = 8
    game.active_player().gain_priority()


def end_combat(game):
    game.step_or_phase = 9
    game.active_player().gain_priority()


def post_combat(game):
    game.step_or_phase = 10
    game.active_player().gain_priority()


def end(game):
    game.step_or_phase = 11
    game.active_player().gain_priority()


def cleanup(game):
    game.step_or_phase = 12
    untap(game)




START_METHODS = (upkeep, draw, pre_combat, begin_combat, declare_attackers,
                 declare_blockers, first_strike_damage, combat_damage,
                 end_combat, post_combat, end, cleanup, untap)


# after succesive passing of priority, we ought to move to next step or phase
# ^ time to wrap in method for easy calling from there
# ^ need to keep track of it now, it seems


# TEST: 10 MINUTES HARD CODING QUICK COMMENTS LET'S GO!

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

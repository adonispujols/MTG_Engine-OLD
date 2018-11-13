import typing
import random
from new_src import player as player_mod
from new_src import deck
from new_src import card as card_mod
from new_src import hand
from new_src import stack as stack_mod


# TODO Last design failed because you thought too much about "what" and not "how"
# ^ Don't guess ahead of time what's needed! Find out by trying to do it!
# TODO keep code compatible code with multiplayer & ai vs ai!
# TODO Always let code fail gracefully on invalid input (if reversible)!
# TODO Stay Pythonic! Throw exceptions on actual errors, rather than check ahead!
# XXX Try generalizing ai behavior to a script or so?
# XXX Maintain a complete, solid CLI to depend on during GUI dev.
# ^ This is ALWAYS our main focus, with ports made to GUI when ready.


# methods/classes for setting up game
# (before going through official "Starting the Game" steps [CR 103])
def init_battlefield():
    for player in range(len(players)):
        battlefield.append([])


class StepOrPhase:
    # again, awkward creation of object
    # XXX seems like we need to collect these into a "game" object or so
    # ^ XXX HOWEVER, don't assume game should inherit the other methods!!
    def __init__(self):
        # So far this is hard set, can it be better?
        self.index = 0

    def get_index(self):
        return self.index


# utility methods
def print_hand_and_decks():
    # some objects have __repr__ defined (to simplify printing)
    # XXX Use ID when comparing objects (as you should)
    for i, player in enumerate(players):
        print("P" + str(i + 1), "HAND:\n", player.hand,
              "\nP" + str(i + 1), "DECK:\n", player.deck)


def print_hand(index):
    # XXX Python recommends EAFP (Easier to ask for forgiveness than permission)
    # ^ As opposed to LBYL (Look before you leap)
    # Thus, use exceptions to handle (actual) errors, instead of checking ahead.
    try:
        hand_str = players[index].hand
    except IndexError:
        print("ERROR: Invalid Player #")
    else:
        print("P" + str(index + 1), "HAND:\n", hand_str)


# methods for officially "Starting the Game" [CR 103], in corresponding order
def fill_decks():
    # fill each deck with 60 cards
    for x in range(60):
        # each card must be a new, separate object,
        # else both decks will refer to same object!
        players[0].deck.add_top(card_mod.Card("one"))
        players[1].deck.add_top(card_mod.Card("two"))


def shuffle_all():
    for player in players:
        player.deck.shuffle()


def choose_first_player(index):
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
                if 0 <= choice <= len(players) - 1:
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


def initial_draw():
    for player in players:
        for n in range(player.get_max_hand_size()):
            player.draw()


# methods/classes to use during game
# XXX could definitely optimize this AND SIMILAR (however, clarity is key atm)
def active_index():
    for i, player in enumerate(players):
        if player.is_active():
            return i


def active_player():
    return players[active_index()]


# untap all of active player's permanents
def untap_all_of_active():
    for card in battlefield[active_index()]:
        card.untap()


def give_player_priority(index):
    if passes.count() != len(players):
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
                    give_player_priority((index + 1) % len(players))
                    break
                # list of options available (debugging or not)
                # TODO implement user-limited commands (no debug)
                # ^ normally, user's knowledge of game is limited
                # ^ he can't just randomly search through hands, decks, etc
                # ^ EX: hand-self prints own hand of player
                # TODO play(card)
                elif choice[0] == "TODO":
                    pass
                elif debug:
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
                            print_hand(index_1)
                else:
                    print("ERROR: Invalid input")
        if index == 0:
            if not ai_only:
                user_has_priority()
            else:
                # TODO continue adding AI options in future!
                # ai is making choice
                pass
        else:
            if debug:
                user_has_priority()
            else:
                # ai is making choice
                pass
    # TODO need to take into account actions taken in between passes!
    # "passed in succession"
    else:
        # MUST RESET PASSES (else we're stuck in infinite loop)
        passes.reset()
        start_next_step_or_phase(step_or_phase.index)


class Passes:
    # XXX hacky solution, of course, but better than globals!
    # Again, the 50% > 99%, cause the 50% actually exists!
    def __init__(self):
        self.passes = 0

    def inc(self):
        self.passes += 1

    def reset(self):
        self.passes = 0

    def count(self):
        return self.passes


# methods/classes related to (specifically) turn based actions
def start_next_step_or_phase(index):
    START_METHODS[index]()


# XXX try to make this share code with untap
def first_untap_of_game():
    print("Start of First Untap Step")
    step_or_phase.index = 0
    # ^ XXX evil sets? (along with rest of step_or_phase.index = x)
    # at start, no one is active, so we must directly make 1st player active.
    players[first_player].make_active()
    print("Active Player:", active_index() + 1)
    print("TBA: Untap all")
    untap_all_of_active()
    upkeep()


def untap():
    print("Start of Untap Step")
    step_or_phase.index = 0
    # change active player to the next
    prev_active_index = active_index()
    active_player().make_inactive()
    players[(prev_active_index + 1) % len(players)].make_active()
    # XXX calling active_index again is slightly inefficient, but HEY,
    # ^ there might be a corner case we need to cover
    # ALWAYS FAVOR SECURITY/CLARITY OVER EFFICIENCY (to reasonable limits)
    print("Active Player:", active_index() + 1)
    # TBA = "Turn-Based Action", SBA = "State-Based Action"
    print("TBA: Untap all")
    untap_all_of_active()
    upkeep()


def upkeep():
    print("Start of Upkeep Step")
    step_or_phase.index = 1
    give_player_priority(active_index())


def draw():
    # TODO must skip if 1st player's 1st draw (if 1v1 or 2-headed giant)
    print("Start of Draw Step")
    step_or_phase.index = 2
    print("TBA: Draw")
    active_player().draw()
    print_hand_and_decks()
    give_player_priority(active_index())


def pre_combat():
    print("Start of Precombat Main Phase")
    step_or_phase.index = 3
    give_player_priority(active_index())


def begin_combat():
    print("Start of Beginning of Combat Step")
    step_or_phase.index = 4
    give_player_priority(active_index())


def declare_attackers():
    print("Start of Declare Attackers Step")
    # TODO need to skip to end if no attackers declared
    step_or_phase.index = 5
    give_player_priority(active_index())


def declare_blockers():
    print("Start of Declare Blockers Step")
    step_or_phase.index = 6
    give_player_priority(active_index())


def first_strike_damage():
    print("Start of First Strike Damage Step")
    # TODO need to skip to combat damage if no creatures wih first strike
    # ^ on either side of the field
    step_or_phase.index = 7
    give_player_priority(active_index())


def combat_damage():
    print("Start of Combat Damage Step")
    step_or_phase.index = 8
    give_player_priority(active_index())


def end_combat():
    print("Start of End of Combat Step")
    step_or_phase.index = 9
    give_player_priority(active_index())


def post_combat():
    print("Start of Postcombat Main Phase")
    step_or_phase.index = 10
    print("Step or Phase:", step_or_phase.index)
    give_player_priority(active_index())


def end():
    print("Start of End Step")
    step_or_phase.index = 11
    give_player_priority(active_index())


def cleanup():
    print("Start of Cleanup Step")
    step_or_phase.index = 12
    untap()


# initializations (for set up)
# user controls all players (including AI), if true
debug = False
# AI controls all players (including player 1), if true
ai_only = False
# player 1, the user by default, has index = 0
# player 2+, the ai by default, has index = nth player - 1
players = [player_mod.Player(), player_mod.Player()]
# XXX hard setting attributes is not ideal. ( we'll refractor once done)
players[0].deck = deck.Deck()
players[0].hand = hand.Hand()
players[1].deck = deck.Deck()
players[1].hand = hand.Hand()
fill_decks()
# cards in battlefield[player_index] pertain to that player
battlefield: typing.List[typing.List[card_mod.Card]] = []
init_battlefield()
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
# ^ we'll refractor/apply proper OOP principles once we're done!
def play(card: card_mod.Card, is_active, met_land_limit):
    if card.type() == "Land":
        # check if at sorcery speed (priority is implied since play can only be
        # ^ be called if had priority)
        sorcery_speed = stack.is_empty() and is_active
        if sorcery_speed and not met_land_limit:
            # put on battlefield (typically from hand)
            pass
        # PASS THE ZONE!


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

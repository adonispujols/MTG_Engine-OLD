# import collections
#
# # dummy for type checking
# class Signal:
#     NAME = None
#
#
# class ChooseStartingPlayer(Signal):
#     NAME = "ChooseStartingPlayer"
#
#     def __init__(self, index):
#         self.index = index
#
# d = collections.deque()
# d.append(ChooseStartingPlayer(2))
# d.append(1)
# d.append(2)
# d.append(3)
# d.append(4)
# new_signal = d.popleft()
# print(type(new_signal))
#
#
# def choose_start(signal: ChooseStartingPlayer):
#     print(signal.index)
#
#
# def process_signal(signal: Signal):
#     dct[signal.NAME](signal)
#
#
# dct = {ChooseStartingPlayer.NAME: choose_start}
#
# process_signal(new_signal)

# # import threading
# # import time
#
# # event = threading.Event()
# # lock = threading.Lock()
# #
# # def test():
# #     print("event called, waiting")
# #     event.wait()
# #     print("got event, clear flag")
# #     event.clear()
# #     # releasing lock here still doesn't help
# #     # possible that set is called in between
# #     # lock release and wait!
# #     print("waiting again after clear")
# #     event.wait()
# #     print("done")
# #     # print("doing stuff")
# #     # time.sleep(2)
# #     # print("done")
# #
# #
# # thread_1 = threading.Thread(target=test)
# # print("starting thread")
# # thread_1.start()
# # print("unlocking")
# # # doing stuff there
# # lock.acquire()
# # event.set()
# # # don't call next until test has told us it's ready
# # # if lock is held (still need to finish processing from before),
# # # ^ THEN go ahead and set (and break us out of block!)
# # lock.acquire()
# # event.set()
#
#
# # METHOD USING SEPARATE STATE
# # class ChooseNext:
# #     def __init__(self, game: "Game"):
# #         self.game = game
# #
# #     # all classes have same input handler
# #     def on_set_up(self):
# #         self.game.current_input_handler = self
# #         self.set_up()
# #
# #     def set_up(self):
# #         # tell gui player with random index needs to choose
# #         pass
# #
# #     # process what was given by gui
# #     def process(self, input_):
# #         self.game.start_game_part_2(input_)
# #         # continue with starting game
# #         # makes more sense to <- not case with in priority
# #         # yes. keep this as small as possible.
# #         # keep the states simple
# #
# #
# # class Game:
# #     current_input_handler: ChooseNext
# #
# #     def __init__(self):
# #         # current state/thing to call
# #         self.current_input_handler = None
# #
# #     # gui calls on_event
# #     def on_input(self, input_):
# #         self.current_input_handler.process(input_)
# #
# #     def start_game(self):
# #         # blah blah
# #         # need to choose next player
# #         ChooseNext(self).on_set_up()
# #         # stuff to do after depending on previous
# #         # CAN NEVER DO STUFF UNTIL THAT FINISHES!
# #         # We're relying on input before moving on.
# #
# #     def start_game_part_2(self, player_chosen):
# #         # shuffle decks (or whatever needs to happen) THEN
# #         # call first untap with player_chosen
# #         pass
# #
# #
# # new_game = Game()
# # # TODO get it working like this, THEN we'll try the locks/waiting version!
# # new_game.start_game()
# # new_game.on_input(2)
# #
# # METHOD USING LOCK
# # ^ Much clearer that we're waiting for input
#
# # import threading
# # # import time
# # threading.C
# #
# # def on_input(input_):
#     # only interface game has
#     # we can set "input" property to whatever
#     # OR have it rely on OUR input
#     # then continue processing on our set alive part
#     # can we pass that as an argument?
#     # we could make a queue if wanted to, but that's over kill
#     # we pass input to object, since we'll be calling game.input anyways!
#     # ^- its something the OBJECT deals with!
#     # but can we do it on call?
#     # easier to do on constructor. but we should have locked stuff up...
#     # we call lock up here?
#     # call and
#     pass
#
#
# def start_game():
#     # blah blah
#     # block until input for next player:
#     starting_player = choose_next()
#     # do stuff with index (but after shuffling or so)
#
#
# def choose_next():
#     # block until received input
#     return 0
#
#
# # event = threading.Event()
# # lock = threading.Lock()
# #
# # def test():
# #     print("event called, waiting")
# #     event.wait()
# #     print("got event, clear flag")
# #     event.clear()
# #     # releasing lock here still doesn't help
# #     # possible that set is called in between
# #     # lock release and wait!
# #     print("waiting again after clear")
# #     event.wait()
# #     print("done")
# #     # print("doing stuff")
# #     # time.sleep(2)
# #     # print("done")
# #
# #
# # thread_1 = threading.Thread(target=test)
# # print("starting thread")
# # thread_1.start()
# # print("unlocking")
# # # doing stuff there
# # lock.acquire()
# # event.set()
# # # don't call next until test has told us it's ready
# # # if lock is held (still need to finish processing from before),
# # # ^ THEN go ahead and set (and break us out of block!)
# # lock.acquire()
# # event.set()


# METHOD USING SEPARATE STATE
# class ChooseNext:
#     def __init__(self, game: "Game"):
#         self.game = game
#
#     def on_set_up(self):
#         self.game.current_input_handler = self
#         self.set_up()
#
#     def set_up(self):
#         # tell gui player with random index needs to choose
#         pass
#
#     def process(self, input_):
#         self.game.start_game_part_2(input_)
#         # continue with starting game
#
#
# class Game:
#     current_input_handler: ChooseNext
#
#     def __init__(self):
#         self.current_input_handler = None
#
#     def on_input(self, input_):
#         self.current_input_handler.process(input_)
#
#     def start_game(self):
#         # blah blah
#         ChooseNext(self).on_set_up()
#
#     def start_game_part_2(self, player_chosen):
#         # continue with info
#         pass
#
#
# new_game = Game()
# # TODO get it working like this, THEN we'll try the locks/waiting version!
# new_game.start_game()
# new_game.on_input(2)

# TODO THIS WORKS
# new version using while true loop/just getting rid of dead calls
# ^ using threads and loops
# import threading
# import collections
# import time
#
# # lock = threading.Lock()
# event = threading.Event()
#
#
# # the WHOLE game needs to block!
# # ^ either warp in function OR subclass threading
# # we'll keep it simple for now
# class Game:
#     def __init__(self):
#         self.input_ = None
#
#     def un_block(self, given_input_):
#         print("setting input")
#         self.input_ = given_input_
#         print("unblocking")
#         event.set()
#
#     def start_game(self):
#             # blah blah
#             starting_player = self.choose_next()
#             # use input
#             print("starting player: ", starting_player)
#
#     # TODO make general input blocking object
#     # ^ it just takes a signal to tell gui
#     # ^ rest is automated
#     def choose_next(self):
#         # simulate long process before true block
#         time.sleep(3)
#         signals.append("<Simulating signal>")
#         # block input
#         event.wait()
#         return self.input_
#
# def run_game():
#     game.start_game()
#
#
# signals = collections.deque()
# game = Game()
# thread = threading.Thread(target=run_game)
# thread.start()
#
# # simulating gui
# while True:
#     # if there is a signal
#     if signals:
#         # signal handling will be more advanced
#         print(signals.popleft())
#         input_ = input("<Dialog that corresponds to signal>: ")
#         game.un_block(input_)
#         break

# That's fine. how to stop recursive calls?
# one approach
# import functools as ft
#
#
# def foo1(arg, arg2=None):
#     print("foo1:", arg, arg2)
#     return ft.partial(foo2, "arg 1", arg2="arg 2")
#
#
# def foo2(arg, arg2=None):
#     print("foo2:", arg, arg2)
#     return ft.partial(foo3, "arg 1", arg2="arg 2")
#
#
# def foo3(arg, arg2=None):
#     print("foo3:", arg, arg2)
#     return ft.partial(foo1, "arg 1", arg2="arg 2")
#
#
# current_func = foo1("arg 1", "arg 2")
# while True:
#     # do next, then set up next (almost like current_func ++)
#     current_func = current_func()

# now put it all together

# threading with dead frame optimization

# import threading
# import collections
# import functools as ft
#
#
# class Game:
#     def __init__(self):
#         self.input_ = None
#
#     def internal_loop(self):
#         current_func = self.start_game()
#         while True:
#             current_func = current_func()
#
#     def un_block(self, given_input_):
#         self.input_ = given_input_
#         event.set()
#
#     def start_game(self):
#             # blah blah
#             # noinspection PyUnusedLocal
#             starting_player = self.choose_next()
#             # more start game stuff
#             return ft.partial(self.first_untap)
#
#     def choose_next(self):
#         signals.append("<Simulating signal>")
#         event.wait()
#         return self.input_
#
#     def first_untap(self):
#         return ft.partial(self.upkeep)
#
#     def upkeep(self):
#         return ft.partial(self.in_priority)
#
#     def in_priority(self):
#         return ft.partial(self.pass_priority)
#
#     def pass_priority(self):
#         return ft.partial(self.give_priority)
#
#     def give_priority(self):
#         return ft.partial(self.in_priority)
#
#
# def run_game():
#     game.internal_loop()
#
#
# event = threading.Event()
# signals = collections.deque()
# game = Game()
# thread = threading.Thread(target=run_game)
# thread.start()
#
# while True:
#     if signals:
#         print(signals.popleft())
#         input_ = input("<Dialog that corresponds to signal>: ")
#         game.un_block(input_)
#         break

# version using func to process + optional context (func to call next)
# TODO THIS VERSION DOES NOT EXPLICITLY CONTROL CALL FRAMES!
# ^ MAKE SURE NOOOO FUNCTION IS RECURSIVELY CALLED BEFORE STATE REACHED!
# MORE ISSUES WITH MAKING SURE THING STAYS A CERTAIN TYPE

import abc


class State(abc.ABC):
    @abc.abstractmethod
    def process(self, event):
        pass


class ChoosePlayer(State):
    def __init__(self, context):
        # send signal to gui
        self.context = context

    def process(self, event):
        self.context(event)


class InPriority(State):
    def __init__(self, game_):
        # send signal to gui
        self.game = game_

    def process(self, event):
        self.game.pass_priority()


class Game:
    state: State

    def __init__(self):
        self.state = None

    def on_input(self, input_):
        self.state.process(input_)

    def start_game(self):
        # blah blah
        self.state = ChoosePlayer(self.start_game_part_2)

    # noinspection PyUnusedLocal
    def start_game_part_2(self, player_chosen):
        # more start game stuff
        self.first_untap()

    def first_untap(self):
        self.upkeep()

    def upkeep(self):
        self.give_priority()

    def give_priority(self):
        self.state = InPriority(self)

    def pass_priority(self):
        self.give_priority()


# TODO REDUCE DEAD FRAMES!!!!
# ^ make quote that when we optimize we'll deal with it
# For now make important TODO for making sure no infinite recursion
# ^ like what happened originally
# ^ ensure same function is NEVER recursivly called
# ^ some languages have tail call optimization, so we don't haVe to worry
# ^- (unless making cross compiler compatible)
# TODO note some lang have tail call opt (know how to tap into) and no worry (if set up right)
# ^ IF OPTIMIZATION FLAGS ARE ON FOR COMPILING!
# ^ WHICH MEANS WE CANT DO IF WANTING TO MAKE CROSS PLATFORM
# ^ BIG OOF TO MENTION!
# TODO note we should make sure if ANY function where to be called again before previous finishes
# we should have that be a state (or put in a queue or soemthing) and processed immediately
# ^ transient.
#  most likely you won't have to.
# queue?
# TODO make note about simplicity and/or performance boost from recreating objects during run
# ^ could create function like choose_player, taking needed params for object
# ^ we'll haave code for that in two different places AND requiring any update on object
# ^ to reflect chnge in wrapper
# TODO could reqquire locks on input (only accept when game allows)
# ^ ultimately up to gui to understand we only accet ONE input call per EACH signal!
# ^ but good side goal
# TODO put init on differnet prt of code?
# TODO natural/more intuitive way of forcing subclasses to have X?
# TODO how to force subclasses to init n object (signal?)
# TODO use keyword args for many params?
# TODO better description of constants SPECIFICALLY for each instance (not shared throughout)
# ^ https://stackoverflow.com/questions/1527395/constant-instance-variables
# ^ These guys suggest forcibly using property to avoid set
# ^ Well, if they should never logically be changed, then we should never logically change them
# TODO IMPORTANT MEMO: MAKE IT RECURRING:
# TODO:MEMO, TO MAKE SURE GIVEN PARAM IS EITHER X TYPE OR INITIALIZED:
# ^ THEN JUST MAKE A TYPE ANNOTATION! Pycharm will warn you if passing the wrong type/class object
# ^ instead of an actual instance object! YES, IT DOES KNOW THE DIFFERENCE!
# TODO Do we really need "" for mods around ALL type annotations? Just non-lib/package ones?
# TODO do we really need to pass game, or can we pass exactly what they need to work?
# ^ consider choose player, we should just get len of players, no?
# TODO if subclasses require a common param, or common object containing that param:
# ^ consider super class automate/force usage of it (though this gives objcets more info than
# ^ they may need
# TODO ^ OR ATLEAST FIND A WAY TO SHARE SAME REFERENCE AMONG THEM, IF NEEDED
# TODO first untap and untap sharing code. any clean way to merge them?
# TODO clean way to merge code of each step? Seems very repetitive...
# ^ could we use constants to just auto set a bit?
# TODO make sure ANY needed params/stuff tht happens to be given/done before/after call
# ARE ALL identified in code somehow! Only leave to documenttion (either formally or in head)
# ^ if you can't force it otherwise! (without going to any messy/extreme lengths, like name mangling)
# TODO Just use class names for signal names?
# ^ Keeping them the same let's us ensure X signal corresponds to X state
# TODO Should p w/ priority index just be stored in game vs passed around everywhere?
game = Game()
game.start_game()
game.on_input("test")
game.on_input("test 2")


class F:
    def __init__(self):
        self.name: str = "sd"


f = F()
f.name = 3
print(type(f.name))

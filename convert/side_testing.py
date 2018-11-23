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

import threading
import collections
import functools as ft


class Game:
    def __init__(self):
        self.input_ = None

    def internal_loop(self):
        current_func = self.start_game()
        while True:
            current_func = current_func()

    def un_block(self, given_input_):
        self.input_ = given_input_
        event.set()

    def start_game(self):
            # blah blah
            starting_player = self.choose_next()
            # more start game stuff
            return ft.partial(self.first_untap)

    def choose_next(self):
        signals.append("<Simulating signal>")
        event.wait()
        return self.input_

    def first_untap(self):
        return ft.partial(self.upkeep)

    def upkeep(self):
        return ft.partial(self.in_priority)

    def in_priority(self):
        return ft.partial(self.pass_priority)

    def pass_priority(self):
        return ft.partial(self.give_priority)

    def give_priority(self):
        return ft.partial(self.in_priority)


def run_game():
    game.internal_loop()


event = threading.Event()
signals = collections.deque()
game = Game()
thread = threading.Thread(target=run_game)
thread.start()

while True:
    if signals:
        print(signals.popleft())
        input_ = input("<Dialog that corresponds to signal>: ")
        game.un_block(input_)
        break

# version using func to process + optional context (func to call next)


class Game:
    def start_game(self):
        # blah blah
        # get starting player input
        # more start game stuff
        pass

    def choose_next(self):
        pass

    def first_untap(self):
        pass

    def upkeep(self):
        pass

    def in_priority(self):
        pass

    def pass_priority(self):
        pass

    def give_priority(self):
        pass

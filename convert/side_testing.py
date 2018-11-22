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

import threading
# import time

# event = threading.Event()
# lock = threading.Lock()
#
# def test():
#     print("event called, waiting")
#     event.wait()
#     print("got event, clear flag")
#     event.clear()
#     # releasing lock here still doesn't help
#     # possible that set is called in between
#     # lock release and wait!
#     print("waiting again after clear")
#     event.wait()
#     print("done")
#     # print("doing stuff")
#     # time.sleep(2)
#     # print("done")
#
#
# thread_1 = threading.Thread(target=test)
# print("starting thread")
# thread_1.start()
# print("unlocking")
# # doing stuff there
# lock.acquire()
# event.set()
# # don't call next until test has told us it's ready
# # if lock is held (still need to finish processing from before),
# # ^ THEN go ahead and set (and break us out of block!)
# lock.acquire()
# event.set()

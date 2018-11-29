import collections
from KISS import game as game_mod
from KISS import signals as signal_mod
from KISS import signal_handler as signal_handler_mod
# REMOVE pympler


def debug_info():
    print("SIGNAL: {}\nSTEP/PHASE: {}\nP0 HAND:\n{}\nP0 FIELD:\n{}\nP1 HAND:\n{}\nP1 FIELD:\n{}".format(
        dequeued_signal.NAME, game.step_or_phase.name, game.players[0].hand, game.battlefield[0],
        game.players[1].hand, game.battlefield[1]))


def choose_starting_player(signal: "signal_mod.ChooseStartingPlayer"):
    input_ = input("P" + str(signal.index) + ", Choose the starting player: ")
    signal.use_given_index(int(input_))


def in_priority(signal: "signal_mod.InPriority"):
    index = signal.index
    # split into: <action> <param1> <param2> ... etc (if requried)
    input_ = input("P" + str(index) + " has priority: ").split()
    if not input_:
        signal.pass_priority()
    # <action> <zone> <index_in_zone>
    elif input_[0] == "play":
        if input_[1] == "hand":
            signal.play(game.players[index].hand, int(input_[2]) - 1)


if __name__ == "__main__":
    signals = collections.deque()
    signal_handler = signal_handler_mod.SignalHandler(signals)
    game = game_mod.Game(signal_handler)
    game.start_game()

    # simulate gui
    while True:
        # TODO MEGA NOTE! BECAUSE WE ONLY CALL STUFF IF CONSUMED SIGNAL:
        # TODO MEGA NOTE! BECAUSE WE ONLY CALL STUFF IF CONSUMED SIGNAL:
        # TODO MEGA NOTE! BECAUSE WE ONLY CALL STUFF IF CONSUMED SIGNAL:
        # WE CAN'T CALL ADVANCE MULTIPLE TIMES!
        # WE AUTOMATICALLY CAN ONLY CALL PER SIGNAL!
        # If this runs on multi threads we might STILL get races BUT
        # tech (out side of multi thread races, potentially) they need a signal
        # to do ANYTHING (at least, to interact with game)!
        # TODO This means a we may just have failed input throw exception
        # ^ This lets us know we can't put in anymore input!
        # ^ Try to generalize this. Make it so all states inherit this basic
        # "throw exception on fail" stuff (if possible without messiness).
        if signals:
            dequeued_signal: "signal_mod.Signal" = signals.popleft()
            # TODO MAY NEED TO DO .EQUALS FOR STRINGS IN C++
            if dequeued_signal.NAME == signal_mod.ChooseStartingPlayer.NAME:
                # TODO Note, we separate into func for type checking & organization
                # noinspection PyTypeChecker
                choose_starting_player(dequeued_signal)
            elif dequeued_signal.NAME == signal_mod.InPriority.NAME:
                debug_info()
                # noinspection PyTypeChecker
                in_priority(dequeued_signal)
        # if signal.NAME == sgn.ChoosingPlayer.NAME:
            #     input_ = input("Choose starting player int: ")
            #     new_game.advance(int(input_))
            # elif signal.NAME == sgn.InPriority.NAME:
            #     input_ = input("In priority. May pass or play: ")
            #     new_game.advance(input_)

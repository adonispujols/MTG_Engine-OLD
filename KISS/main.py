import collections
from KISS import game
from KISS import signal_classes as sgn

if __name__ == "__main__":
    signals = collections.deque()
    new_game = game.Game(signals)
    new_game.start_game()

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
            signal: "sgn.Signal" = signals.popleft()
            if signal.NAME == sgn.ChoosingPlayer.NAME:
                input_ = input("Choose starting player int: ")
                new_game.advance(int(input_))
            elif signal.NAME == sgn.InPriority.NAME:
                input_ = input("In priority. May pass or play: ")
                new_game.advance(input_)

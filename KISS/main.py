from KISS import game
import collections

if __name__ == "__main__":
    signals = collections.deque()
    # automatically calls choose 1st player, starting game
    new_game = game.Game(signals)
    new_game.start_game()

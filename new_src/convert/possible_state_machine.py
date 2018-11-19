import tkinter as tk
import abc
from new_src.convert import passes
from new_src.convert import player as player_mod
from new_src.convert import stack
from new_src.convert import card as card_mod
from new_src.convert import deck
from new_src.convert import hand


class Game(tk.Frame):
    def __init__(self, parent=None):
        # gui
        super().__init__(parent)
        self.parent = parent
        self.init_gui()
        # main logic
        self.debug = True
        self.ai_only = False
        self.players = [player_mod.Player(), player_mod.Player()]
        self.battlefield = []
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # initially none until 1st turn
        self.step_or_phase = None
        # state machine
        # current state set in main
        self.current_state = None

    # gui
    def init_gui(self):
        self.grid()
        # noinspection PyAttributeOutsideInit
        self.test_button = tk.Button(self, text="test", command=None)
        # self.hi_there["text"] = "test"
        self.test_button.grid()

    # main logic
    def initialize(self):
        self.players[0].deck = deck.Deck()
        self.players[0].hand = hand.Hand()
        self.players[1].deck = deck.Deck()
        self.players[1].hand = hand.Hand()
        for i in range(10):
            self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
            self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
        for i in range(10):
            self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
            self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))
        for _ in self.players:
            self.battlefield.append([])
        # [CR 103.1], 1st part of starting game
        self._shuffle_all()

    def _shuffle_all(self):
        for player in self.game.players:
            player.deck.shuffle()

    # state machine
    def advance(self, event):
        self.current_state = self.current_state.next(event)
        self.current_state.run()


class State(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def next(self, event):
        pass


# According to [CR 103]
class StartGame(State):
    def __init__(self, game: "Game"):
        self.game = game

    def run(self):
        # [CR 103.1]
        self._shuffle_all()

    def next(self, event):
        pass

    def _shuffle_all(self):
        for player in self.game.players:
            player.deck.shuffle()


if __name__ == "__main__":
    root = tk.Tk()
    app = Game(parent=root)

    Game.start_game = StartGame(app)
    Game.current_state = Game.start_game

    # do NOT remove these three lines (lift, attributes, after_idle)
    # needed to automatically bring tkinter window to front.
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.after_idle(Game.current_state.run())
    root.mainloop()

import tkinter as tk
import abc
from new_src.convert import passes
from new_src.convert import player as player_mod
from new_src.convert import stack
from new_src.convert import card as card_mod
from new_src.convert import deck
from new_src.convert import hand

# class StateMachine:
#     def __init__(self, initial_state):
#         self.current_state = initial_state
#         self.current_state.run()
#
#     # Template method:
#     def advance(self, input):
#             self.current_state = self.current_state.next(input)
#             self.current_state.run()
#
#


class MTGEngine(tk.Frame):
    def __init__(self, initial_state: "State", master=None):
        # gui
        super().__init__(master)
        self.master = master
        self.init_gui()
        # main logic
        self.debug = True
        self.ai_only = False
        self.players = [player_mod.Player(), player_mod.Player()]
        self.players[0].deck = deck.Deck()
        self.players[0].hand = hand.Hand()
        self.players[1].deck = deck.Deck()
        self.players[1].hand = hand.Hand()
        self._fill_decks()
        self.battlefield = []
        self._init_battlefield()
        self._stack = stack.Stack()
        self._passes = passes.Passes()
        # initially none until 1st turn
        self.step_or_phase = None
        # state machine
        self.current_state = initial_state
        self.current_state.run()

    # gui
    def init_gui(self):
        self.grid()
        # noinspection PyAttributeOutsideInit
        self.test_button = tk.Button(self, text="test", command=None)
        # self.hi_there["text"] = "test"
        self.test_button.grid()

    # main logic
    def _fill_decks(self):
        for i in range(10):
            self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
            self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
        for i in range(10):
            self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
            self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))

    def _init_battlefield(self):
        for _ in self.players:
            self.battlefield.append([])

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





if __name__ == "__main__":
    root = tk.Tk()
    app = MTGEngine(master=root, )

    # lift and topmost = true automatically brings window to top
    # topmost = false so it isn't stuck on top
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()

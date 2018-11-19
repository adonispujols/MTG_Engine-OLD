import abc
import random
import functools
import typing

from new_src.convert import turn_actions



class State(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def next(self, event):
        pass


# According to [CR 103]
class ChoosingStartingPlayer(State):
    choose_btns: typing.List["tk.Button"]

    def __init__(self, game: "Game"):
        self.game = game
        self.choose_btns = []

    def run(self):
        # [CR 103.2]
        index = random.randrange(len(self.game.players))
        player_label = tk.Label(self.game,
                                text="P{0}, who goes first?".format(index + 1))
        player_label.grid()
        for i in self.game.players:
            choose_btn = tk.Button(self.game,
                                   text=i, command=functools.partial(self.game.advance, i))
            self.choose_btns.append(choose_btn)
            choose_btn.grid()
        # TODO give AI option/ability to choose

    def next(self, event):
        for btn in self.choose_btns:
            btn.destroy()
        # event = player index chosen
        # [CR 103.7]
        turn_actions.first_untap_(self.game, event)
        # TODO return result from turn actions


if __name__ == "__main__":
    root = tk.Tk()
    app = Game(parent=root)

    Game.choosing_starting_player = ChoosingStartingPlayer(app)
    Game.current_state = Game.choosing_starting_player

    # do NOT remove these three lines (lift, attributes, after_idle)
    # needed to automatically bring tkinter window to front.
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.after_idle(Game.current_state.run())
    root.mainloop()

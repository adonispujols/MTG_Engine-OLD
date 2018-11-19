import tkinter as tk
from convert import game
from convert import states

if __name__ == "__main__":
    root = tk.Tk()
    app = game.Game(parent=root)

    app.choosing_starting_player = states.ChoosingStartingPlayer(app)
    app.current_state = app.choosing_starting_player

    # do NOT remove these three lines (lift, attributes, after_idle)
    # needed to automatically bring tkinter window to front.
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.after_idle(app.current_state.run())
    root.mainloop()

import tkinter as tk
from convert import game

if __name__ == "__main__":
    root = tk.Tk()
    app = game.Game(parent=root)

    # do NOT remove these three lines (lift, attributes, after_idle)
    # ^ needed to automatically bring tkinter window to front.
    root.lift()
    root.attributes('-topmost', True)
    # XXX disabling here for easier debugging
    # root.after_idle(root.attributes, '-topmost', False)
    root.after_idle(app.current_state.run, None)
    root.mainloop()

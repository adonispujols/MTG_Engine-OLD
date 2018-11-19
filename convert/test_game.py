import unittest
import tkinter as tk
from unittest import TestCase

from convert import game


class TestGame(unittest.TestCase):
    def setUp(self):
        root = tk.Tk()
        self.app = game.Game(parent=root)

        # do NOT remove these three lines (lift, attributes, after_idle)
        # ^ needed to automatically bring tkinter window to front.
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)
        root.after_idle(self.test___init__())
        # root.after_idle(self.test)
        # root.after_idle(self.test2)
        # root.after_idle(self.app.current_state.run, None)
        root.mainloop()

    def test___init__(self):
        self.assertTrue(self.app._debug)
        self.assertFalse(self.app._ai_only)
        self.

    # def test__init_game(self):
    #     se


# def test(self):
#     print("yooooo")
#
# def test2(self):
#     print("niiiice")

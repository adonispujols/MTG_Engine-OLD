import unittest
import tkinter as tk
from unittest import TestCase

from convert import bindings as bnd

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
        # players
        self.assertListEqual(self.app._battlefield, [[], []])
        self.assertListEqual(self.app._stack._stack, [])
        self.assertEqual(self.app._passes._count, 0)
        self.assertIsNone(self.app.step_or_phase)
        self.assertEqual(self.players[0].deck)

        #         self.players[0].deck = deck.Deck()
        #         self.players[0].hand = hand.Hand()
        #         self.players[1].deck = deck.Deck()
        #         self.players[1].hand = hand.Hand()
        #         for i in range(10):
        #             self.players[0].deck.push(card_mod.Card("land_1 " + str(i), "Land"))
        #             self.players[1].deck.push(card_mod.Card("land_2 " + str(i), "Land"))
        #         for i in range(10):
        #             self.players[0].deck.push(card_mod.Card("creat_1 " + str(i), "Creature"))
        #             self.players[1].deck.push(card_mod.Card("creat_2 " + str(i), "Creature"))
        #         for _ in self.players:
        #             self._battlefield.append([])
        #         # [CR 103.1], 1st part of starting game
        #         for player in self.players:
        #             player.deck.shuffle()


    def test__init_gui(self):
        self.assertEqual(bnd.Bindings.ADVANCE, "<<Advance>>")

    # implicitly tested by test___init__
    # def test__init_game(self):
        # self.fail()


import collections
from KISS import signals as signal_mod


class SignalHandler:
    def __init__(self, gui_context: "collections.deque"):
        self.gui_context = gui_context

    def emit_signal(self, signal: "signal_mod.Signal"):
        self.gui_context.append(signal)

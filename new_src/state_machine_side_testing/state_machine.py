# import tkinter as tk
#
#
# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")
#
#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")
#
#     def say_hi(self):
#         print("hi there, everyone!")
#
#
# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()


# StateMachine/StateMachine.py
# Takes a list of Inputs to move from State to
# State using a template method.


# class StateMachine:
#     def __init__(self, initial_state):
#         self.current_state = initial_state
#         self.current_state.run()
#
#     # Template method:
#     def advance(self, input):
#             self.current_state = self.current_state.next(input)
#             self.current_state.run()



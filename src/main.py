import abc


class Foo(abc.ABC):
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def bar(self, x):
        print(x, "basic functionality")


class Test(Foo):
    def __init__(self):
        super().__init__()

    def bar(self):
        super().bar(45)
        print("legit")


f = Test()
f.bar()

# when ready for tkinter:
# import tkinter as tk
#
# root = tk.Tk()
# root.title("test")
# # lift and topmost = true automatically brings window to top
# # topmost = false so it isn't stuck on top
# root.lift()
# root.attributes('-topmost',True)
# root.after_idle(root.attributes,'-topmost',False)
# root.mainloop()

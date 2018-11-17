import tkinter as tk
import functools

def get_entry():
    print(e1.get())


def test():
    print("doing test")
    for i in range(7):
        # new_button = tk.Button(root, text=("button " + str(i)), command=lambda n=i: test_2(n))
        new_button = tk.Button(root, text=("button " + str(i)), command=functools.partial(test_2, i))
        new_button.pack()


def test_2(index):
    print("test 2 done. i: ", index)


class TestClass:
    def __init__(self, main_root):
        print("root background is %s" % main_root.cget("background"))


root = tk.Tk()
root.title("title")

test_class = TestClass(root)

label1 = tk.Label(root, text="test label")
e1 = tk.Entry(root)
button = tk.Button(root, text="button", command=test)

label1.pack()
e1.pack()
button.pack()

# lift and topmost = true automatically brings window to top
# topmost = false so it isn't stuck on top
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes, '-topmost', False)
root.mainloop()
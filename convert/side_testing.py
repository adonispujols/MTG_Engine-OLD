import tkinter as tk
import functools


def test():
    print("doing test")
    for i in range(7):
        # new_button = tk.Button(root, text=("button " + str(i)), command=lambda n=i: test_2(n))
        new_button = tk.Button(root, text=("button " + str(i)), command=functools.partial(test_2, i))
        new_button.grid()


def test_2(index):
    print("test 2 done. i: ", index)

root = tk.Tk()
root.title("title")
button = tk.Button(root, text="button", command=test)
button.grid()
# TODO USE .config(command="") TO REMOVE COMMANDS FROM BUTTONS, NOT UNBIND!
# button.config(command="")
# TODO DON'T REMOVE COMMAND/BUTTON IF YOU WANT IT TO STAY. DISABLE BUTTON, INSTEAD!
# button.config(state=tk.DISABLED)


pic = tk.PhotoImage(file="test_pic.png")
test_button = tk.Button(root, image=pic)
test_button.grid()

# lift and topmost = true automatically brings window to top
# topmost = false so it isn't stuck on top
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)
root.mainloop()

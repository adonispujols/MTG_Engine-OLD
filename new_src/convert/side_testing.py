# import time
# import tkinter as tk
# import functools
#
#
# def test():
#     print("doing test")
#     for i in range(7):
#         # new_button = tk.Button(root, text=("button " + str(i)), command=lambda n=i: test_2(n))
#         new_button = tk.Button(root, text=("button " + str(i)), command=functools.partial(test_2, i))
#         new_button.grid()
#
#
# def test_2(index):
#     print("test 2 done. i: ", index)
#     time.sleep(.1)
#
#
# def okay():
#     print("okay")
#
#
# root = tk.Tk()
# root.title("title")
#
# button = tk.Button(root, text="button", command=test)
# okay_button = tk.Button(root, text="okay", command=okay)
#
# button.grid()
# okay_button.grid()
#
# # lift and topmost = true automatically brings window to top
# # topmost = false so it isn't stuck on top
# root.lift()
# root.attributes('-topmost', True)
# root.after_idle(root.attributes, '-topmost', False)
# root.mainloop()

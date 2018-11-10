
# when ready for tkinter:
# """
import tkinter as tk

root = tk.Tk()
root.title("test")
# lift and topmost = true automatically brings window to top
# topmost = false so it isn't stuck on top
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.mainloop()
# """

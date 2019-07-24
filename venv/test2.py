import tkinter

root = tkinter.Tk()
root.title("root")

top = tkinter.Toplevel(root)
top.title("top")
top.lift(root)
root.mainloop()
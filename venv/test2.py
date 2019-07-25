import tkinter

root = tkinter.Tk()
root.title("root")

top = tkinter.Toplevel(root)
top.title("top")
top.lift(root)
root.mainloop()

s=[1,2,3]
print(*s)
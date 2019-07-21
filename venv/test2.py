import tkinter as tk

master = tk.Tk()

var = tk.StringVar(master)
var.set("one") # initial value

option = tk.OptionMenu(master, var, "one", "two", "three", "four")
option.pack()

#
# test stuff

def ok():
    print ("value is", var.get())
    master.quit()

button = tk.Button(master, text="OK", command=ok)
button.pack()

master.mainloop()

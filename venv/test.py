
import tkinter as tk
class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # here is the application variable
        self.contents = tk.StringVar()
        # set it to some value
        self.contents.set("this is a variable")
        # tell the entry widget to watch this variable
        self.entrythingy["textvariable"] = self.contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entrythingy.bind('<Key-Return>',
                              self.print_contents)

    def print_contents(self, event):
        print("hi. contents of entry is now ---->",
              self.contents.get())

root = tk.Tk()
app = App(master=root)
app.mainloop()


class Prof:
    def __init__(self, prof_id, name="", telephone=''):
        self.prof_id = str(prof_id)
        self.name = name
        self.telephone = str(telephone)
        self.schedule = [[], [], [], [], [], [], []]
        self.time_preferred = []
        self.time_occupied = []
        self.important_info=[prof_id]


p=Prof(1,'sads','asd')
print(p.important_info)
p.prof_id=2
print(p.important_info)

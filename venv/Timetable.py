import tkinter as tk

import Constants as c
import Prof
import operations_gui as og


class Timetable:
    def __init__(self):
        self.timetable = [[0 for x in range(7)] for y in range(12)]

    def __str__(self):
        res = ''
        for i in range(len(self.timetable)):
            for j in range(len(self.timetable[0])):
                if self.timetable[i][j] == 1 or self.timetable[i][j] == '1':
                    res += c.WEEK[j] + ' period ' + str(i) + ' '
        return res if res else 'N/A'

    def show(self, page_name, parent=None):
        timetable_page = tk.Toplevel()
        timetable_page.title(page_name)
        var_array = []

        def save():
            for i in range(12):
                for j in range(7):
                    self.timetable[i][j] = var_array[i][j].get()
            if parent and isinstance(parent, Prof.Prof):
                og.show_prof_info(parent)
            timetable_page.destroy()

        for j in range(7):
            b = tk.Label(timetable_page, text=c.WEEK[j])
            b.grid(row=0, column=j + 1)
        for i in range(12):
            b = tk.Label(timetable_page, text='period' + str(i + 1))
            b.grid(row=i + 1, column=0)

        for i in range(12):
            var_array.append([])
            for j in range(7):
                v = tk.Variable()
                v.set(self.timetable[i][j])
                b = tk.Checkbutton(timetable_page, variable=v)
                b.grid(row=i + 1, column=j + 1)
                var_array[i].append(v)

        b = tk.Button(timetable_page, text='Save & Quit', command=save)
        b.grid()
        return timetable_page

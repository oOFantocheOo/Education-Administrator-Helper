import tkinter as tk

import Constants as c
import Prof
import operations_gui as og


class Timetable:
    def __init__(self):
        self.timetable = [[0 for x in range(7)] for y in range(12)]

    def __str__(self):  # to be modified
        res = ''
        for i in range(len(self.timetable)):
            for j in range(len(self.timetable[0])):
                if self.timetable[i][j] == 1 or self.timetable[i][j] == '1':
                    res += c.WEEK[j] + ' period ' + str(i) + ' '
        return res if res else str(self.timetable)

    def show(self, page_name='.', parent=None):
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

    # Update using Timetable_2: if Timetable_2[i][j] == value_from, self[i][j] = value_to
    # Return error message if any changing self[i][j] is not in possible_values_1
    # or any Timetable_2[i][j] is not in possible_values_2
    def update_based_on(self, Timetable_2, possible_values_1, possible_values_2, value_from, value_to):
        errors = []
        if str(value_from) not in possible_values_2:
            errors.append(
                'value_from should not be ' + str(value_from) + ', but it can be one of ' + str(
                    possible_values_2))
        for i in range(len(possible_values_1)):
            possible_values_1[i] = str(possible_values_1[i])
        for i in range(len(possible_values_2)):
            possible_values_2[i] = str(possible_values_2[i])
        for r in range(len(self.timetable)):
            for c in range(len(self.timetable[0])):
                if str(Timetable_2.timetable[r][c]) == str(value_from):
                    if str(self.timetable[r][c]) not in possible_values_1:
                        errors.append(
                            str(self) + '[' + str(r) + ']' + '[' + str(c) + ']' + ' should not be ' + str(
                                self.timetable[r][c]) + ', but it can be one of ' + str(possible_values_1))
                    else:
                        self.timetable[r][c] = str(value_to)
                else:
                    if str(Timetable_2.timetable[r][c]) not in possible_values_2:
                        errors.append(
                            str(Timetable_2) + '[' + str(r) + ']' + '[' + str(c) + ']' + ' should not be ' + str(
                                self.timetable[r][c]) + ', but it can be one of ' + str(possible_values_2))
        return errors

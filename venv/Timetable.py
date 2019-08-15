import tkinter as tk

import Constants as c
import Prof
import operations_gui as og


class Timetable:
    def __init__(self, title=''):
        self.timetable = [['0' for x in range(7)] for y in range(12)]
        self.title = title

    def all_zeros(self):
        def all_zeros_1d(L):
            return all(x == 0 or x == '0' for x in L)

        return all(all_zeros_1d(a) for a in self.timetable)

    def __str__(self):  # to be modified
        if self.all_zeros():
            return 'N/A'

        res = ''
        for i in range(len(self.timetable)):
            for j in range(len(self.timetable[0])):
                if self.timetable[i][j] == 1 or self.timetable[i][j] == '1':
                    res += c.WEEK[j] + ' period ' + str(int(i) + 1) + ' '
        return res if res else str(self.timetable)

    def show(self, page_name='.', parent=None):
        timetable_page = tk.Toplevel()
        timetable_page.focus_force()
        timetable_page.grab_set()
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

    # Check if every time when Timetable_2[i][j] == value_2, self[i][j] == value_1
    def check(self, Timetable_2, value_1, value_2):
        err = []
        for r in range(len(self.timetable)):
            for c in range(len(self.timetable[0])):
                if str(Timetable_2.timetable[r][c]) == str(value_2):
                    if str(self.timetable[r][c]) != value_1:
                        err.append(self.title + '[' + str(r) + '][' + str(c) + "] shouldn't be " + self.timetable[r][c] + '; it will be overwritten; correction: ' + str(value_1))

        return err

    # Set self[i][j] = value_1 every time when Timetable_2[i][j] == value_2
    def change(self, Timetable_2, value_1, value_2):
        for r in range(len(self.timetable)):
            for c in range(len(self.timetable[0])):
                if str(Timetable_2.timetable[r][c]) == str(value_2):
                    self.timetable[r][c] = value_1

    # Return the least occupied day in a week; 0:Monday, 6:Sunday
    def least_occupied(self):
        idx, empty_slot = -1, -1
        for c in range(7):
            cur_empty_slot = 0
            for r in range(12):
                if self.timetable[r][c] == '0':
                    cur_empty_slot += 1
            if cur_empty_slot > empty_slot:
                idx, empty_slot = c, cur_empty_slot
        return idx

    def get_ones_as_list(self):
        res = []
        for i in range(12):
            for j in range(7):
                if self.timetable[i][j] in [1, '1']:
                    res.append((i, j))
        return res

    def is_available(self, period, date):
        if self.timetable[period][date] in [0, '0']:
            return True
        else:
            return False

    def change_one_period(self, period, date, content):
        self.timetable[period][date] = content

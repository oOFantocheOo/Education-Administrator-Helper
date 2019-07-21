import tkinter as tk

import Constants as c
import operations_breaktime as ob
import operations_course as oc
import operations_profs as op


def show_succeed_message():
    temp = tk.Tk()
    tk.Label(temp, text='Succeeded!').pack()
    tk.Button(temp, text='OK', command=temp.destroy).pack()


def show_root_page(profs, courses, class_list, break_time):
    root = tk.Tk()
    root.title("Educational Administration Helper")
    button1 = tk.Button(root, text="Generate Timetable")
    button1.pack()
    button2 = tk.Button(root, text="Prof info", command=lambda: show_prof_page(profs))
    button2.pack()
    button3 = tk.Button(root, text="Course info", command=lambda: show_course_page(courses))
    button3.pack()
    button4 = tk.Button(root, text="Class info", command=lambda: show_class_page(class_list))
    button4.pack()
    button5 = tk.Button(root, text="Set Break Time", command=lambda: show_breaktime_page(break_time))
    button5.pack()
    button6 = tk.Button(root, text="Set Rules", command=show_rule_page)
    button6.pack()
    button7 = tk.Button(root, text='Check Conflicts', command=show_checking_page)
    button7.pack()
    root.mainloop()


def show_checking_page():
    pass


def show_prof_page(profs):
    def find_prof_widget():
        fp = tk.Tk()
        fp.title("Find A Professor")
        tk.Label(fp, text="Enter the professor's name").pack()
        e = tk.Entry(fp)
        e.pack()
        tk.Button(fp, text='OK', command=lambda: show_prof_info(op.find_prof(profs, e.get()))).pack(side='left')
        tk.Button(fp, text='Cancel', command=fp.destroy).pack()

    def add_prof_widget():
        ap = tk.Tk()
        ap.title("Add A Professor")
        tk.Label(ap, text="Enter the professor's name").pack()
        e = tk.Entry(ap)
        e.pack()
        tk.Button(ap, text='OK').pack(side='left')
        tk.Button(ap, text='Cancel', command=ap.destroy).pack()

    def delete_prof_widget():
        dp = tk.Tk()
        dp.title("Delete A Professor")
        tk.Label(dp, text="Enter the professor's name").pack()
        e = tk.Entry(dp)
        e.pack()
        tk.Button(dp, text='OK').pack(side='left')
        tk.Button(dp, text='Cancel', command=dp.destroy).pack()

    prof_page = tk.Tk()
    prof_page.title("Prof Information")
    label = tk.Label(prof_page, text=op.all_profs_info(profs))
    label.pack()
    button1 = tk.Button(prof_page, text="Find Prof", command=find_prof_widget)
    button1.pack()
    button2 = tk.Button(prof_page, text="Add Prof", command=add_prof_widget)
    button2.pack()
    button3 = tk.Button(prof_page, text="Delete Prof", command=delete_prof_widget)
    button3.pack()


def show_course_page(courses):
    course_page = tk.Tk()
    course_page.title("Course Information")
    label = tk.Label(course_page, text=oc.all_courses_info(courses))
    label.pack()
    course_page.mainloop()


def show_class_page(classes):
    class_page = tk.Tk()
    class_page.title("Class Information")
    class_page.mainloop()


def show_breaktime_page(breaktime):
    breaktime_page = tk.Toplevel()
    breaktime_page.title("Break Time")
    height = 12
    width = 7
    button_array = []
    var_array = []

    def save_break_time():
        for i in range(height):
            for j in range(width):
                breaktime[i][j] = var_array[i][j].get()
        ob.save_breaktime(breaktime)
        breaktime_page.destroy()

    for j in range(width):
        b = tk.Label(breaktime_page, text=c.WEEK[j])
        b.grid(row=0, column=j + 1)
    for i in range(height):
        b = tk.Label(breaktime_page, text='period' + str(i + 1))
        b.grid(row=i + 1, column=0)

    for i in range(height):
        button_array.append([])
        var_array.append([])
        for j in range(width):
            v = tk.Variable()
            v.set(breaktime[i][j])
            b = tk.Checkbutton(breaktime_page, variable=v)
            b.grid(row=i + 1, column=j + 1)
            button_array[i].append(b)
            var_array[i].append(v)

    b = tk.Button(breaktime_page, text='Save & Quit', command=save_break_time)
    b.grid()


def show_rule_page():
    rule_page = tk.Tk()
    rule_page.title("Rules")
    rule_page.mainloop()


def show_prof_info(prof):
    p = tk.Toplevel()
    p.title("Professor Information")
    if not prof:
        tk.Label(p, text='Professor not found').pack()
        tk.Button(p, text='OK', command=p.destroy).pack()
        return
    l = tk.Label(p, text=prof.complete_info())
    l.pack()

    def clear_TP():
        prof.clear_time_preference()
        show_succeed_message()
        l['text'] = prof.complete_info()

    def add_preferred_time():
        apt = tk.Toplevel()
        apt.title("Add Preferred Time")
        day_chosen = tk.StringVar()
        day_chosen.set(c.WEEK[0])
        tk.Label(apt, text="Day of the week").pack()
        tk.OptionMenu(apt, day_chosen, *c.WEEK).pack()

    tk.Button(p, text="Clear Time Preference", command=clear_TP).pack(side='left')
    tk.Button(p, text="Add Time Preferred", command=add_preferred_time).pack(side='left')
    tk.Button(p, text="Add Time Not Possible").pack(side='left')

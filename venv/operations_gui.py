import tkinter as tk

import operations_course as oc
import operations_profs as op


def show_succeed_message():
    temp = tk.Tk()
    tk.Label(temp, text='Succeeded!').pack()
    tk.Button(temp, text='OK', command=temp.destroy).pack()


def show_root_page(profs, courses):
    root = tk.Tk()
    root.title("Educational Administration Helper")
    button1 = tk.Button(root, text="Generate Timetable")
    button1.pack()
    button2 = tk.Button(root, text="Prof info", command=lambda: show_prof_page(profs))
    button2.pack()
    button3 = tk.Button(root, text="Course info", command=lambda: show_course_page(courses))
    button3.pack()
    button4 = tk.Button(root, text="Class info", command=show_class_page)
    button4.pack()
    button5 = tk.Button(root, text="Set Break Time", command=show_breaktime_page)
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


def show_class_page():
    class_page = tk.Tk()
    class_page.title("Class Information")
    class_page.mainloop()


def show_breaktime_page(breaktime):
    breaktime_page = tk.Tk()
    breaktime_page.title("Break Time")
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    height = 12
    width = 7

    for j in range(width):
        b = tk.Label(breaktime_page, text=week[j])
        b.grid(row=0, column=j+1)
    for i in range(height):
        b = tk.Label(breaktime_page, text='period'+str(i+1))
        b.grid(row=i+1, column=0)


    for i in range(height):
        for j in range(width):
            b = tk.Checkbutton(breaktime_page, text="")
            b.grid(row=i + 1, column=j+1)
    breaktime_page.mainloop()


def show_rule_page():
    rule_page = tk.Tk()
    rule_page.title("Rules")
    rule_page.mainloop()


def show_prof_info(prof):
    p = tk.Tk()
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

    tk.Button(p, text="Clear Time Preference", command=clear_TP).pack(side='left')
    tk.Button(p, text="Add Time Preferred").pack(side='left')
    tk.Button(p, text="Add Time Not Possible").pack(side='left')

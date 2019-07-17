import tkinter as tk

import operations_course as oc
import operations_profs as op


def show_root_page():
    root = tk.Tk()
    root.title("Educational Administration Helper")

    button1 = tk.Button(root, text="Generate Timetable")
    button1.pack()
    button2 = tk.Button(root, text="Prof info", command=show_prof_page)
    button2.pack()
    button3 = tk.Button(root, text="Course info", command=show_course_page)
    button3.pack()
    button4 = tk.Button(root, text="Class info", command=show_class_page)
    button4.pack()
    button5 = tk.Button(root, text="Set Break Time", command=show_breaktime_page)
    button5.pack()
    button6 = tk.Button(root, text="Set Rules", command=show_rule_page)
    button6.pack()

    root.mainloop()


def show_prof_page():
    def find_prof_widget():
        fp = tk.Tk()
        fp.title("Find A Professor")
        tk.Label(fp, text="Enter the professor's name").pack()
        e = tk.Entry(fp)
        e.pack()
        tk.Button(fp, text='OK', command=lambda: op.find_prof(e["textvariable"])).pack(side='left')
        tk.Button(fp, text='Cancel', command=fp.destroy).pack()

    prof_page = tk.Tk()
    prof_page.title("Prof Information")
    label = tk.Label(prof_page, text=op.all_profs_info())
    label.pack()
    button = tk.Button(prof_page, text="Find Prof", command=find_prof_widget)
    button.pack()
    prof_page.mainloop()


def show_course_page():
    course_page = tk.Tk()
    course_page.title("Course Information")
    label = tk.Label(course_page, text=oc.all_courses_info())
    label.pack()
    course_page.mainloop()


def show_class_page():
    class_page = tk.Tk()
    class_page.title("Class Information")
    class_page.mainloop()


def show_breaktime_page():
    breaktime_page = tk.Tk()
    breaktime_page.title("Break Time")
    breaktime_page.mainloop()


def show_rule_page():
    rule_page = tk.Tk()
    rule_page.title("Rules")
    rule_page.mainloop()

def show_prof_info
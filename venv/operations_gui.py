import tkinter as tk

import SchoolTimetable as st
import operations_course as oc
import operations_profs as op


def show_succeed_message():
    temp = tk.Toplevel()
    tk.Label(temp, text='Succeeded!').pack()
    tk.Button(temp, text='OK', command=temp.destroy).pack()


def show_root_page(profs, courses, class_list, break_time):
    root = tk.Tk()
    root.geometry('600x400')
    root.title("Educational Administration Helper")
    button1 = tk.Button(root, text="Generate Timetable",
                        command=lambda: st.generate_school_timetable(profs, courses, class_list, break_time))
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
        fp = tk.Toplevel()
        fp.title("Find A Professor")
        tk.Label(fp, text="Enter the professor's name").pack()
        e = tk.Entry(fp)
        e.pack()
        tk.Button(fp, text='OK', command=lambda: show_prof_info(op.find_prof(profs, e.get()), fp)).pack(side='left')
        tk.Button(fp, text='Cancel', command=fp.destroy).pack()

    def add_prof_widget():
        ap = tk.Toplevel()
        ap.title("Add A Professor")
        tk.Label(ap, text="Not implemented").pack()
        tk.Button(ap, text='Cancel', command=ap.destroy).pack()

    def delete_prof_widget():
        dp = tk.Toplevel()
        dp.title("Delete A Professor")
        tk.Label(dp, text="Not implemented").pack()
        tk.Button(dp, text='Cancel', command=dp.destroy).pack()

    def clear_all_preference():
        for i in profs.keys():
            profs[i].clear_time_preference()
        show_succeed_message()

    prof_page = tk.Toplevel()
    prof_page.title("Prof Information")

    for pid in profs.keys():
        tk.Label(prof_page, text=profs[pid]).pack()
        tk.Button(prof_page, text='Details..', command=lambda a=pid: show_prof_info(profs[a])).pack()

    button1 = tk.Button(prof_page, text="Find Prof", command=find_prof_widget)
    button1.pack()
    button2 = tk.Button(prof_page, text="Add Prof", command=add_prof_widget)
    button2.pack()
    button3 = tk.Button(prof_page, text="Delete Prof", command=delete_prof_widget)
    button3.pack()
    button4 = tk.Button(prof_page, text='Clear All Preference', command=clear_all_preference)
    button4.pack()


def show_course_page(courses):
    course_page = tk.Toplevel()
    course_page.title("Course Information")
    v1 = tk.Variable()
    v2 = tk.Variable()
    v3 = tk.Variable()
    v4 = tk.Variable()
    v1.set(1)
    v2.set(1)
    v3.set(1)
    v4.set(1)
    courses_to_be_shown = []
    label = tk.Label(course_page, text=oc.all_courses_info(courses))

    def update_courses_shown():
        courses_to_be_shown.clear()
        for ck in courses.keys():
            if courses[ck].scheduled_manually and int(v1.get()) == 1:
                courses_to_be_shown.append(courses[ck])
            elif not courses[ck].scheduled_manually and int(v2.get()) == 1:
                courses_to_be_shown.append(courses[ck])
            elif courses[ck].should_be_scheduled and int(v3.get()) == 1:
                courses_to_be_shown.append(courses[ck])
            elif not courses[ck].should_be_scheduled and int(v4.get()) == 1:
                courses_to_be_shown.append(courses[ck])
            label['text'] = oc.selected_courses_info(courses_to_be_shown)

    b1 = tk.Checkbutton(course_page, variable=v1, text='Scheduled manually', command=update_courses_shown).pack()
    b2 = tk.Checkbutton(course_page, variable=v2, text='Scheduled automatically', command=update_courses_shown).pack()
    b3 = tk.Checkbutton(course_page, variable=v3, text='Should be scheduled', command=update_courses_shown).pack()
    b4 = tk.Checkbutton(course_page, variable=v4, text='Should not be scheduled', command=update_courses_shown).pack()
    label.pack()


def show_class_page(classes):
    class_page = tk.Toplevel()
    class_page.title("Class Information")


def show_breaktime_page(breaktime):
    breaktime.show('Breaktime')


def show_rule_page():
    rule_page = tk.Toplevel()
    rule_page.title("Rules")


def show_prof_info(prof, prev_page=None):
    p = tk.Toplevel()
    p.title("Professor Information")
    if not prof:
        tk.Label(p, text='Professor not found').pack()
        tk.Button(p, text='OK', command=p.destroy).pack()
        return
    l = tk.Label(p, text=prof.complete_info())
    l.pack()
    if prev_page:
        prev_page.destroy()

    def update_label():
        l['text'] = prof.complete_info()

    def clear_TP():
        prof.clear_time_preference()
        show_succeed_message()
        update_label()

    def change_preferred_time():
        prof.time_preferred.show(prof.name + "'s Preferred Time", prof)
        p.destroy()

    def change_impossible_time():
        prof.time_not_possible.show(prof.name + "'s Impossible Time", prof)
        p.destroy()

    tk.Button(p, text="Clear Time Preference", command=clear_TP).pack(side='left')
    tk.Button(p, text="Change Time Preferred", command=change_preferred_time).pack(side='left')
    tk.Button(p, text="Add Time Not Possible", command=change_impossible_time).pack(side='left')

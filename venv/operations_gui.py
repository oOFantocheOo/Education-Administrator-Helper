import tkinter as tk

import SchoolTimetable as st
import operations_course as oc
import operations_profs as op


def show_succeed_message():
    temp = tk.Toplevel()
    tk.Label(temp, text='Succeeded!').pack()
    tk.Button(temp, text='OK', command=temp.destroy, default='active').pack()
    temp.focus_force()
    return temp


def show_waiting_message():
    temp = tk.Toplevel()
    tk.Label(temp, text='Please wait...').pack()
    return temp


def show_error_message(error):
    temp = tk.Toplevel()
    tk.Label(temp, text='Error! ' + error).pack()
    tk.Button(temp, text='OK', command=temp.destroy, default='active').pack()
    temp.focus_force()
    return temp


def show_root_page(profs, courses, class_list, break_time):
    school_timetable = [None]  # wrapped as list for modification
    root = tk.Tk()

    def show_school_timetable_widget(parent):
        st_widget = tk.Toplevel(parent)
        st_widget.geometry('300x200')
        st_widget.focus_force()

        def create_empty_school_timetable(week_num, title):
            school_timetable[0] = st.SchoolTimetable(week_num, title)
            label['text'] = 'School timetable initialized'
            st_widget.destroy()

        st_widget.title('Create School Timetable')
        tk.Label(st_widget, text='Title of school timetable:').pack()
        e1 = tk.Entry(st_widget)
        e1.insert(tk.END, 'qwe')
        e1.pack()
        tk.Label(st_widget, text='Number of weeks:').pack()
        e2 = tk.Entry(st_widget)
        e2.insert(tk.END, 3)
        e2.pack()
        tk.Button(st_widget, text='OK', command=lambda: create_empty_school_timetable(e2.get(), e1.get())).pack()
        tk.Button(st_widget, text='Cancel', command=st_widget.destroy).pack()

    def check_and_build_school_timatable():
        if not school_timetable[0]:
            return
        else:
            school_timetable[0].generate_school_timetable(profs, courses, class_list, break_time)

    root.geometry('600x400')
    root.title("Educational Administration Helper")
    button1 = tk.Button(root, text="Set Timetable", command=lambda: show_school_timetable_widget(root))
    button1.pack()
    label = tk.Label(root, text='School timetable not initialized yet!')
    label.pack()
    button2 = tk.Button(root, text="Prof info", command=lambda: show_prof_page(profs))
    button2.pack()
    button3 = tk.Button(root, text="Course info", command=lambda: show_course_page(courses, class_list, profs))
    button3.pack()
    button4 = tk.Button(root, text="Class info", command=lambda: show_class_page(class_list))
    button4.pack()
    button5 = tk.Button(root, text="Set Break Time", command=lambda: show_breaktime_page(break_time))
    button5.pack()
    button6 = tk.Button(root, text="Set Rules", command=show_rule_page)
    button6.pack()
    button7 = tk.Button(root, text='Check Conflicts', command=show_checking_page)
    button7.pack()
    button8 = tk.Button(root, text='Generate Timetable', command=check_and_build_school_timatable)
    button8.pack()

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


def show_course_page(courses, classes, profs):
    def find_course_by_title_widget():
        fc = tk.Toplevel()
        fc.focus_force()
        fc.title("Find A Course")
        tk.Label(fc, text="Enter the course's title").pack()
        e = tk.Entry(fc)
        e.insert(tk.END, 'intro to comp sci')
        e.pack()
        tk.Button(fc, text='OK',
                  command=lambda: show_course_info(oc.find_course_by_title(courses, e.get()), classes, profs, fc)).pack(
            side='left')
        tk.Button(fc, text='Cancel', command=fc.destroy).pack()

    def find_course_by_id_widget():
        fc = tk.Toplevel()
        fc.focus_force()
        fc.title("Find A Course")
        tk.Label(fc, text="Enter the course ID").pack()
        e = tk.Entry(fc)
        e.insert(tk.END, '1')
        e.pack()
        tk.Button(fc, text='OK',
                  command=lambda: show_course_info(oc.find_course_by_course_id(courses, e.get()), classes, profs,
                                                   fc)).pack(
            side='left')
        tk.Button(fc, text='Cancel', command=fc.destroy).pack()

    course_page = tk.Toplevel()
    course_page.focus_force()
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
    button1 = tk.Button(course_page, text="Find Course by Title", command=find_course_by_title_widget)
    button1.pack()
    button2 = tk.Button(course_page, text="Find Course by Course ID", command=find_course_by_id_widget)
    button2.pack()


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


def show_course_info(course, classes, profs, prev_page=None):
    c = tk.Toplevel()
    c.title("Course Information")
    if not course:
        tk.Label(c, text='Course not found').pack()
        tk.Button(c, text='OK', command=c.destroy).pack()
        return
    l = tk.Label(c, text=course.complete_info())
    l.pack()
    if prev_page:
        prev_page.destroy()

    def update_label():
        l['text'] = course.complete_info()

    def set_scheduled_manually():
        course.set_scheduled_manually()
        show_succeed_message()
        update_label()

    def set_not_scheduled_manually():
        course.set_not_scheduled_manually()
        show_succeed_message()
        update_label()

    def set_should_be_scheduled():
        course.set_should_be_scheduled()
        show_succeed_message()
        update_label()

    def set_should_not_be_scheduled():
        course.set_should_not_be_scheduled()
        show_succeed_message()
        update_label()

    def set_required_period():
        if not course.should_be_scheduled:
            show_error_message('This course should not be scheduled')
            return
        course.period_required.show('Course Required Period', course)
        c.destroy()

    def rebind_classes():
        course.clear_classes()
        update_label()
        rc = tk.Toplevel()
        rc.title('Rebind Classes')
        label1 = tk.Label(rc, text='Major').pack()
        entry1 = tk.Entry(rc)
        entry1.pack()

        label2 = tk.Label(rc, text='Grade').pack()
        entry2 = tk.Entry(rc)
        entry2.pack()

        label3 = tk.Label(rc, text='Index').pack()
        entry3 = tk.Entry(rc)
        entry3.pack()

        def find_class():
            class_id = str(entry1.get()) + str(entry2.get()) + str(entry3.get())
            if class_id not in classes:
                show_error_message('Class not found!')
            else:
                course.add_class(classes[class_id])
                update_label()
                show_succeed_message()

        button = tk.Button(rc, text='Add Class', command=find_class).pack()

    def rebind_profs():

        course.clear_profs()
        update_label()
        def find_prof_by_name():
            print(entry1.get())
            print(profs)
            p = op.find_prof(profs, entry1.get())
            if not p:
                show_error_message('Prof not found!')
            else:
                course.add_prof(p)
                update_label()
                show_succeed_message()

        def find_prof_by_id():
            if str(entry2.get()) not in profs:
                show_error_message('Prof not found!')
            else:
                course.add_prof(profs[str(entry2.get())])
                update_label()
                show_succeed_message()

        rp = tk.Toplevel()
        rp.title('Rebind Profs')
        label1 = tk.Label(rp, text='Name').pack()
        entry1 = tk.Entry(rp)
        entry1.pack()
        button1 = tk.Button(rp, text='Search By Name', command=find_prof_by_name).pack()

        label2 = tk.Label(rp, text='Prof ID').pack()
        entry2 = tk.Entry(rp)
        entry2.pack()
        button2 = tk.Button(rp, text='Search By ID', command=find_prof_by_id).pack()

    tk.Button(c, text="Schedule Manually", command=set_scheduled_manually).pack(side='left')
    tk.Button(c, text="Schedule For Me", command=set_not_scheduled_manually).pack(side='left')
    tk.Button(c, text="Schedule This Course", command=set_should_be_scheduled).pack(side='left')
    tk.Button(c, text="Don't Schedule This Course", command=set_should_not_be_scheduled).pack(side='left')
    tk.Button(c, text="Set Required Period", command=set_required_period).pack(side='left')
    tk.Button(c, text="Rebind Classes", command=rebind_classes).pack(side='left')
    tk.Button(c, text="Rebind Profs", command=rebind_profs).pack(side='left')

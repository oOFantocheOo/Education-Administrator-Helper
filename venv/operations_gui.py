import tkinter as tk

import Constants as c
import SchoolTimetable as st
import operations_class as ocl
import operations_course as oc
import operations_profs as op
import operations_settings as ost


def show_succeed_message():
    temp = tk.Toplevel()
    temp.grab_set()
    tk.Label(temp, text='Succeeded!').pack()
    tk.Button(temp, text='OK', command=temp.destroy, default='active').pack()
    temp.focus_force()
    return temp


def show_waiting_message():
    temp = tk.Toplevel()
    temp.grab_set()
    tk.Label(temp, text='Please wait...').pack()
    return temp


def show_error_message(error):
    temp = tk.Toplevel()
    temp.grab_set()
    temp.title('Error')
    tk.Label(temp, text='\nError: ' + error + '\n').pack()
    tk.Button(temp, text='OK', command=temp.destroy, default='active').pack()
    temp.focus_force()
    temp.geometry('300x100')
    return temp


def show_root_page(profs, courses, class_list, break_time, settings):
    school_timetable = [None]  # wrapped as list for modification
    root = tk.Tk()
    root.focus_force()

    def show_school_timetable_widget(parent):
        st_widget = tk.Toplevel(parent)
        st_widget.geometry('300x200')
        st_widget.focus_force()
        st_widget.grab_set()

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
        e2.insert(tk.END, 100)
        e2.pack()
        default_button = tk.Button(st_widget, text='OK',
                                   command=lambda: create_empty_school_timetable(e2.get(), e1.get()))
        default_button.pack()
        default_button.focus()
        tk.Button(st_widget, text='Cancel', command=st_widget.destroy).pack()

    def check_and_build_school_timetable():
        if not school_timetable[0]:
            show_error_message('School Timetable not initialized yet')
            return
        else:
            school_timetable[0].generate_school_timetable(profs, courses, class_list, break_time, settings)

    root.geometry('600x400')
    root.title("Educational Administration Helper")
    button1 = tk.Button(root, text="Set Timetable", command=lambda: show_school_timetable_widget(root))
    button1.pack()
    label = tk.Label(root, text='School timetable not initialized yet!')
    label.pack()
    button2 = tk.Button(root, text="Prof info", command=lambda: show_prof_page(profs))
    button2.pack()
    button3 = tk.Button(root, text="Course info", command=lambda: show_course_page(courses, profs))
    button3.pack()
    button4 = tk.Button(root, text="Class info", command=lambda: show_class_page(class_list))
    button4.pack()
    button5 = tk.Button(root, text="Set Break Time", command=lambda: show_breaktime_page(break_time))
    button5.pack()
    button6 = tk.Button(root, text="Settings", command=lambda: show_settings_page(settings))
    button6.pack()
    button7 = tk.Button(root, text='Check Conflicts', command=show_checking_page)
    button7.pack()
    button8 = tk.Button(root, text='Generate Timetable', command=check_and_build_school_timetable)
    button8.pack()

    root.mainloop()


def show_checking_page():
    pass


def show_prof_page(profs):
    def find_prof_widget():
        fp = tk.Toplevel()
        fp.grab_set()
        fp.focus_force()
        fp.title("Find A Professor")
        tk.Label(fp, text="Enter the professor's name").pack()
        e = tk.Entry(fp)
        e.pack()
        tk.Button(fp, text='OK', command=lambda: show_prof_info(op.find_prof(profs, e.get()), fp)).pack(side='left')
        tk.Button(fp, text='Cancel', command=fp.destroy).pack()

    def add_prof_widget():
        ap = tk.Toplevel()
        ap.focus_force()
        ap.grab_set()
        ap.title("Add A Professor")
        tk.Label(ap, text="Not implemented").pack()
        tk.Button(ap, text='Cancel', command=ap.destroy).pack()

    def delete_prof_widget():
        dp = tk.Toplevel()
        dp.focus_force()
        dp.grab_set()
        dp.title("Delete A Professor")
        tk.Label(dp, text="Not implemented").pack()
        tk.Button(dp, text='Cancel', command=dp.destroy).pack()

    def clear_all_preference():
        for i in profs.keys():
            profs[i].clear_time_preference()
        show_succeed_message()

    prof_page = tk.Toplevel()
    prof_page.grab_set()
    prof_page.title("Prof Information")

    canvas = tk.Canvas(prof_page)
    scroll = tk.Scrollbar(prof_page, orient='vertical', command=canvas.yview)
    i = 0
    for pid in profs.keys():
        label = tk.Label(canvas, text=profs[pid])
        canvas.create_window(0, i * 30, anchor='nw', window=label, height=30)
        button = tk.Button(canvas, text='Details..', command=lambda a=pid: show_prof_info(profs[a]))
        canvas.create_window(300, i * 30, anchor='nw', window=button, height=30)
        i += 1

    button1 = tk.Button(prof_page, text="Find Prof", command=find_prof_widget)
    button1.pack(s='top')
    button2 = tk.Button(prof_page, text="Add Prof", command=add_prof_widget)
    button2.pack(s='top')
    button3 = tk.Button(prof_page, text="Delete Prof", command=delete_prof_widget)
    button3.pack(s='top')
    button4 = tk.Button(prof_page, text='Clear All Preference', command=clear_all_preference)
    button4.pack(s='top')
    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll.pack(fill='y', side='right')


def show_course_page(courses, profs, values=[]):
    def find_course_by_title_widget():
        fc = tk.Toplevel()
        fc.grab_set()
        fc.focus_force()
        fc.title("Find A Course")
        tk.Label(fc, text="Enter the course's title").pack()
        e = tk.Entry(fc)
        e.insert(tk.END, 'intro to comp sci')
        e.pack()
        tk.Button(fc, text='OK',
                  command=lambda: show_course_info(oc.find_course_by_title(courses, e.get()), profs, fc)).pack(
            side='left')
        tk.Button(fc, text='Cancel', command=fc.destroy).pack()

    def find_course_by_id_widget():
        fc = tk.Toplevel()
        fc.focus_force()
        fc.grab_set()
        fc.title("Find A Course")
        tk.Label(fc, text="Enter the course ID").pack()
        e = tk.Entry(fc)
        e.insert(tk.END, '1')
        e.pack()
        tk.Button(fc, text='OK',
                  command=lambda: show_course_info(oc.find_course_by_course_id(courses, e.get()), profs, fc)).pack(side='left')
        tk.Button(fc, text='Cancel', command=fc.destroy).pack()

    course_page = tk.Toplevel()
    course_page.focus_force()
    course_page.grab_set()
    course_page.title("Course Information")
    v1 = tk.Variable()
    v2 = tk.Variable()
    v3 = tk.Variable()
    v4 = tk.Variable()
    v1.set(1)
    v2.set(1)
    v3.set(1)
    v4.set(1)

    if values:
        v1.set(values[0])
        v2.set(values[1])
        v3.set(values[2])
        v4.set(values[3])

    courses_to_be_shown = []

    row5 = [tk.Label(course_page) for _ in range(7)]
    for i in range(len(row5)):
        row5[i]['text'] = c.COURSE_GENERAL_INFO[i]
        row5[i].grid(row=5, column=i)

    tk.Label(course_page, text='Filters:').grid(row=0, column=0)

    def refresh_with_values():
        new_values = [v1.get(), v2.get(), v3.get(), v4.get()]
        course_page.destroy()
        show_course_page(courses, profs, new_values)

    tk.Button(course_page, text='Refresh', command=refresh_with_values).grid(row=1, column=2)
    tk.Checkbutton(course_page, variable=v1, text='Scheduled manually', command=refresh_with_values).grid(row=1, column=1)
    tk.Checkbutton(course_page, variable=v2, text='Scheduled automatically', command=refresh_with_values).grid(row=2, column=1)
    tk.Checkbutton(course_page, variable=v3, text='Should be scheduled', command=refresh_with_values).grid(row=3, column=1)
    tk.Checkbutton(course_page, variable=v4, text='Should not be scheduled', command=refresh_with_values).grid(row=4, column=1)
    button1 = tk.Button(course_page, text="Find Course by Title", command=find_course_by_title_widget)
    button1.grid(row=1, column=4)
    button2 = tk.Button(course_page, text="Find Course by Course ID", command=find_course_by_id_widget)
    button2.grid(row=2, column=4)

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
        n = len(courses_to_be_shown)
        for i in range(n):
            print(i)
            oc.display_course(course_page, courses_to_be_shown[i], i, profs)

    update_courses_shown()


def show_class_page(classes):
    class_page = tk.Toplevel()
    class_page.title("Class Information")
    class_page.grab_set()
    class_page.focus_force()


def show_breaktime_page(breaktime):
    breaktime.show('Breaktime')


def show_settings_page(settings):
    def save_and_quit():
        settings.language = variable_language.get()
        settings.arranging_rule = variable_rule.get()
        ost.save_settings(settings)
        settings_page.destroy()

    settings_page = tk.Toplevel()
    settings_page.title("Settings")
    settings_page.grab_set()
    settings_page.focus_force()

    variable_language = tk.IntVar()
    variable_rule = tk.IntVar()
    variable_language.set(settings.language)
    variable_rule.set(settings.arranging_rule)

    tk.Label(settings_page, text='Language:').pack(anchor='w')
    tk.Radiobutton(settings_page, text="English", variable=variable_language, value=0).pack(anchor='w')
    tk.Radiobutton(settings_page, text="中文", variable=variable_language, value=1).pack(anchor='w')

    tk.Label(settings_page, text='Arranging Rule:').pack(anchor='w')
    tk.Radiobutton(settings_page, text="Vacancy priority", variable=variable_rule, value=0).pack(anchor='w')
    tk.Radiobutton(settings_page, text="Compactness priority", variable=variable_rule, value=1).pack(anchor='w')

    button_save = tk.Button(settings_page, text='Save & Quit', command=save_and_quit)
    button_save.pack()


def show_prof_info(prof, prev_page=None):
    def update_label():
        column2[0]['text'] = str(prof.prof_id)
        column2[1]['text'] = str(prof.name)
        column2[2]['text'] = str(prof.telephone)
        column2[3]['text'] = str(prof.time_preferred)
        column2[4]['text'] = str(prof.time_not_possible)

    def clear_time_preference():
        prof.clear_time_preference()
        show_succeed_message()
        update_label()

    def change_preferred_time():
        prof.time_preferred.show(prof.name + "'s Preferred Time", prof)
        p.destroy()

    def change_impossible_time():
        prof.time_not_possible.show(prof.name + "'s Impossible Time", prof)
        p.destroy()

    p = tk.Toplevel()
    p.grab_set()
    p.focus_force()
    p.title("Professor Information")
    if not prof:
        tk.Label(p, text='Professor not found').pack()
        tk.Button(p, text='OK', command=p.destroy).pack()
        return

    column1 = [tk.Label(p) for _ in range(5)]
    column2 = [tk.Label(p) for _ in range(5)]

    column1[0]['text'] = 'ID'
    column1[1]['text'] = 'Name'
    column1[2]['text'] = 'Contact'
    column1[3]['text'] = 'Periods preferred'
    column1[4]['text'] = 'Periods not possible'

    update_label()

    for i in range(5):
        column1[i].grid(row=i, column=0)
        column2[i].grid(row=i, column=1)

    if prev_page:
        prev_page.destroy()

    tk.Button(p, text="Clear Time Preference", command=clear_time_preference).grid(s='s')
    tk.Button(p, text="Change Time Preferred", command=change_preferred_time).grid(s='s')
    tk.Button(p, text="Add Time Not Possible", command=change_impossible_time).grid(s='s')


def show_course_info(course, profs, prev_page=None):
    def update_label():
        profs_names = ''
        status = ''
        classes = ''
        if course.should_be_scheduled:
            status += 'Should be scheduled in the school timetable\n'
        else:
            status += 'Should NOT be scheduled in the school timetable\n'

        if course.scheduled_manually:
            status += 'Scheduled manually'
        else:
            status += 'To be scheduled by the program'
        for prof in course.taught_by_profs:
            profs_names += ' ' + profs[prof].name
        for class_id in course.class_list:
            classes += ' ' + class_id

        column2[0]['text'] = str(course.course_id)
        column2[1]['text'] = str(course.title)
        column2[2]['text'] = str(course.course_type)
        column2[3]['text'] = str(course.week_start)
        column2[4]['text'] = str(course.week_end)
        column2[5]['text'] = str(profs_names)
        column2[6]['text'] = str(classes)
        column2[7]['text'] = str(status)

    classes = ocl.load_classes()
    c = tk.Toplevel()
    c.grab_set()
    c.focus_force()
    c.title("Course Information")
    if not course:
        tk.Label(c, text='Course not found').pack()
        tk.Button(c, text='OK', command=c.destroy).pack()
        return

    column1 = [tk.Label(c) for _ in range(8)]
    column2 = [tk.Label(c) for _ in range(8)]

    column1[0]['text'] = 'ID'
    column1[1]['text'] = 'Title'
    column1[2]['text'] = 'Course type'
    column1[3]['text'] = 'Start week'
    column1[4]['text'] = 'End week'
    column1[5]['text'] = 'Taught by'
    column1[6]['text'] = 'Taught to'
    column1[7]['text'] = 'Status'

    for i in range(8):
        column1[i].grid(row=i, column=0)
        column2[i].grid(row=i, column=1)

    update_label()

    if prev_page:
        prev_page.destroy()

    def set_scheduled_manually():
        course.set_scheduled_manually()
        update_label()

    def set_not_scheduled_manually():
        course.set_not_scheduled_manually()
        update_label()

    def set_should_be_scheduled():
        course.set_should_be_scheduled()
        update_label()

    def set_should_not_be_scheduled():
        course.set_should_not_be_scheduled()
        update_label()

    def set_required_period():
        if not course.should_be_scheduled:
            show_error_message('This course should not be scheduled')
            return

        if not course.scheduled_manually:
            show_error_message("It will be scheduled automatically, \ntherefore can't set periods required.\nChange it by pressing 'Schedule Manually'")
            return
        course.period_required.show('Course Required Period', course)
        update_label()

    def rebind_classes():
        course.clear_classes()
        update_label()
        rc = tk.Toplevel()
        rc.title('Rebind Classes')
        rc.grab_set()
        rc.focus_force()
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

        button1 = tk.Button(rc, text='Add Class', command=find_class).pack()
        button2 = tk.Button(rc, text='Finish', command=rc.destroy).pack()

    def rebind_profs():

        course.clear_profs()
        update_label()

        def find_prof_by_name():
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
        rp.grab_set()
        rp.focus_force()
        label1 = tk.Label(rp, text='Name').pack()
        entry1 = tk.Entry(rp)
        entry1.pack()
        button1 = tk.Button(rp, text='Add By Name', command=find_prof_by_name).pack()

        label2 = tk.Label(rp, text='Prof ID').pack()
        entry2 = tk.Entry(rp)
        entry2.pack()
        button2 = tk.Button(rp, text='Add By ID', command=find_prof_by_id).pack()

        button3 = tk.Button(rp, text='Finish', command=rp.destroy).pack()

    tk.Button(c, text="Schedule Manually", command=set_scheduled_manually).grid(s='s')
    tk.Button(c, text="Schedule For Me", command=set_not_scheduled_manually).grid(s='s')
    tk.Button(c, text="Schedule This Course", command=set_should_be_scheduled).grid(s='s')
    tk.Button(c, text="Don't Schedule This Course", command=set_should_not_be_scheduled).grid(s='s')
    tk.Button(c, text="Set Required Period", command=set_required_period).grid(s='s')
    tk.Button(c, text="Rebind Classes", command=rebind_classes).grid(s='s')
    tk.Button(c, text="Rebind Profs", command=rebind_profs).grid(s='s')

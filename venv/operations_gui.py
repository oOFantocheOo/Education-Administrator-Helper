import tkinter as tk
from tkinter import ttk

import Constants as c
import SchoolTimetable as st
import languages as l
import operations_course as oc
import operations_profs as op
import operations_settings as ost


def show_succeed_message(language=0):
    temp = tk.Toplevel()
    temp.grab_set()
    tk.Label(temp, text=l.succeeded[language]).pack()
    b = tk.Button(temp, text='OK', command=temp.destroy, default='active')
    b.pack()
    temp.focus_force()
    b.focus_force()
    return temp


def show_waiting_message():
    temp = tk.Toplevel()
    temp.grab_set()
    tk.Label(temp, text='Please wait...').pack()
    return temp


def show_error_message(error, language=0):
    temp = tk.Toplevel()
    temp.grab_set()
    temp.title('Error')
    tk.Label(temp, text=l.error[language] + error + '\n').pack()
    b = tk.Button(temp, text='OK', command=temp.destroy, default='active')
    b.pack()
    temp.focus_force()
    b.focus_force()
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

        def create_empty_school_timetable(title):
            school_timetable[0] = st.SchoolTimetable(title)
            label['text'] = l.st_initialized[settings.language]
            st_widget.destroy()

        st_widget.title('Create School Timetable')
        tk.Label(st_widget, text='Title of school timetable:').pack()
        e1 = tk.Entry(st_widget)
        e1.insert(tk.END, 'qwe')
        e1.pack()
        default_button = tk.Button(st_widget, text='OK', command=lambda: create_empty_school_timetable(e1.get()))
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
    root.title(l.EAH[settings.language])
    button1 = tk.Button(root, text=l.set_timetable[settings.language], command=lambda: show_school_timetable_widget(root))
    button1.pack()
    button1.focus_force()
    label = tk.Label(root, text=l.st_not_initialized[settings.language])
    label.pack()
    button2 = tk.Button(root, text=l.prof_info[settings.language], command=lambda: show_prof_page(profs, settings))
    button2.pack()
    button3 = tk.Button(root, text=l.course_info[settings.language], command=lambda: show_course_page(courses, profs, class_list, settings))
    button3.pack()
    button4 = tk.Button(root, text=l.class_info[settings.language], command=lambda: show_class_page(class_list))
    button4.pack()
    button5 = tk.Button(root, text=l.set_break_time[settings.language], command=lambda: show_breaktime_page(break_time, settings))
    button5.pack()
    button6 = tk.Button(root, text=l.settings[settings.language])
    button6.pack()
    button7 = tk.Button(root, text=l.check_conflicts[settings.language], command=show_checking_page)
    button7.pack()
    button8 = tk.Button(root, text=l.generate_timetable[settings.language], command=check_and_build_school_timetable)
    button8.pack()
    button9 = tk.Button(root, text=l.check_schedule[settings.language], command=lambda: show_schedules_page(profs, courses, class_list, school_timetable[0], settings.language))
    button9.pack()
    buttons_and_label = [button1, button2, button3, button4, button5, button6, button7, button8, button9, label]
    button6['command'] = lambda: show_settings_page(settings, buttons_and_label)
    root.mainloop()


def show_checking_page():
    pass


def show_prof_page(profs, settings):
    def find_prof_widget():
        fp = tk.Toplevel()
        fp.grab_set()
        fp.focus_force()
        fp.title(l.find_a_prof[settings.language])
        tk.Label(fp, text=l.enter_name[settings.language]).pack()
        e = tk.Entry(fp)
        e.pack()
        tk.Button(fp, text='OK', command=lambda: show_prof_info(op.find_prof(profs, e.get()), fp, language=settings.language)).pack(side='left')
        tk.Button(fp, text=l.cancel[settings.language], command=fp.destroy).pack()

    def clear_all_preference():
        for i in profs.keys():
            profs[i].clear_time_preference()
        show_succeed_message()

    prof_page = tk.Toplevel()
    prof_page.grab_set()
    prof_page.title()

    canvas = tk.Canvas(prof_page)
    scroll = tk.Scrollbar(prof_page, orient='vertical', command=canvas.yview)
    i = 0
    for pid in profs.keys():
        label = tk.Label(canvas, text=profs[pid])
        canvas.create_window(0, i * 30, anchor='nw', window=label, height=30)
        button = tk.Button(canvas, text=l.details[settings.language], command=lambda a=pid: show_prof_info(profs[a], language=settings.language))
        canvas.create_window(300, i * 30, anchor='nw', window=button, height=30)
        i += 1

    button1 = tk.Button(prof_page, text=l.find_a_prof[settings.language], command=find_prof_widget)
    button1.pack(s='top')
    button4 = tk.Button(prof_page, text=l.clear_all_preference[settings.language], command=clear_all_preference)
    button4.pack(s='top')
    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll.pack(fill='y', side='right')


def show_course_page(courses, profs, class_list, settings, values=[]):
    def find_course_by_title_widget():
        fc = tk.Toplevel()
        fc.grab_set()
        fc.focus_force()
        fc.title(l.find_course[settings.language])
        tk.Label(fc, text=l.enter_title[settings.language]).pack()
        e = tk.Entry(fc)
        e.insert(tk.END, 'intro to comp sci')  # Set default value
        e.pack()
        tk.Button(fc, text='OK', command=lambda: show_course_info(oc.find_course_by_title(courses, e.get()), profs, class_list, fc, language=settings.language)).pack(side='left')
        tk.Button(fc, text=l.cancel[settings.language], command=fc.destroy).pack()

    def find_course_by_id_widget():
        fc = tk.Toplevel()
        fc.focus_force()
        fc.grab_set()
        fc.title(l.find_course[settings.language])
        tk.Label(fc, text=l.enter_id[settings.language]).pack()
        e = tk.Entry(fc)
        e.insert(tk.END, '1')
        e.pack()
        tk.Button(fc, text='OK',
                  command=lambda: show_course_info(oc.find_course_by_course_id(courses, e.get()), profs, class_list, fc, language=settings.language)).pack(side='left')
        tk.Button(fc, text=l.cancel[settings.language], command=fc.destroy).pack()

    course_page = tk.Toplevel()
    course_page.focus_force()
    course_page.grab_set()
    course_page.title(l.course_info[settings.language])
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

    row5 = [tk.Label(course_page) for _ in range(4)]
    for i in range(len(row5)):
        row5[i]['text'] = c.COURSE_GENERAL_INFO[settings.language][i]
        row5[i].grid(row=5, column=i)

    tk.Label(course_page, text=l.filters[settings.language]).grid(row=0, column=0)

    def refresh_with_values():
        new_values = [v1.get(), v2.get(), v3.get(), v4.get()]
        course_page.destroy()
        show_course_page(courses, profs, class_list, settings, new_values)

    tk.Button(course_page, text=l.refresh[settings.language], command=refresh_with_values).grid(row=1, column=2)
    tk.Checkbutton(course_page, variable=v1, text=l.sche_man[settings.language], command=refresh_with_values).grid(row=1, column=1)
    tk.Checkbutton(course_page, variable=v2, text=l.sche_auto[settings.language], command=refresh_with_values).grid(row=2, column=1)
    tk.Checkbutton(course_page, variable=v3, text=l.should_sche[settings.language], command=refresh_with_values).grid(row=3, column=1)
    tk.Checkbutton(course_page, variable=v4, text=l.should_not_sche[settings.language], command=refresh_with_values).grid(row=4, column=1)
    button1 = tk.Button(course_page, text=l.find_course_by_title[settings.language], command=find_course_by_title_widget)
    button1.grid(row=1, column=4)
    button2 = tk.Button(course_page, text=l.find_course_by_id[settings.language], command=find_course_by_id_widget)
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
            oc.display_course(course_page, courses_to_be_shown[i], i, profs, class_list, settings)

    update_courses_shown()


def show_class_page(classes):
    class_page = tk.Toplevel()
    class_page.title("0")
    class_page.grab_set()
    class_page.focus_force()
    for i in classes.keys():
        tk.Label(class_page, text=classes[i].classId).pack()


def show_breaktime_page(breaktime, settings):
    breaktime.show(l.breaktime[settings.language], language=settings.language)


def show_settings_page(settings, buttons):
    def save_and_quit():
        settings.language = variable_language.get()
        settings.arranging_rule = variable_rule.get()
        ost.save_settings(settings)
        settings_page.destroy()
        buttons[0]['text'] = l.set_timetable[settings.language]
        buttons[1]['text'] = l.prof_info[settings.language]
        buttons[2]['text'] = l.course_info[settings.language]
        buttons[3]['text'] = l.class_info[settings.language]
        buttons[4]['text'] = l.set_break_time[settings.language]
        buttons[5]['text'] = l.settings[settings.language]
        buttons[6]['text'] = l.check_conflicts[settings.language]
        buttons[7]['text'] = l.generate_timetable[settings.language]
        buttons[8]['text'] = l.check_schedule[settings.language]
        buttons[9]['text'] = l.st_not_initialized[settings.language]

    settings_page = tk.Toplevel()
    settings_page.title("Settings")
    settings_page.grab_set()
    settings_page.focus_force()

    variable_language = tk.IntVar()
    variable_rule = tk.IntVar()
    variable_language.set(settings.language)
    variable_rule.set(settings.arranging_rule)

    tk.Label(settings_page, text='Language（语言）:').pack(anchor='w')
    tk.Radiobutton(settings_page, text="English", variable=variable_language, value=0).pack(anchor='w')
    tk.Radiobutton(settings_page, text="中文", variable=variable_language, value=1).pack(anchor='w')

    tk.Label(settings_page, text='Arranging Rule（排课规则）:').pack(anchor='w')
    tk.Radiobutton(settings_page, text="Vacancy priority", variable=variable_rule, value=0).pack(anchor='w')
    tk.Radiobutton(settings_page, text="Compactness priority（紧凑型）", variable=variable_rule, value=1).pack(anchor='w')

    button_save = tk.Button(settings_page, text='Save & Quit（保存并退出）', command=save_and_quit)
    button_save.pack()


def show_prof_info(prof, prev_page=None, language=0):
    def update_label():
        column2[0]['text'] = str(prof.prof_id)
        column2[1]['text'] = str(prof.name)
        column2[2]['text'] = str(prof.telephone)
        column2[3]['text'] = prof.time_preferred.__str__(language)
        column2[4]['text'] = prof.time_not_possible.__str__(language)

    def clear_time_preference():
        prof.clear_time_preference()
        show_succeed_message()
        update_label()

    def change_preferred_time():
        show_error_message('Not implemented yet')
        # prof.time_preferred.show(prof.name + "'s Preferred Time", prof)
        # p.destroy()

    def change_impossible_time():
        prof.time_not_possible.show(prof.name + l.impossible_time[language], prof, language=language)
        p.destroy()

    p = tk.Toplevel()
    p.grab_set()
    p.focus_force()
    p.title(l.prof_info[language])
    if not prof:
        tk.Label(p, text=l.prof_not_found[language]).pack()
        tk.Button(p, text='OK', command=p.destroy).pack()
        return

    column1 = [tk.Label(p) for _ in range(5)]
    column2 = [tk.Label(p) for _ in range(5)]

    column1[0]['text'] = l.ID[language]
    column1[1]['text'] = l.name[language]
    column1[2]['text'] = l.contact[language]
    column1[3]['text'] = l.periods_preferred[language]
    column1[4]['text'] = l.periods_impossible[language]

    update_label()

    for i in range(5):
        column1[i].grid(row=i, column=0)
        column2[i].grid(row=i, column=1)

    if prev_page:
        prev_page.destroy()

    tk.Button(p, text=l.clear_time_preference[language], command=clear_time_preference).grid(s='s')
    # tk.Button(p, text="Change Time Preferred", command=change_preferred_time).grid(s='s')
    tk.Button(p, text=l.change_time_impossible[language], command=change_impossible_time).grid(s='s')


def show_course_info(course, profs, class_list, prev_page=None, language=0):
    def update_label():
        def groups_str(groups):
            s = ''
            for g in groups:
                for cid in g[0]:
                    s += cid + ' '
                s += ','
                for pid in g[1]:
                    s += profs[pid].name + ' '
                s += '\n'
            return s

        profs_names = ''
        status = ''
        classes = ''
        if course.should_be_scheduled:
            status += l.should_sche[language] + '\n'
        else:
            status += l.should_not_sche[language] + '\n'

        if course.scheduled_manually:
            status += l.sche_man[language]
        else:
            status += l.sche_auto[language]
        for prof in course.taught_by_profs:
            profs_names += ' ' + profs[prof].name
        for class_id in course.class_list:
            classes += ' ' + class_id

        week_str = ''
        for i in range(len(course.weeks)):
            if course.weeks[i] == 1 or course.weeks[i] == '1':
                week_str += str(i + 1) + ' '

        if not week_str:
            week_str = 'N/A'

        column2[0]['text'] = str(course.course_id)
        column2[1]['text'] = str(course.title)
        column2[2]['text'] = str(course.course_type)
        column2[3]['text'] = week_str
        column2[4]['text'] = str(status)
        column2[5]['text'] = groups_str(course.groups)

    c = tk.Toplevel()
    c.grab_set()
    c.focus_force()
    c.title(l.course_info[language])
    if not course:
        tk.Label(c, text=l.course_not_found[language]).pack()
        tk.Button(c, text='OK', command=c.destroy).pack()
        return

    column1 = [tk.Label(c) for _ in range(6)]
    column2 = [tk.Label(c) for _ in range(6)]

    column1[0]['text'] = l.id_course[language]
    column1[1]['text'] = l.title[language]
    column1[2]['text'] = l.course_type[language]
    column1[3]['text'] = l.weeks[language]
    column1[4]['text'] = l.status[language]
    column1[5]['text'] = l.group[language]

    for i in range(6):
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

    def set_weeks():
        def save_checkbuttons():
            for i in range(30):
                course.weeks[i] = str(var_array[i].get())
            sw.destroy()
            update_label()

        var_array = []
        sw = tk.Toplevel()
        sw.grab_set()
        sw.focus_force()
        for r in range(6):
            for c in range(5):
                n = 5 * r + c
                v = tk.Variable()
                v.set(course.weeks[n])
                b = tk.Checkbutton(sw, variable=v, text='Week ' + str(n + 1))
                b.grid(row=r, column=c)
                var_array.append(v)

        tk.Button(sw, text=l.save_and_quit[language], command=save_checkbuttons).grid(s='s')

    tk.Button(c, text=l.sche_man[language], command=set_scheduled_manually).grid(s='s')
    tk.Button(c, text=l.sche_auto[language], command=set_not_scheduled_manually).grid(s='s')
    tk.Button(c, text=l.should_sche[language], command=set_should_be_scheduled).grid(s='s')
    tk.Button(c, text=l.should_not_sche[language], command=set_should_not_be_scheduled).grid(s='s')
    tk.Button(c, text=l.set_required_period[language], command=set_required_period).grid(s='s')
    tk.Button(c, text=l.set_weeks[language], command=set_weeks).grid(s='s')
    tk.Button(c, text=l.manage_grouping[language], command=lambda: show_grouping_page(course, profs, class_list, c, language)).grid(s='s')


def show_grouping_page(course, profs, class_list, parent_course_info, language=0):
    gp = tk.Toplevel()
    gp.focus_force()
    gp.grab_set()

    def refresh():
        gp.destroy()
        show_grouping_page(course, profs, class_list, parent_course_info, language)

    def update_labels():
        for i in range(len(course.groups)):
            s = ''
            for class_id in course.groups[i][0]:
                s += class_id + ' '
            labels[i][0]['text'] = s
            labels[i][1]['text'] = op.list_prof_ids_to_names(profs, course.groups[i][1])

    def save_and_quit():

        for i in course.groups:
            for j in i:
                if not j:
                    show_error_message(l.group_empty[language])
                    return
        gp.destroy()
        parent_course_info.destroy()
        show_course_info(course, profs, class_list, language=language)

    def rebind_classes(group):
        group[0] = []
        update_labels()
        rc = tk.Toplevel()
        rc.title(l.rebind_classes[language])
        rc.grab_set()
        rc.focus_force()
        label1 = tk.Label(rc, text=l.major[language]).pack()
        entry1 = tk.Entry(rc)
        entry1.pack()

        label2 = tk.Label(rc, text=l.grade[language]).pack()
        entry2 = tk.Entry(rc)
        entry2.pack()

        label3 = tk.Label(rc, text=l.index[language]).pack()
        entry3 = tk.Entry(rc)
        entry3.pack()

        def find_class():
            class_id = str(entry1.get()) + str(entry2.get()) + str(entry3.get())
            if class_id not in class_list:
                show_error_message(l.class_not_found[language])
            else:
                course.add_class_to_group(group, class_list[class_id])
                update_labels()

        button1 = tk.Button(rc, text=l.add_class[language], command=find_class).pack()
        button2 = tk.Button(rc, text=l.finish[language], command=rc.destroy).pack()

    def rebind_profs(group):
        group[1] = []
        update_labels()

        def find_prof_by_name():
            p = op.find_prof(profs, entry1.get())
            if not p:
                show_error_message(l.prof_not_found[language])
            else:
                course.add_prof_to_group(group, p)
                update_labels()

        def find_prof_by_id():
            if str(entry2.get()) not in profs:
                show_error_message(l.prof_not_found[language])
            else:
                course.add_prof_to_group(group, profs[str(entry2.get())])
                update_labels()
                show_succeed_message()

        rp = tk.Toplevel()
        rp.title('Rebind Profs')
        rp.grab_set()
        rp.focus_force()
        label1 = tk.Label(rp, text=l.name[language]).pack()
        entry1 = tk.Entry(rp)
        entry1.pack()
        button1 = tk.Button(rp, text=l.add_by_name[language], command=find_prof_by_name).pack()
        label2 = tk.Label(rp, text=l.ID[language]).pack()
        entry2 = tk.Entry(rp)
        entry2.pack()
        button2 = tk.Button(rp, text=l.add_by_id[language], command=find_prof_by_id).pack()
        button3 = tk.Button(rp, text=l.finish[language], command=rp.destroy).pack()

    def add_group():
        course.add_group()
        refresh()

    def remove_group(group):
        course.remove_group(group)
        refresh()

    tk.Label(gp, text=l.prof[language]).grid(row=0, column=1)
    tk.Label(gp, text=l.classes[language]).grid(row=0, column=0)
    labels = []
    for i in range(len(course.groups)):
        labels.append([])
        labels[-1].append(tk.Label(gp, text=course.groups[i][0]))
        labels[-1][0].grid(row=i + 1, column=0)
        labels[-1].append(tk.Label(gp, text=op.list_prof_ids_to_names(profs, course.groups[i][1])))
        labels[-1][1].grid(row=i + 1, column=1)
        tk.Button(gp, text=l.rebind_classes[language], command=lambda g=course.groups[i]: rebind_classes(g)).grid(row=i + 1, column=2)
        tk.Button(gp, text=l.rebind_profs[language], command=lambda g=course.groups[i]: rebind_profs(g)).grid(row=i + 1, column=3)
        tk.Button(gp, text=l.delete[language], command=lambda g=course.groups[i]: remove_group(g)).grid(row=i + 1, column=4)

    tk.Button(gp, text=l.add_group[language], command=add_group).grid(s='s')
    tk.Button(gp, text=l.save_and_quit[language], command=save_and_quit).grid(s='s')


def show_schedules_page(profs, courses, class_list, school_timetable, language=0):
    if not school_timetable:
        show_error_message(l.st_not_initialized[language])
        return
    if not school_timetable.is_generated:
        show_error_message(l.st_not_generated[language])
        return
    sp = tk.Toplevel()
    sp.grab_set()
    sp.focus_force()
    tk.Button(sp, text=l.prof_sche[language], command=lambda: show_prof_schedule_widget(profs, courses, language)).pack()
    tk.Button(sp, text=l.class_sche[language]).pack()
    tk.Button(sp, text=l.school_sche[language], command=lambda: show_error_message('Not implemented')).pack()


def show_prof_schedule_widget(profs, courses, language=0):
    def find_prof():
        p = op.find_prof(profs, e.get())
        if not p:
            show_error_message(l.prof_not_found[language])
            return
        else:
            psp.destroy()
            show_prof_schedule(profs, p, courses, language)

    psp = tk.Toplevel()
    psp.grab_set()
    psp.focus_force()
    tk.Label(psp, text=l.enter_name[language]).grid(row=0, column=0)
    e = tk.Entry(psp)
    e.grid(row=1, column=0)
    tk.Button(psp, text=l.search[language], command=find_prof).grid(row=2, column=0)


def show_prof_schedule(profs, p, courses, language=0):
    def update_info(prof, week, labels=[]):
        if not prof:
            show_error_message(l.prof_not_found[language])
            return
        elif week < 0 or week > 29:
            show_error_message(l.week_not_existed[language])
        else:
            forget_labels(labels)
            week_entry = tk.Entry(psp)
            week_entry.grid(row=0, column=6)
            label = tk.Label(psp, text=prof.name + l.of_week_part1[language] + str(week + 1) + l.of_week_part2[language])
            label.grid(row=3, column=3)
            labels = schedule_to_gui(courses, prof.schedule[week], psp, 4, 0, language)
            labels.append(label)
            tk.Button(psp, text=l.jump_to_week[language], command=lambda: update_info(prof, int(week_entry.get()) - 1, labels)).grid(row=0, column=7)
            tk.Button(psp, text=l.prev_week[language], command=lambda: update_info(prof, week - 1, labels)).grid(row=1, column=6)
            tk.Button(psp, text=l.next_week[language], command=lambda: update_info(prof, week + 1, labels)).grid(row=2, column=6)

    def find_prof():
        p = op.find_prof(profs, e.get())
        if not p:
            show_error_message(l.prof_not_found[language])
            return
        else:
            psp.destroy()
            show_prof_schedule(profs, p, courses)

    psp = tk.Toplevel()
    psp.grab_set()
    psp.focus_force()
    tk.Label(psp, text=l.enter_name[language]).grid(row=0, column=0)
    e = tk.Entry(psp)
    e.grid(row=1, column=0)
    tk.Button(psp, text=l.search[language], command=find_prof).grid(row=2, column=0)
    update_info(p, 0, [])


def schedule_to_gui(courses, timetable, page, row_start, col_start, language=0):
    for i in range(row_start, row_start + 12):
        tk.Label(page, text=l.period_part1 + str(i - row_start + 1) + l.period_part2).grid(row=i + 1, column=col_start)
    for i in range(col_start, col_start + 7):
        tk.Label(page, text=c.WEEK[language][i - col_start]).grid(row=row_start, column=i + 1)
    ttk.Separator(page, orient='horizontal').grid(column=0, row=row_start + 4, columnspan=7, sticky='ns')
    labels = []
    for i in range(12):
        for j in range(7):
            cur = timetable.timetable[i][j]
            if cur != '0':
                if isinstance(cur, str):
                    label = tk.Label(page, text=cur)
                    label.grid(row=row_start + i + 1, column=col_start + j + 1)
                else:  # It's of form of [course_id,[classId]]
                    s = ''
                    s += courses[cur[0]].title
                    s += ', '
                    for cid in cur[1]:
                        s += cid + ' '
                    label = tk.Label(page, text=s)
                    label.grid(row=row_start + i + 1, column=col_start + j + 1)
                labels.append(label)
    return labels


def forget_labels(labels):
    for l in labels:
        l.grid_forget()
    labels = []

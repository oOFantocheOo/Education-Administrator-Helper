import Group
import Timetable as tt
import operations_class as oc
import operations_gui as og
import operations_profs as op
import languages as l


class SchoolTimetable:
    class DepartmentTimetable:
        def __init__(self, major, week_num=30):
            self.major = major
            self.weekly_schedule = [tt.Timetable() for _ in range(week_num)]

    def __init__(self, title='', major=''):
        self.title = title
        self.major = major
        self.week_num = 30
        self.is_generated = False
        self.departments = {}
        '''
        workbook = xl.load_workbook('../Input/requirement.xlsx')
        worksheet = workbook[workbook.sheetnames[0]]
        messages = []
        class_list_title_cell = ''
        course_name_title_cell = ''
        major_title_cell = ''
        start_week_title_cell = ''
        end_week_title_cell = ''
        prof_list_title_cells = []
        class_is_set = False
        course_name_is_set = False
        major_is_set = False
        start_week_is_set = False
        end_week_is_set = False
        max_row=worksheet.max_row
        max_col=worksheet.max_column
        for i in range(65,max_col+65):
            cur = str(worksheet[chr(i) + '1'].value)

            if 'class' in cur or '班级' in cur:
                if class_is_set:
                    og.show_error_message('Class column already set to ' + class_list_title_cell + '.\n Not ' + chr(i) + '1')
                    return
                class_list_title_cell = chr(i) + '1'
                class_is_set = True
            elif 'course' in cur or '课程' in cur:
                if course_name_is_set:
                    og.show_error_message('Course name already set to ' + course_name_title_cell + '.\n Not ' + chr(i) + '1')
                    return
                course_name_title_cell = chr(i) + '1'
                course_name_is_set = True
            elif 'major' in cur or '专业' in cur:
                if major_is_set:
                    og.show_error_message('Major already set to ' + major_title_cell + '.\n Not ' + chr(i) + '1')
                    return
                major_title_cell = chr(i) + '1'
                major_is_set = True
            elif 'start' in cur or '开始' in cur:
                if start_week_is_set:
                    og.show_error_message('Start week already set to ' + start_week_title_cell + '.\n Please remove the previous column')
                    return
                start_week_title_cell = chr(i) + '1'
                start_week_is_set = True
            elif 'end' in cur or '结束' in cur:
                if end_week_is_set:
                    print(1)
                    og.show_error_message('End week already set to ' + end_week_title_cell + '.\n Please remove the previous column')
                    return
                end_week_title_cell = chr(i) + '1'
                end_week_is_set = True
            elif 'prof' in cur or '师' in cur:
                prof_list_title_cells.append(chr(i) + '1')
            else:
                messages.append(chr(i) + '1 is ignored')
        print(messages)
        '''

    def apply(self, profs, courses, class_list, group: Group.Group):
        cid_list = group.class_id_list

    def __str__(self):
        return "Not implemented"

    def generate_school_timetable(self, profs, courses, class_list, break_time, settings):

        def arrange_regular():
            pass

        # Step 1: initialization & checking
        wait = og.show_waiting_message()
        conflicts = []
        for pid in profs.keys():
            profs[pid].schedule = []  # Clear all schedule
            for i in range(self.week_num):
                profs[pid].schedule.append(tt.Timetable(title=profs[pid].name + l.timetable_of_week[settings.language] + str(i)))
                # in Prof.schedule, for Timetable[i][j],
                # 0: not occupied;
                # not possible: the prof required not to teach in this period(set in Prof info page;
                # break time: the period is in break time, thus not allocated with any courses;
                # [course_id, [classId]]: teach Course with course_id to Class(es) with classId(s)in this period

        for cid in class_list.keys():
            class_list[cid].schedule = []  # Clear all schedule
            for i in range(self.week_num):
                class_list[cid].schedule.append(tt.Timetable(title=class_list[cid].classId + l.timetable_of_week[settings.language] + str(i)))
                # in Class.schedule, for Timetable[i][j],
                # 0: not occupied;
                # break time: the period is in break time, thus not allocated with any courses;
                # [course_id, [prof_id]]: be taught Course with course_id by Prof(s) with prof_id(s) in this period

        # Step 2: negate all break time in schedule, so that it can't be used
        for pid in profs.keys():  # set break time in profs' info
            cur = profs[pid].schedule
            for w in range(self.week_num):
                err = cur[w].update_based_on(break_time, ['0'], ['0', '1'], '1', 'break time')
                if err: print(err)

        for cid in class_list.keys():  # set break time in classes' info
            cur = class_list[cid].schedule
            for w in range(self.week_num):
                err = cur[w].update_based_on(break_time, ['0'], ['0', '1'], '1', 'break time')
                if err: print(err)

        # Step 3: negate all time not possible in profs' schedule
        for pid in profs.keys():
            tnp = profs[pid].time_not_possible
            for w in range(self.week_num):
                err = profs[pid].schedule[w].update_based_on(tnp, ['0', 'break time'], ['0', '1'], '1', 'time not possible')
                if err: print(err)

        # Step 4: take all Courses that should be scheduled
        courses_to_be_allocated = {}
        courses_manually = []
        for cid in courses.keys():
            if courses[cid].should_be_scheduled and not courses[cid].scheduled_manually:
                courses_to_be_allocated[cid] = courses[cid]
        for cid in courses.keys():
            if courses[cid].should_be_scheduled and courses[cid].scheduled_manually:
                courses_manually.append(courses[cid])

        # Step 5: check Courses
        for c in courses_manually:
            if not c.groups:
                err.append(c.title + " hasn't been assigned with any classes or profs")
            if c.period_required.all_zeros():
                err.append(c.title + ' is set to manually distributed, but no periods are given')
            if not ('1' in c.weeks):
                err.append(c.title + ': no weeks are set')
        for cid in courses_to_be_allocated.keys():
            c = courses_to_be_allocated[cid]
            if not c.groups:
                err.append(c.title + " hasn't been assigned with any classes or profs")
            if not ('1' in c.weeks):
                err.append(c.title + ': no weeks are set')
        if err: print(err)

        # Step 6: pre-distribute courses that are set manually
        for c in courses_manually:
            print('allocating ', c.title)
            for w in range(30):
                if c.weeks[w] == 0 or c.weeks[w] == '0':
                    continue
                for g in c.groups:
                    for cl in g[0]:
                        err = class_list[cl].schedule[w].check(c.period_required, '0', '1')
                        class_list[cl].schedule[w].change(c.period_required, [c.course_id, [i for i in g[1]]], '1')
                        if err:
                            print(err)

                    for p in g[1]:
                        err = profs[p].schedule[w].check(c.period_required, '0', '1')
                        profs[p].schedule[w].change(c.period_required, [c.course_id, [i for i in g[0]]], '1')
                        if err:
                            print(err)

        # Step 7: allocate courses

        # Courses to groups
        groups = []
        for cid in courses_to_be_allocated.keys():
            c = courses_to_be_allocated[cid]
            for g in c.groups:
                cur_group = Group.Group(c.course_id, g[1], g[0])
                groups.append(cur_group)

        # i)Select courses that have profs with time preference (first group of Courses)

        # to be implemented

        # ii)Select courses that have profs with time not possible (second group of Courses)
        second = []
        for i in range(len(groups))[::-1]:
            cur_prof_id_list = groups[i].prof_id_list
            for cur_prof_id in cur_prof_id_list:
                if profs[cur_prof_id].get_time_impossible_as_list():
                    second.append(groups[i])
                    groups.pop(i)

        err = []
        if settings.arranging_rule == 0:  # if set to priority to periods that are most empty
            print('Allocating courses with priority to periods that are most empty in a week')
        elif settings.arranging_rule == 1:  # if set to closely pack
            print('Allocating courses: closely pack everything')
            for i in range(len(second)):
                cur_prof_id_list = second[i].prof_id_list
                cur_class_id_list = second[i].class_id_list
                weeks = courses[second[i].course_id].weeks
                first_period_is_chosen, second_period_is_chosen = False, False

                for date in range(7):
                    for period in range(12):
                        if not op.profs_are_available(profs, cur_prof_id_list, weeks, period, date):
                            continue
                        elif not oc.classes_are_available(class_list, cur_class_id_list, weeks, period, date):
                            continue
                        else:
                            first_period_is_chosen = True
                            first_period = (period, date)
                            for d in range(date + 2, 7):
                                for p in range(12):
                                    if not op.profs_are_available(profs, cur_prof_id_list, weeks, p, d):
                                        continue
                                    elif not oc.classes_are_available(class_list, cur_class_id_list, weeks, p, d):
                                        continue
                                    else:
                                        second_period_is_chosen = True
                                        second_period = (p, d)
                                        break
                                if second_period_is_chosen:
                                    break

                        if first_period_is_chosen and second_period_is_chosen:
                            break
                    if first_period_is_chosen and second_period_is_chosen:
                        break

                if not (first_period_is_chosen and second_period_is_chosen):
                    err.append(courses[second[i].course_id].title + 'cannot be arranged')
                else:
                    for pid in cur_prof_id_list:
                        op.change(profs, pid, weeks, first_period[0], first_period[1], [second[i].course_id, cur_class_id_list])
                        op.change(profs, pid, weeks, first_period[0] + 1, first_period[1], [second[i].course_id, cur_class_id_list])
                        op.change(profs, pid, weeks, second_period[0], second_period[1], [second[i].course_id, cur_class_id_list])
                        op.change(profs, pid, weeks, second_period[0] + 1, second_period[1], [second[i].course_id, cur_class_id_list])

                    for cid in cur_class_id_list:
                        oc.change(class_list, cid, weeks, first_period[0], first_period[1], [second[i].course_id, cur_prof_id_list])
                        oc.change(class_list, cid, weeks, first_period[0] + 1, first_period[1], [second[i].course_id, cur_prof_id_list])
                        oc.change(class_list, cid, weeks, second_period[0], second_period[1], [second[i].course_id, cur_prof_id_list])
                        oc.change(class_list, cid, weeks, second_period[0] + 1, second_period[1], [second[i].course_id, cur_prof_id_list])

        # iii)Allocate the remaining courses according to rules
        err = []
        if settings.arranging_rule == 0:  # if set to priority to periods that are most empty
            print('Allocating courses with priority to periods that are most empty in a week')
        elif settings.arranging_rule == 1:  # if set to closely pack
            print('Allocating courses: closely pack everything')
            for i in range(len(groups)):
                cur_prof_id_list = groups[i].prof_id_list
                cur_class_id_list = groups[i].class_id_list
                weeks = courses[groups[i].course_id].weeks
                first_period_is_chosen, second_period_is_chosen = False, False

                for date in range(7):
                    for period in range(12):
                        if not op.profs_are_available(profs, cur_prof_id_list, weeks, period, date):
                            continue
                        elif not oc.classes_are_available(class_list, cur_class_id_list, weeks, period, date):
                            continue
                        else:
                            first_period_is_chosen = True
                            first_period = (period, date)
                            for d in range(date + 2, 7):
                                for p in range(12):
                                    if not op.profs_are_available(profs, cur_prof_id_list, weeks, p, d):
                                        continue
                                    elif not oc.classes_are_available(class_list, cur_class_id_list, weeks, p, d):
                                        continue
                                    else:
                                        second_period_is_chosen = True
                                        second_period = (p, d)
                                        break
                                if second_period_is_chosen:
                                    break

                        if first_period_is_chosen and second_period_is_chosen:
                            break
                    if first_period_is_chosen and second_period_is_chosen:
                        break

                if not (first_period_is_chosen and second_period_is_chosen):
                    err.append(courses[groups[i].course_id].title + 'cannot be arranged')
                else:
                    for pid in cur_prof_id_list:
                        op.change(profs, pid, weeks, first_period[0], first_period[1], [groups[i].course_id, cur_class_id_list])
                        op.change(profs, pid, weeks, first_period[0] + 1, first_period[1], [groups[i].course_id, cur_class_id_list])
                        op.change(profs, pid, weeks, second_period[0], second_period[1], [groups[i].course_id, cur_class_id_list])
                        op.change(profs, pid, weeks, second_period[0] + 1, second_period[1], [groups[i].course_id, cur_class_id_list])

                    for cid in cur_class_id_list:
                        oc.change(class_list, cid, weeks, first_period[0], first_period[1], [groups[i].course_id, cur_prof_id_list])
                        oc.change(class_list, cid, weeks, first_period[0] + 1, first_period[1], [groups[i].course_id, cur_prof_id_list])
                        oc.change(class_list, cid, weeks, second_period[0], second_period[1], [groups[i].course_id, cur_prof_id_list])
                        oc.change(class_list, cid, weeks, second_period[0] + 1, second_period[1], [groups[i].course_id, cur_prof_id_list])

        else:
            og.show_error_message('Bad arranging rule parameter: mode ' + str(settings.arranging_rule) + ' not define')
        if err:
            print(err)

        self.is_generated = True
        wait.destroy()
        og.show_succeed_message()

import Timetable as tt
import openpyxl as xl
import operations_gui as og


class SchoolTimetable:
    def __init__(self, title='', major=''):
        self.title = title
        self.major = major
        self.week_num = 30
        workbook = xl.load_workbook('../Input/requirementlss.xx')
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



    def __str__(self):
        return "Not implemented"

    def generate_school_timetable(self, profs, courses, class_list, break_time, settings):

        # Step 1: initialization & checking
        wait = og.show_waiting_message()
        conflicts = []
        for pid in profs.keys():
            profs[pid].schedule = []  # Clear all schedule
            for i in range(self.week_num):
                profs[pid].schedule.append(tt.Timetable(title=profs[pid].name + "'s Timetable of week " + str(i)))
                # in Prof.schedule, for Timetable[i][j],
                # 0: not occupied;
                # not possible: the prof required not to teach in this period(set in Prof info page;
                # break time: the period is in break time, thus not allocated with any courses;
                # (course_id, [classId]): teach Course with course_id to Class(es) with classId(s)in this period

        for cid in class_list.keys():
            class_list[cid].schedule = []  # Clear all schedule
            for i in range(self.week_num):
                class_list[cid].schedule.append(tt.Timetable(title=class_list[cid].classId + "'s Timetable of week " + str(i)))
                # in Class.schedule, for Timetable[i][j],
                # 0: not occupied;
                # break time: the period is in break time, thus not allocated with any courses;
                # (course_id, [prof_id]): be taught Course with course_id by Prof(s) with prof_id(s) in this period

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
            if not c.class_list:
                err.append(c.title + " hasn't been assigned with any classes")
            if not c.taught_by_profs:
                err.append(c.title + " hasn't been assigned with any profs")
        for cid in courses_to_be_allocated.keys():
            if not courses_to_be_allocated[cid].class_list:
                err.append(courses_to_be_allocated[cid].title + " hasn't been assigned with any classes")
            if not courses_to_be_allocated[cid].taught_by_profs:
                err.append(courses_to_be_allocated[cid].title + " hasn't been assigned with any profs")
        if err: print(err)

        # Step 6: pre-distribute courses that are set manually
        err = []
        for c in courses_manually:
            for i in range(c.week_start - 1, c.week_end):
                for p in c.taught_by_profs:
                    err.append(profs[p].schedule[i].check(c.period_required, '0', '1'))  # Check if there's conflict
                for class_a in c.class_list:
                    err.append(class_list[class_a].schedule[i].check(c.period_required, '0', '1'))  # Check if there's conflict
        if err: print(err)
        for c in courses_manually:
            for i in range(c.week_start - 1, c.week_end):
                for p in c.taught_by_profs:
                    profs[p].schedule[i].change(c.period_required, (c.course_id, c.class_list), '1')
                for class_a in c.class_list:
                    class_list[class_a].schedule[i].change(c.period_required, (c.course_id, c.taught_by_profs), '1')

        # Step 5: allocate courses
        # i)

        wait.destroy()
        og.show_succeed_message()

import Prof
import Timetable as tt
import operations_gui as og


class SchoolTimetable:
    def __init__(self, week_num, title='', major=''):
        self.title = title
        self.major = major
        self.week_num = int(week_num)

    def __str__(self):
        return "Not implemented"

    def generate_school_timetable(self, profs, courses, class_list, break_time):

        # Step 1: initialization & checking
        wait = og.show_waiting_message()
        conflicts = []
        for pid in profs.keys():
            profs[pid].schedule = []  # Clear all schedule
            for i in range(self.week_num):
                profs[pid].schedule.append(tt.Timetable())
                # in Prof.schedule, for Timetable[i][j],
                # 0: not occupied;
                # not possible: the prof required not to teach in this period(set in Prof info page;
                # break time: the period is in break time, thus not allocated with any courses;
                # (course_id, [classId]): teach Course with course_id to Class(es) with classId(s)in this period

        for cid in class_list.keys():
            class_list[cid].schedule = []  # Clear all schedule
            for i in range(self.week_num):
                class_list[cid].schedule.append(tt.Timetable())
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
                err = profs[pid].schedule[w].update_based_on(tnp, ['0', 'break time'], ['0', '1'], '1',
                                                             'time not possible')
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

        # Step 5: pre-distribute courses that are set manually
        for c in courses_manually:
            for i in range(c.week_start - 1, c.week_end):
                for p in c.taught_by_profs:
                    p.schedule[i]

        print(profs['1'].schedule[0])
        wait.destroy()
        og.show_succeed_message()

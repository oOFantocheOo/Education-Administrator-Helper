import Class
import Course
import Prof
import Timetable as tt


class SchoolTimetable:
    def __init__(self, week_num, title='', major=''):
        self.title = title
        self.major = major
        self.week_num = week_num

    def __str__(self):
        return "Not implemented"


    def generate_school_timetable(self,profs: list[Prof.Prof], courses: list[Course.Course], class_list: list[Class.Class],
                                  break_time):
        for pid in profs.keys():
            profs[pid].schedule = []
            for i in range(self.week_num):
                profs[pid].schedule.append(tt.Timetable())

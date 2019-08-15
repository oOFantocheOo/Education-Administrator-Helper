import Timetable as tt


class Group:
    def __init__(self, course_id, prof_id_list, class_id_list):
        self.course_id = course_id
        self.prof_id_list = prof_id_list
        self.class_id_list = class_id_list
        self.timetable = tt.Timetable()

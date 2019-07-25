import Timetable as tt


class Course:
    def __init__(self, course_id, course_type, week_start='', week_end='', title='', class_list=[], taught_by_profs=[],
                 period_required=tt.Timetable(), location='', scheduled_manually=False, should_be_scheduled=True):
        self.course_type = course_type
        self.course_id = str(course_id)
        self.title = title
        self.class_list = class_list
        self.week_start = week_start
        self.week_end = week_end
        self.location = location
        self.taught_by_profs = taught_by_profs
        for prof in taught_by_profs:
            self.taught_by_profs.append(prof)
        self.period_required = period_required
        self.period_allocated = []
        self.scheduled_manually = scheduled_manually
        self.should_be_scheduled = should_be_scheduled

    def __str__(self):
        profs_names = ''
        status = ''
        if self.should_be_scheduled:
            status += 'Should be scheduled in the school timetable\n'
        else:
            status += 'Should NOT be scheduled in the school timetable\n'

        if self.scheduled_manually:
            status += 'Scheduled manually'
        else:
            status += 'To be scheduled by the program'
        for prof in self.taught_by_profs:
            profs_names = profs_names + prof.name
        return str(self.course_id) + '\n' + str(self.title) + '\n' + str(profs_names) + '\n' + str(
            *self.class_list) + '\n' + str(self.week_start) + '\n' + str(self.week_end) +'\n'+ status

    def complete_info(self):
        time = self.period_allocated if self.period_allocated else 'Not Allocated Yet!'
        return self.__str__() + '\n' + str(self.period_required) + '\n' + str(self.location) + '\n' + str(time)

    def set_info(self, course_type, week_start, week_end, title, location=''):
        self.course_type = course_type
        self.title = title
        self.week_start = week_start
        self.week_end = week_end
        self.location = location

    def set_scheduled_manually(self):
        self.scheduled_manually = True

    def set_not_scheduled_manually(self):
        self.scheduled_manually = False

    def set_should_be_scheduled(self):
        self.should_be_scheduled = True

    def set_should_not_be_scheduled(self):
        self.should_be_scheduled = False

    def clear_classes(self):
        self.class_list = []

    def add_class(self, class_a):
        self.class_list.append(class_a)

    def clear_profs(self):
        self.taught_by_profs = []

    def add_prof(self, prof):
        self.taught_by_profs.append(prof)

class Course:
    def __init__(self, course_id, course_type, title='', class_list='', week_start='', week_end='', taught_by_profs=[],
                 period_required='', location='', scheduled_manually=False):
        self.course_type = course_type
        self.course_id = course_id
        self.title = title
        self.class_list = class_list
        self.week_start = week_start
        self.week_end = week_end
        self.location = location
        self.taught_by_profs = []
        for prof in taught_by_profs:
            self.taught_by_profs.append(prof)
        self.period_required = period_required
        self.period_allocated = ''
        self.scheduled_manually = scheduled_manually

    def __str__(self):
        profs_names = ''
        for prof in self.taught_by_profs:
            profs_names = profs_names + prof.name
        return str(self.course_id) + '\t' + str(self.title) + '\t' + str(profs_names) + '\t' + str(
            self.class_list) + '\t' + str(self.week_start) + '\t' + str(self.week_end)

    def complete_info(self):
        time = self.period_allocated if self.period_allocated else 'Not Allocated Yet!'
        return self.__str__() + '\t' + str(self.period_required) + '\t' + str(self.location) + '\t' + str(
            self.frequency) + '\t' + str(time)

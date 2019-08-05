import Timetable as tt


class Prof:

    def __init__(self, prof_id, name="", telephone=''):
        self.prof_id = str(prof_id)
        self.name = name
        self.telephone = str(telephone)
        self.schedule = []
        self.time_preferred = tt.Timetable()
        self.time_not_possible = tt.Timetable()

    def __str__(self):
        return str(self.name)

    def complete_info(self):
        tp = self.time_preferred.__str__()
        tnp = self.time_not_possible.__str__()
        tele = self.telephone if self.telephone else 'N/A'
        return self.__str__() + '\t' + str(tele) + '\t' + str(tp) + '\t' + str(tnp)

    def change_telephone(self, telephone):
        self.telephone = str(telephone)

    def change_name(self, name):
        self.name = str(name)

    def change_id(self, id):  # check if same
        self.prof_id = id

    def clear_time_preference(self):
        self.time_preferred = tt.Timetable()
        self.time_not_possible = tt.Timetable()

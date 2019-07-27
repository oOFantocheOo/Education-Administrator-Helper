import  pickle

class Settings:
    def __init__(self):
        self.language = 0
        # 0: English
        # 1: Chinese

        self.arranging_rule = 0
        # When arranging SchoolTimetable,
        # 0: Set priority to periods that are most empty
        # 1: Closely pack every course

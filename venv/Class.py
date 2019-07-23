class Class:
    def __init__(self, major='', grade='', index=''):
        self.major = str(major)
        self.grade = str(grade)
        self.index = str(index)
        self.schedule = []
        self.classId = str(major) + str(grade) + str(index)

    def __str__(self):
        return self.major + self.grade + self.index

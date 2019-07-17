import pickle


def load_courses():
    return pickle.load(open("courses_file", "rb"))


def save_courses(course_list):
    pickle.dump(course_list, open("courses_file", "wb"))


def all_courses_info():
    courses = load_courses()
    string = 'ID\tTitle\tProfs\tClasses\tWeek Start\tWeek End\n'
    for course in courses:
        string += course.__str__()
        string += '\n'
    return string

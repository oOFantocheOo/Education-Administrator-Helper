import pickle


def load_courses():
    return pickle.load(open("courses_file", "rb"))


def save_courses(course_list):
    pickle.dump(course_list, open("courses_file", "wb"))


def all_courses_info(courses):
    string = 'ID\tTitle\tProfs\tClasses\tWeek Start\tWeek End\n'
    for cid in courses.keys():
        string += courses[cid].__str__()
        string += '\n'
    return string


def find_course_by_title(courses, title):
    for cid in courses.keys():
        if title == courses[cid].title:
            return courses[cid]
    return None


def find_course_by_course_id(courses, course_id):
    if course_id not in courses:
        return None
    else:
        return courses[course_id]


def selected_courses_info(courses):
    string = 'ID\tTitle\tProfs\tClasses\tWeek Start\tWeek End\n'
    for c in courses:
        string += c.__str__()
        string += '\n'
    return string


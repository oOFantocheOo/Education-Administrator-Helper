import pickle
import tkinter as tk

import Course
import openpyxl as xl
import operations_gui as og
import operations_profs as op


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


def display_course(page, course, n, profs):  # In which page, display which course, and this is the nth course to display
    profs_names = ''
    classes = ''
    for prof in course.taught_by_profs:
        profs_names += ' ' + profs[prof].name
    for class_a in course.class_list:
        classes += ' ' + class_a

    row = [tk.Label(page) for _ in range(7)]
    row.append(tk.Button(page, text='Details..', command=lambda a=course: og.show_course_info(a,profs)))

    row[0]['text'] = str(course.course_id)
    row[1]['text'] = str(course.title)
    row[2]['text'] = str(course.course_type)
    row[3]['text'] = str(profs_names)
    row[4]['text'] = str(classes)
    row[5]['text'] = str(course.week_start)
    row[6]['text'] = str(course.week_end)

    for i in range(8):
        row[i].grid(row=6 + n, column=i)


# Extract info from the first worksheet in courses.xlsx
# column1: ID; column2: title
def update_courses(courses):
    workbook = xl.load_workbook('courses.xlsx')
    worksheet = workbook[workbook.sheetnames[0]]

    i = 1
    while worksheet['A' + str(i)].value:
        id = str(worksheet['A' + str(i)].value)
        title = str(worksheet['B' + str(i)].value)
        courses[id] = Course.Course(id, title)
        i += 1

import tkinter as tk

course_page = tk.Tk()
course_page.title("Course Information")
v1 = tk.Variable()
v1.set(1)
v2 = tk.Variable()
v2.set(1)
v3 = tk.Variable()
v3.set(1)
v4 = tk.Variable()
v4.set(0)

b1 = tk.Checkbutton(course_page, variable=v1, text='Scheduled manually').pack()
b2 = tk.Checkbutton(course_page, variable=v2, text='Scheduled automatically').pack()
b3 = tk.Checkbutton(course_page, variable=v3, text='Should be scheduled').pack()
b4 = tk.Checkbutton(course_page, variable=v4, text='Should not be scheduled').pack()

course_page.mainloop()

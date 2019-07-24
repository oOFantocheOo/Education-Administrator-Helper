import tkinter as tk


def show_school_timetable_widget(parent):
    st_widget = tk.Toplevel(parent)
    st_widget.geometry('300x200')

    def create_empty_school_timetable(week_num, title):
        st_widget.destroy()

    st_widget.title('Create School Timetable')
    tk.Label(st_widget, text='Title of school timetable:').pack()
    e1 = tk.Entry(st_widget)
    e1.insert(tk.END, 'qwe')
    e1.pack()
    tk.Label(st_widget, text='Number of weeks:').pack()
    e2 = tk.Entry(st_widget)
    e2.insert(tk.END, 3)
    e2.pack()
    tk.Button(st_widget, text='OK', command=lambda: create_empty_school_timetable(e2.get(), e1.get())).pack()
    tk.Button(st_widget, text='Cancel', command=st_widget.destroy).pack()
    st_widget.lift(parent)
    print('lifted')


def show_root_page():
    root = tk.Tk()
    root.geometry('600x400')
    root.title("Educational Administration Helper")
    button1 = tk.Button(root, text="Set Timetable", command=lambda: show_school_timetable_widget(root))
    button1.pack()
    label = tk.Label(root, text='School timetable not initialized yet!')
    label.pack()

    root.mainloop()


show_root_page()

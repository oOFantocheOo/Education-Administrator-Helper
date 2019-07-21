import tkinter as tk
def show_breaktime_page(breaktime):
    breaktime_page = tk.Tk()
    breaktime_page.title("Break Time")
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    height = 12
    width = 7
    button_array = []
    var_array=[]

    def save_break_time(row, col):
        print(var_array[row][col].get())
        # breaktime[row][col]=button_array[row][col]

    for j in range(width):
        b = tk.Label(breaktime_page, text=week[j])
        b.grid(row=0, column=j + 1)
    for i in range(height):
        b = tk.Label(breaktime_page, text='period' + str(i + 1))
        b.grid(row=i + 1, column=0)

    for i in range(height):
        button_array.append([])
        var_array.append([])
        for j in range(width):
            v=tk.IntVar()
            b = tk.Checkbutton(breaktime_page, command=lambda: save_break_time(i, j), variable=v)
            b.grid(row=i + 1, column=j + 1)
            button_array[i].append(b)
            var_array[i].append(v)

    breaktime_page.mainloop()
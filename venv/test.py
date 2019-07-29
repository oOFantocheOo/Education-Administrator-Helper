import tkinter as tk

root = tk.Tk()

height = 30
width = 10
for i in range(height):  # Rows
    for j in range(width):  # Columns
        b = tk.Entry(root, text="")
        b.grid(row=i, column=j)
for i in range(height):  # Rows
    for j in range(width):  # Columns
        b = tk.Label(root, text="")
        b.grid(row=i, column=j)

for i in range(height):  # Rows
    for j in range(width):  # Columns
        b = tk.Label(root, text="")
        b.grid(row=i, column=j)

for i in range(height):  # Rows
    for j in range(width):  # Columns
        b = tk.Label(root, text="")
        b.grid(row=i, column=j)

for i in range(height):  # Rows
    for j in range(width):  # Columns
        b = tk.Label(root, text="")
        b.grid(row=i, column=j)

tk.mainloop()

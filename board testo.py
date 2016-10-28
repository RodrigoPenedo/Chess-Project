from tkinter import *
from tkinter import ttk

root = Tk()
frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)

grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1,minsize=50)
Grid.columnconfigure(frame, 0, weight=1,minsize=50)


for x in range(8):
    a = True
    if x % 2:
        a = False
    for y in range(8):
        if a == True:
            btn = Button(frame,bg = "black")
            a = False
        else:
            btn = Button(frame,bg = "white")
            a = True

        btn.grid(column=x, row=y, sticky=N+S+E+W)


for x in range(8):
  Grid.columnconfigure(frame, x, weight=1, minsize=50)

for y in range(8):
  Grid.rowconfigure(frame, y, weight=1, minsize=50)

def motion(event):
    grid_location(x, y)

def mouse(event):
    grid_info = event.widget.grid_info()
    print(grid_info["row"], grid_info["column"])




root.bind("<Button-1>", mouse)

root.mainloop()

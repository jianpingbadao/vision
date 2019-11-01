from main import execute
from tkinter import *
from tkinter.ttk import *


window = Tk()

window.title("Traffic Analyzer")
 
window.geometry('650x400')
up_down = 0

lbl = Label(window, text="What is the name of the file?")
lbl1 = Label(window, text="What would you like to name the results?")
lbl2 = Label(window, text="Would up like to display cars going down only, up only, or both?")

lbl.grid(column=0, row=0)
lbl1.grid(column=0, row=1)
lbl2.grid(column=0, row=2)

txt = Entry(window,width=10)
txt1 = Entry(window,width=10)

txt.grid(column=1, row=0)
txt1.grid(column=1, row=1)
 


def clicked():    
    file_name = "" + txt.get()
    result_name = "" + txt1.get()
    
    execute(file_name, result_name, up_down)


def clicked1():
    global up_down
    up_down = 1

    

def clicked2():
    global up_down
    up_down = 2

def clicked3():
    global up_down
    up_down = 0

    

rad1 = Radiobutton(window,text='Down', value=1, command=clicked3)
rad2 = Radiobutton(window,text='Up', value=2, command=clicked1)
rad3 = Radiobutton(window,text='Both', value=3, command=clicked2)

rad1.grid(column=1, row=2)
rad2.grid(column=2, row=2)
rad3.grid(column=3, row=2)

btn = Button(window, text="Run", command=clicked) 
btn.grid(column=3, row=4)
 
window.mainloop()
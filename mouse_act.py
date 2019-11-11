
import cv2
import numpy as np
import vehicles
import time
import tkinter as tk, threading
from tkinter import filedialog
import imageio
from PIL import Image, ImageTk
from pynput.mouse import Listener

import os

# https://www.youtube.com/watch?v=kJshtCfqCsY

# def on_move(x,y):
#    print("Mouse moved to ({0}, {1})".format(x,y))
win = tk.Tk()
win.geometry("1000x600")
win.title("New GUI")

height = 200 
width = 400

vid_h = 300
vid_w = 690

valid = False

def enable():
    global valid 
    valid = True
    print("enabled")
    
x = 1
y = 2
vid_x = (x/width)*vid_w
vid_y = (y/height)*vid_h
string = str(x) + ' , ' + str(y) + '    vid coordinates: ' + str(vid_x) + ' , ' + str(vid_y)

Button_w = tk.Button(win, text = "Select line 1 pt 1", command = enable)
Button_w.grid(row = 3, column = 0)
Label_1 = tk.Label(win, text = string)
Label_1.grid(row = 3, column = 1)

Button_w = tk.Button(win, text = "Select line 1 pt 2", command = enable)
Button_w.grid(row = 4, column = 0)
Label_2 = tk.Label(win, text = string)
Label_2.grid(row = 4, column = 1)

Button_w = tk.Button(win, text = "Select line 2 pt 1", command = enable)
Button_w.grid(row = 5, column = 0)
Button_w = tk.Button(win, text = "Select line 2 pt 2", command = enable)
Button_w.grid(row = 6, column = 0)

Button_w = tk.Button(win, text = "Select line 3 pt 1", command = enable)
Button_w.grid(row = 7, column = 0)
Button_w = tk.Button(win, text = "Select line 3 pt 2", command = enable)
Button_w.grid(row = 8, column = 0)

Button_w = tk.Button(win, text = "Select line 4 pt 1", command = enable)
Button_w.grid(row = 9, column = 0)
Button_w = tk.Button(win, text = "Select line 4 pt 2", command = enable)
Button_w.grid(row = 10, column = 0)

def on_click(x, y, button, pressed):
    global valid
    if(valid):
        print("Mouse clicked at({0}, {1}) with {2}".format(x,y,button))
        valid = False
    else:
        print("not valid") 
        valid = True   



#def on_scroll(x,y,dx,dy):
   # print("Mouse scrolledat ({0},{1})({2}, {3})".format(x, y, dx, dy))
#
#with Listener(on_move = on_move, on_click = on_click, on_scroll = on_scroll) as listener:
 #   listener.join()
win.mainloop()
with Listener(on_click = on_click) as listener:
    listener.join()
# if cv2.waitKey(1) & 0xFF == ord('q'):
  #   sys.exit()

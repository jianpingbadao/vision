import cv2
import numpy as np
import vehicles
import time
import tkinter 
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import imageio
from PIL import Image, ImageTk



class Root(Tk):




    def __init__(self):
        super(Root, self).__init__()
        self.title("Video File Opener Window")
        self.minsize(600, 400)

        
        self.labelFrame = ttk.LabelFrame(self, text = "Open A Video File")
        self.labelFrame.grid(row = 1, column = 0, padx = 10, pady = 20)
        self.button()
        # self.printf()

    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "File Browser", command = self.fileDialog)
        self.button.grid(row = 1, column = 1)


    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir = '/', title = "Select a File")
        self.label = ttk.Label(self)
        self.label.grid(row = 2, column = 1)
        self.label.configure(text = self.filename)
        cap = cv2.VideoCapture(self.filename)
        while True:
            
            _, self.frame = cap.read()
            self.frame = self.Frame(title = "Vid Frame")
            self.frame.grid(row = 5, column = 0, padx = 10, pady = 20)
            
            cv2.imshow('frame', self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        # return self.filename
    
    #def printf(self):
     #   print(self.fileDialog())

if __name__ == '__main__':
    root = Root()
    root.mainloop()










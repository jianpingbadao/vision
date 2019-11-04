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
        # Constructor, Makes version 
        # Args: self = Root
        super(Root, self).__init__()
        self.title("Video File Opener Window")
        self.minsize(600, 400) # Min size of window

        #Graphics window
        self.imageFrame = ttk.Frame(self, width=600, height=500)
        self.imageFrame.grid(row=0, column=0, padx=10, pady=2)

        #Capture video frames
        self.lmain = ttk.Label(self.imageFrame)
        self.lmain.grid(row=4, column=4)

        self.labelFrame = ttk.LabelFrame(self, text = "Open A Video File")
        self.labelFrame.grid(row = 1, column = 0, padx = 10, pady = 20)
        self.button()
        
        # self.printf()

    def button(self):
        # Create Button to open file directory
        
        self.button = ttk.Button(self.labelFrame, text = "File Browser", command = self.fileDialog)
        self.button.grid(row = 2, column = 0)


    def fileDialog(self):
        #Reads file to video and displays video in Gui
        vid_x = 500 # Vid Width
        vid_y = 300 # Vid Height


        self.filename = filedialog.askopenfilename(initialdir = '/', title = "Select a File") # Read File
        self.label = ttk.Label(self)
        self.label.grid(row = 3, column = 0)
        self.label.configure(text = self.filename) # Display filename
        cap = cv2.VideoCapture(self.filename) # Play video of file
        while True:
            # Video 
            _, self.frame = cap.read()
            # cv2.imshow('frame', self.frame)
            # self.frame = cv2.flip(self.frame, 1)
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)

            copy_of_image = img.copy() 
            img = copy_of_image.resize((vid_x,vid_y)) # size of video
            imgtk = ImageTk.PhotoImage(image=img)
    
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.lmain.after(10, filedialog) 




            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            input('q')
            self.quit()
        cap.release()
        cv2.destroyAllWindows()
        # return self.filename
    
    #def printf(self):
     #   print(self.fileDialog())

if __name__ == '__main__':
    root = Root()
    root.mainloop()










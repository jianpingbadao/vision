# This is the main file that houses the Gui for the video display
# It has a search button that opens up the file directory to select a video
# Displays the video file name below
# The Submit button tracks the mouse click, but only in the pixels of the button, needs to be fixed

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
from pynput.mouse import Controller

import os


class Root(Tk):

    

    def __init__(self):
        # Constructor, Makes version 
        # Args: self = Root
        super(Root, self).__init__()
        self.title("Video File Opener Window")
        self.minsize(600, 400) # Min size of window

        self.video_image_tk = None  # save the first frame of the video as an ImageTk obj
        self.video_file_loaded = False

        #Graphics window
        global vid_x
        global vid_y
        self.imageCanvas = Canvas(self, width=vid_x, height=vid_y, bg='grey')
        self.imageCanvas.bind("<Button-1>", self.canvasClickCallBack)
        self.imageCanvas.grid(row=0, column=0)

        self.create_entries_to_hold_lines()
        #Capture video frames
        self.lmain = ttk.Label(self.imageFrame)
        self.lmain.grid(row=4, column=4)

        self.labelFrame = ttk.LabelFrame(self, text = "Open A Video File")
        self.labelFrame.grid(row = 1, column = 0, padx = 10, pady = 20)
        self.button()
        # self.printf()
        self.mouse = Controller()
        global coord
        coord = ''
        self.pt_1 = ttk.Label(self, text = coord)
        self.pt_1.grid(row = 4, column = 6)

        """Create Submit Button"""
        # self.photo = Image.open("C:\Users\mhepel\Pictures\Cars_1.jpeg")
        self.submitButton = Button(self, command=self.buttonClick, text="Submit")
        self.submitButton.grid(row = 4, column = 5)
        

        global val 
        val = False
        # self.click()
        if(val == True):
            val = False
            print("second click")
            # self.buttonClick()

    

    def buttonClick(self):

    def create_entries_to_hold_lines(self):
        """
        Create entries to hold information about the lines that we will click/enter later.
        """
        self.num_of_groups = 2
        self.num_of_lines_per_group = 3
        self.num_of_clicks_per_line = 2
        self.entry_strvars = [[StringVar() for _ in range(self.num_of_lines_per_group)] for _ in range(self.num_of_groups)]

        self.line_entries = []
        start_row = 3
        start_col = 0
        for group in range(self.num_of_groups):
            line_entries_cur_group = []
            for row in range(self.num_of_lines_per_group):
                line_entry = Entry(self, textvariable=self.entry_strvars[group][row])
                cur_row = start_row + row + group * self.num_of_lines_per_group
                line_entry.grid(row=cur_row, column=start_col)
                line_entries_cur_group.append(line_entry)
            self.line_entries.append(line_entries_cur_group)

        self.cur_group = 0
        self.cur_line = 0
        self.cur_click = 0

        """ handle button click event and output text from entry area"""
        global val
        val = True
        print('hello')    # do here whatever you want
        global coord
        coord = "f {0}".format(self.mouse.position)
        self.pt_1.configure(text = coord)
        print(coord)
        
    
    

    global vid_x 
    vid_x = 500 # Vid Width
    global vid_y 
    vid_y = 300 # Vid Height

    # def click(self):
      #  global vid_x
       # global vid_y
       # x = vid_x + 100
       # y = vid_y + 100
       # self.vid_button = ttk.Button(self)
       # self.vid_button.config(width = x, height = y)
       # self.vid_button.grid(row = 0, column = 0)
       # print("x: {0}".format(self.mouse.position))

    def button(self):
        # Create Button to open file directory
        self.button = ttk.Button(self.labelFrame, text = "File Browser", command = self.fileDialog)
        self.button.grid(row = 1, column = 1)

    
    

    def check_video_file(self, filename):
        """
        Check whether the given video filename is valid or not.

        Parameters
        ----------
        filename : str
            The filename (absolute path) of the video file.

        Returns
        -------
        bool
            True if the filename is one of the supported video format. False, otherwise.
        """
        if not filename:
            return False

        supported_video_format = ['mp4', 'avi', 'm4v']
        for extension in supported_video_format:
            if filename.endswith(extension):
                return True
        return False
    
    


    def fileDialog(self):
        #Reads file to video and displays video in Gui
        global vid_x
        vid_x = 500 # Vid Width
        global vid_y
        vid_y = 300 # Vid Height
        self.filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select a File") # Read File

        if not self.check_video_file(self.filename):
            return

        self.filename_strvar.set(self.filename) # Display filename
        cap = cv2.VideoCapture(self.filename) # Play video of file

        # while True:
        # Video 
        _, self.frame = cap.read()
        # cv2.imshow('frame', self.frame)
        frame = cv2.flip(self.frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)

        copy_of_image = img.copy() 
        img = copy_of_image.resize((vid_x,vid_y)) # size of video
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_image_tk = imgtk # keep a reference to the image, otherwise, it will be destroyed by garbage-collection
        self.imageCanvas.create_image(0, 0, anchor=NW, image=imgtk)

        self.video_file_loaded = True

        # self.newbut = ttk.Button(self.labelFrame, image = img, command = self.buttonClick)
        # self.newbut.grid(row = 0, column = 0)
        # self.lmain.after(10, self.fileDialog) 

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        cap.release()
        cv2.destroyAllWindows()
        # return self.filename
    
    #def printf(self):
     #   print(self.fileDialog())

if __name__ == '__main__':
    root = Root()
    root.mainloop()
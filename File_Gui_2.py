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

val = False
coord = None
vid_x = 500 # Width of video
vid_y = 300 # Height of video


class Root(Tk):

    def __init__(self):
        # Constructor, Makes version 
        # Args: self = Root
        super(Root, self).__init__()
        self.title("Video File Opener Window")
        self.minsize(600, 500) # Min size of window

        self.video_image_tk = None  # save the first frame of the video as an ImageTk obj
        self.video_file_loaded = False

        #Graphics window
        global vid_x
        global vid_y
        self.imageCanvas = Canvas(self, width=vid_x, height=vid_y, bg='grey')
        self.imageCanvas.bind("<Button-1>", self.canvasClickCallBack)
        self.imageCanvas.grid(row=0, column=0 , rowspan=10 ,columnspan=1)

        self.labelFrame = ttk.LabelFrame(self, text="Open A Video File")
        self.labelFrame.grid(row=11, column=0, padx=10, pady=20)
        self.create_file_dialog_button()

        # filename entry
        self.filename_strvar = StringVar()
        self.filename_entry = Entry(self, textvariable=self.filename_strvar, width=40)
        self.filename_entry.grid(row=13, column=0)
        
        # Assigns num of lanes for data point entries
        num_lanes = 1    # Default 1 lane, for some reason can only increase lanes, can't decrease
        self.create_entries_to_hold_lines(num_lanes)
        self.label_lane = Label(self, text = "Enter # of lanes").grid(row = 0, column = 1)
        self.entry_lane = Entry(self, textvariable = self.num_of_groups)
        self.entry_lane.grid(row = 1, column = 1)

        self.mouse = Controller()
        global coord
        coord = ''
        self.pt_1 = ttk.Label(self, text=coord)
        self.pt_1.grid(row=4, column=6)

        """Create Submit Button"""
        # self.photo = Image.open("C:\Users\mhepel\Pictures\Cars_1.jpeg")
        self.submitButton = Button(self, command=self.submitButtonClick, text="Submit", state = DISABLED)
        self.submitButton.grid(row=1, column=2)

        self.next_entry()
        global next_clicked 
        next_clicked = True
        global val 
        val = False
        # self.click()
        if(val == True):
            val = False
            print("second click")
            # self.submitButtonClick()


    def next_entry(self):
        print("next") # debug
        global next_clicked
        next_clicked = True
        print(next_clicked) # debug


    def create_entries_to_hold_lines(self, num_lanes):
        """
        Create entries to hold information about the lines that we will click/enter later.
        """
        self.num_of_groups = num_lanes
        self.prev_lanes = 0
        self.num_of_lines_per_group = 3
        self.num_of_clicks_per_line = 2
        self.entry_strvars = [[StringVar() for _ in range(self.num_of_lines_per_group)] for _ in range(self.num_of_groups)]

        # self.button_next = Button(self, text = "next", command = self.next_entry)
        # self.button_next.grid(row = 3, column = 2)

        self.line_entries = []
        start_row = 3
        start_col = 1
        for group in range(self.num_of_groups):
            line_entries_cur_group = []
            # next_entries_cur_group = []
            for row in range(self.num_of_lines_per_group):
                line_entry = Entry(self, textvariable=self.entry_strvars[group][row])
                button_next = Button(self, text = "next", state = DISABLED, command = self.next_entry) # next button
                # self.button_next.grid(row = 3, column = 2)
                cur_row = start_row + row + group * self.num_of_lines_per_group
                line_entry.grid(row=cur_row, column=start_col)
                button_next.grid(row = cur_row, column = start_col +1)
                line_entries_cur_group.append(line_entry)
                # next_entries_cur_group.append(button_next)
            self.line_entries.append(line_entries_cur_group)

        if self.prev_lanes > self.num_of_groups: # check to see if the new amount of lanes is less than the previous
            # for ln in range(self.prev_lanes - self.num_of_groups):
            for line_entry in self.grid_slaves():
                if int(line_entry.grid_info()["row"]) > self.num_of_groups:
                    line_entry.grid_forget()
                # line_entry.grid_forget(row = self.num_of_groups + ln, column = start_col)
        self.cur_group = 0
        self.cur_line = 0
        self.cur_click = 0
        self.prev_lanes = num_lanes
        

    def canvasClickCallBack(self, event):
        """The call back function when the mouse clicks on the image canvas.
        It will fill out the entries one by one.
        Parameters
        ----------
        event : obj
            The click event.
        """
        global next_clicked
        print(next_clicked)
        line_one = False
        print(f"{event.x}, {event.y}")
        # self.line_entries[self.cur_group][self.cur_line].insert(-1, f"{event.x}, {event.y}")
        

        if self.cur_click == 0:
            self.entry_strvars[self.cur_group][self.cur_line].set(f"{event.x}, {event.y}")
        else:
            _content = self.entry_strvars[self.cur_group][self.cur_line].get()
            _content += f", {event.x}, {event.y}"
            self.entry_strvars[self.cur_group][self.cur_line].set(_content)
        
        self.cur_click += 1
            
        if self.cur_click == self.num_of_clicks_per_line:
            self.cur_click = 0
            # self.imageCanvas.create_line(_content)
            print(self.entry_strvars[self.cur_group][self.cur_line].get().split(', '))
            # print(self.entry_strvars[self.cur_group][self.cur_line].get()[15:18])
            x_1 = int(self.entry_strvars[self.cur_group][self.cur_line].get().split(', ')[0])
            y_1 = int(self.entry_strvars[self.cur_group][self.cur_line].get().split(', ')[1])
            x_2 = int(self.entry_strvars[self.cur_group][self.cur_line].get().split(', ')[2])
            y_2 = int(self.entry_strvars[self.cur_group][self.cur_line].get().split(', ')[3])
            print(x_1)
            print(y_1)
            print(x_2)
            print(y_2)
             
            
            # self.imageCanvas.create_line(x_1, y_1, x_2, y_2)
            # self.imageCanvas.create_line(0,0,40,40)
            if self.cur_line == self.num_of_lines_per_group:
                self.cur_line = 0
                self.cur_group += 1
                self.cur_group %= self.num_of_groups

        # Draw line on canvas
        if next_clicked == True:
            canvas_id_one = self.imageCanvas.create_line(x_1, y_1, x_2, y_2)

            # Delete line
            self.imageCanvas.after(line_one == False, self.imageCanvas.delete, canvas_id_one) ######
            
            self.cur_line += 1  # move to the next line
            self.cur_click = 0
            next_clicked = False
            if self.cur_line == self.num_of_lines_per_group:
                self.cur_line = 0
                self.cur_group += 1
                self.cur_group %= self.num_of_groups

        

    def submitButtonClick(self):
        """ handle button click event and output text from entry area"""
        input = self.entry_lane.get()
        print(input)
        self.create_entries_to_hold_lines(int(input))
        self.cur_line = 0
        self.submitButton.config(state = DISABLED)
        # self.button_next.config(state = NORMAL)
        # self.submitButton.config(state = DISABLED)

        


    # def click(self):
      #  global vid_x
       # global vid_y
       # x = vid_x + 100
       # y = vid_y + 100
       # self.vid_button = ttk.Button(self)
       # self.vid_button.config(width = x, height = y)
       # self.vid_button.grid(row = 0, column = 0)
       # print("x: {0}".format(self.mouse.position))


    def create_file_dialog_button(self):
        # Create Button to open file directory
        self.button = ttk.Button(self.labelFrame, text="File Browser", command=self.fileDialog)
        self.button.grid(row=12, column=0)


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

        supported_video_format = ['mp4', 'avi', 'm4v', 'mov']
        for extension in supported_video_format:
            if filename.endswith(extension):
                return True
        return False


    def fileDialog(self):
        #Reads file to video and displays video in Gui
        global vid_x
        global vid_y

        # Disable button
        self.button.config(state = DISABLED)
        self.submitButton.config(state = NORMAL)
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File") # Read File

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
        img = copy_of_image.resize((vid_x, vid_y)) # size of video
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_image_tk = imgtk # keep a reference to the image, otherwise, it will be destroyed by garbage-collection
        self.imageCanvas.create_image(0, 0, anchor=NW, image=imgtk)
        ##### Draw lines
        # self.imageCanvas.create_line()


        self.video_file_loaded = True

        # self.newbut = ttk.Button(self.labelFrame, image = img, command = self.submitButtonClick)
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
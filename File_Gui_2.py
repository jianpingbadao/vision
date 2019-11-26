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
i = 0   # iterator for num of groups, used for next button
j = 0   # iterator for num of lanes per group, used for next button
end = False # boolean if all points have been input
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
        
        # Reset
        self.reset_button = Button(self, command=self.reset, text="Reset", state = NORMAL)
        self.reset_button.grid(row = 14, column = 0)

        # Process
        self.process_button = Button(self, command=self.process, text="Process", state = NORMAL)
        self.process_button.grid(row = 15, column = 0)

        # Assigns num of lanes for data point entries
        num_lanes = 1    # Default 1 lane, for some reason can only increase lanes, can't decrease
        self.create_entries_to_hold_lines(num_lanes)
        self.label_lane = Label(self, text = "Enter # of lanes").grid(row = 0, column = 1)
        self.entry_lane = Entry(self, textvariable = self.num_of_groups, state = DISABLED)
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

        # self.next_entry(index)
        global next_clicked 
        next_clicked = False
        global val 
        val = False
        # self.click()
        if(val == True):
            val = False
            print("second click")
            # self.submitButtonClick()

        # self.next_entries = []

    def next_entry(self):
       global i
       global j
       print("next") # debug
       global next_clicked
       next_clicked = True
       print(next_clicked) # debug
       self.next_entries[i][j].config(state = DISABLED)
       self.line_entries[i][j].config(state = DISABLED)
       if i <= self.num_of_groups-1:
            # self.next_entries[i][j].config(state = NORMAL)
            if i == self.num_of_groups-1 and j == self.num_of_lines_per_group-1:
                print("end") 
                # end = True
                self.end()
            else:
                j += 1
                if j == self.num_of_lines_per_group:
                    i +=1
                    j = 0
                self.next_entries[i][j].config(state = NORMAL)
                self.line_entries[i][j].config(state = NORMAL)
            
            
    ######
    # def next_entry(self):
      #  for btn in self.next_entries_cur_group:
       #     if str(btn['state']) == 'disabled':
           #  btn.configure(state = 'normal')
        # self.next_entries_cur_group[index].configure(state = 'disabled')
    
    
    # Process
    def process(self):
        '''
        should take in filename, # of lanes, # of lines per group,
        use those to iterate through each entry and collect points.
        Use point data with vid_x, vid_y size to get ratio
        Send to other video processing function for process.
        In other video processing function use ratio to set lines 
        on original video size.
        Alternatively could probably set video to be processed to specific size
        as is done in this file for the screen shot.

        Probably want to disable this function/button until all data is entered
        to avoid errors.
        '''
        print(self.num_of_groups)
        print(self.num_of_lines_per_group)
        print(self.filename)


    ######
    ### Reset
    def reset(self):
        ''' Reset will reset all the values on the screen.
        User will be able to choose a new file and start over
        File must be enabled
        Text boxes must be cleared and lanes must be destroyed
        '''
        global i
        global j
        self.filename = ' '
        self.button.config(state = NORMAL)
        
        # Destroy old entry boxes and next buttons
        for n in range(self.num_of_groups):
            for m in range(self.num_of_lines_per_group):
                # self.next_entries[n][m].destroy()
                # self.line_entries[n][m].destroy()
                self.next_entries[n][m].grid_forget()
                self.line_entries[n][m].grid_remove()
        print(self.num_of_groups)
        print(self.num_of_lines_per_group)
        self.entry_lane.grid_forget()
        # self.filename_strvar.set(self.filename) # Display filename
        self.submitButton.config(state = DISABLED)
        # self.entry_lane.config(state = NORMAL)
        self.num_of_groups = 0
        # self.entry_lane.update()
        # self.entry_lane.config(state = DISABLED)
        self.entry_lane = Entry(self, textvariable = self.num_of_groups, state = DISABLED)
        self.entry_lane.grid(row = 1, column = 1)
        i = 0
        j = 0
        #self.imageCanvas.bind('<1>', self.canvasClickCallBack)
        self.imageCanvas.bind('<1>', self.canvasClickCallBack)



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

        self.line_entries = [] # list of list of text widgets
        self.next_entries = [] # list of list of buttons
        
        start_row = 3
        start_col = 1
        next_button_index = 0 # keeps track of next button
        for group in range(self.num_of_groups):
            line_entries_cur_group = []
            next_entries_cur_group = []
            for row in range(self.num_of_lines_per_group):
                line_entry = Entry(self, textvariable=self.entry_strvars[group][row], state = DISABLED)
                # button_next = Button(self, text = "next", state = DISABLED, command = lambda: self.next_entry(next_button_index)) # next button
                
                # Create next button
                # next_entries_cur_group.append(Button(self, text=("next"+ str(next_button_index)), state = DISABLED, command=lambda c=row: print(next_entries_cur_group[c].cget("text"))))
                next_button_index += 1
                next_entries_cur_group.append(Button(self, text=("next"+ str(next_button_index)), state = DISABLED, command = self.next_entry))
                cur_row = start_row + row + group * self.num_of_lines_per_group
                line_entry.grid(row=cur_row, column=start_col)
                # button_next.grid(row = cur_row, column = start_col +1)
                next_entries_cur_group[row].grid(row = cur_row, column = start_col +1)
                line_entries_cur_group.append(line_entry)
                # next_entries_cur_group.append(button_next)
                
            # next_entries_cur_group[1].config(state = DISABLED) # disables button 2 in each group.
            self.next_entries.append(next_entries_cur_group)
            self.line_entries.append(line_entries_cur_group)
        
        # self.next_entries[0][1].config(state = NORMAL) # enable disable buttons

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
        
    def end(self):
        """a
        Signal to end / freeze canvas to stop allowing button clicks
        """
        self.imageCanvas.unbind('<1>') # unbind canvas


    def canvasClickCallBack(self, event):
        """The call back function when the mouse clicks on the image canvas.
        It will fill out the entries one by one.
        Parameters
        ----------
        event : obj
            The click event.
        """
        global x_1 
        global y_1 
        global x_2 
        global y_2     
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
                            
            canvas_id_one = self.imageCanvas.create_line(x_1, y_1, x_2, y_2)
            self.imageCanvas.after(1000, self.imageCanvas.delete, canvas_id_one) # Delete after 1 second
            if next_clicked == True:
                canvas_id_one = self.imageCanvas.create_line(x_1, y_1, x_2, y_2)
                # next_clicked = False 
            
            # self.imageCanvas.create_line(x_1, y_1, x_2, y_2)
            # self.imageCanvas.create_line(0,0,40,40)
            if self.cur_line == self.num_of_lines_per_group:
                self.cur_line = 0
                self.cur_group += 1
                self.cur_group %= self.num_of_groups

        # Draw line on canvas

            if next_clicked == True:
                canvas_id_one = self.imageCanvas.create_line(x_1, y_1, x_2, y_2)
                print(x_1)
                print(y_1)
                print(x_2)
                print(y_2)
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
        # global i
        # global j
        global next_clicked
        """ handle button click event and output text from entry area"""
        input = self.entry_lane.get()
        print(input)
        self.create_entries_to_hold_lines(int(input))
        self.cur_line = 0
        self.submitButton.config(state = DISABLED)
        self.next_entries[0][0].config(state = NORMAL) # enable first next button
        self.line_entries[0][0].config(state = NORMAL) # enable first text entry
        next_clicked = True
        self.entry_lane.config(state = DISABLED)
        # self.imageCanvas.bind('<1>')

        # j += 1
        # if(i <= self.num_of_groups*self.num_of_lines_per_group):
           # self.next_entries[i][j].config(state = NORMAL)
           # j += 1
           # if j == self.num_of_lines_per_group:
               # i +=1
               # j = 0
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
        self.entry_lane.config(state = NORMAL)
        self.submitButton.config(state = NORMAL)
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File") # Read File

        if not self.check_video_file(self.filename):
            return

        self.filename_strvar.set(self.filename) # Display filename
        # self.filename_strvar = Entry(self, text = self.filename)
        # self.filename_strvar.grid(row = 13, column = 0)
        # self.filename_strvar.config(state = DISABLED)


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
# This is the main file that houses the Gui for the video display
# It has a search button that opens up the file directory to select a video
# Displays the video file name below
# The Submit button tracks the mouse click, but only in the pixels of the button, needs to be fixed

import os
import sys
import time
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import cv2
import numpy as np
from PIL import Image, ImageTk
from selenium import webdriver

from main import execute

desktop_path = os.path.expanduser("~/Desktop/")
chromedriver_path = os.path.join(desktop_path, "chromedriver")
vision_mater_path = os.path.join(desktop_path, "vision-master")

vid_x = 500  # Width of video
vid_y = 300  # Height of video


class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.title("Video File Opener Window")
        self.minsize(600, 500)  # Min size of window

        self.video_image_tk = None  # save the first frame of the video as an ImageTk obj
        self.video_file_loaded = False

        # Graphics window
        global vid_x
        global vid_y
        self.image_canvas = Canvas(self, width=vid_x, height=vid_y, bg='grey')
        self.image_canvas.grid(row=0, column=0, rowspan=10, columnspan=3)  # Spans 10 rows, 3 cols

        self.file_browser_label_frame = ttk.LabelFrame(self, text="Open A Video File")
        self.file_browser_label_frame.grid(row=11, column=0, padx=10, pady=20)
        self.create_file_dialog_button()

        # filename entry
        self.filename_strvar = StringVar()
        self.filename_entry = Entry(self, textvariable=self.filename_strvar, width=40)
        self.filename_entry.grid(row=13, column=0)

        # URL Enter Button
        self.enter_button = Button(self, command=self.enter_URL, text="Enter", state=NORMAL)
        self.enter_button.grid(row=13, column=1)

        # Reset
        self.reset_button = Button(self, command=self.reset, text="Reset", state=DISABLED)
        self.reset_button.grid(row=11, column=2)

        # Process
        self.process_button = Button(self, command=self.process, text="Process", state=DISABLED)
        self.process_button.grid(row=13, column=2)

        # Assigns num of lanes for data point entries
        self.label_lane = Label(self, text="Enter # of directions").grid(row=0, column=4)
        self.num_of_groups_strvar = StringVar()
        self.group_num_entry = Entry(self, textvariable=self.num_of_groups_strvar, state=DISABLED)
        self.group_num_entry.grid(row=1, column=4)

        self.num_of_groups = 0  # in case the reset button is clicke but this is not initialized

        """Create Submit Button"""
        self.submit_button = Button(self, command=self.submit_button_click, text="Submit", state=DISABLED)
        self.submit_button.grid(row=1, column=5)

        self.cur_click = 0


    def enter_URL(self):
        '''
        Takes in URL input to find link and then uses that for video
        '''
        self.enter_button.config(state=DISABLED)
        self.file_browser_button.config(state=DISABLED)  # Disable file browser button
        self.submit_button.config(state=NORMAL)
        self.group_num_entry.config(state=NORMAL)
        print(self.filename_strvar.get())  # debug Input UrL
        self.get_pic()


    def get_pic(self):
        website_name = self.filename_strvar.get()
        driver = webdriver.Chrome(executable_path=chromedriver_path)
        # https://nyctmc.org/google_popup.php?cid=975
        driver.get(website_name)
        strTime = self.get_current_time()
        image_folder = os.path.join(vision_mater_path, strTime)
        image_folder = os.path.join(vision_mater_path, strTime)
        if not os.path.isdir(image_folder):
            os.mkdir(image_folder)
        os.chdir(image_folder)

        # take multiple screenshots
        # figure out how many duplicates you need
        time.sleep(1)
        for x in range(5):
            time.sleep(1)
            driver.save_screenshot(str(time.time()) + ".png")

        driver.close()

        video_name = 'video.avi'

        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
        images.sort()

        # get the border from the image
        if not images:
            print(f"Error: NO screenshot has been captured from {website_name}")
            sys.exit(0)

        left, top, right, down = self.get_image_border(images[0])
        if left >= right or top >= down:
            print(
                f"Error: Incorrect border of the camera has been detected from image: {images[0]} of URL {website_name}")
            print(f"left: {left}, top: {top}, right: {right}, down: {down}")
            sys.exit(0)

        width = right - left
        height = down - top
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), 1, (width, height))

        for image in images:
            im = Image.open(image)
            crop = im.crop((left, top, right, down))
            crop.save(image)
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()
        # for image in images:
        #     os.remove(image)
        self.display()
        return strTime


    def display(self):
        self.filename = "video.avi"
        self.filename_strvar.set(self.filename)  # Display filename

        cap = cv2.VideoCapture(self.filename)  # Play video of file

        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)

        copy_of_image = img.copy()
        img = copy_of_image.resize((vid_x, vid_y))  # size of video
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_image_tk = imgtk  # keep a reference to the image, otherwise, it will be destroyed by garbage-collection
        self.image_canvas.create_image(0, 0, anchor=NW, image=imgtk)

        self.video_file_loaded = True

        cap.release()
        cv2.destroyAllWindows()


    def get_current_time(self):
        """
        Get current time in an easy to read format

        Returns
        -------
        current time, type: String
        Current time in format, "YYYY-MM-DD-HH-MM-SS-Microsec".
        """
        now = datetime.fromtimestamp(time.time())
        return now.strftime("%Y-%m-%d-%H-%M-%S-%f")


    def get_image_border(self, image_path):
        """
        Get the border of the camera from the image so as to crop the image.

        Parameters
        ----------
        image_path : String
        The absolute path of the image to be dealt with

        Returns
        -------
        left, top, right, down
            Two coordinates of the points, i.e., top left corner and bottom right cornor.
        """
        img = Image.open(image_path)
        img_array = np.asarray(img)

        height, width, _ = img_array.shape

        left = width  # the minimum x with non-white
        top = height  # the minimum y with non-white
        right = 0  # the largest x with non-white
        down = 0  # the largest y with non-white

        for row in range(height):
            for col in range(width):
                if img_array[row][col][0] != 255:
                    top = min(row, top)
                    left = min(col, left)
                    down = max(row, down)
                    right = max(col, right)

        return left, top, right, down


    def next_entry(self):
        """
        Finish inputing/pickin up for one line, and move to the next one if possible.
        """
        try:
            x_1, y_1, x_2, y_2 = [int(num.strip()) for num in self.entry_strvars[self.cur_group][self.cur_line].get().split(',')]
        except:
            return

        self.next_buttons[self.cur_group][self.cur_line].config(state=DISABLED)
        self.line_entries[self.cur_group][self.cur_line].config(state=DISABLED)

        self.image_canvas.create_line(x_1, y_1, x_2, y_2, fill="red", width=3)
        self.cur_line += 1

        if self.cur_line == self.num_of_lines_per_group:
            self.cur_line = 0
            self.cur_group += 1

            # finished the last group
            if self.cur_group >= self.num_of_groups:
                self.finish_lines_pickup()
                return

        self.next_buttons[self.cur_group][self.cur_line].config(state=NORMAL)
        self.line_entries[self.cur_group][self.cur_line].config(state=NORMAL)


    def process(self):
        '''
        should take in filename, # of lanes, # of lines per group,
        use those to iterate through each entry and collect points.
        Use point data with vid_x, vid_y size to get ratio
        Send to other video processing function for process.
        '''
        # Loop to create data locations
        start_row = 3
        start_col = 6
        direction_and_lines = []
        for group in range(self.num_of_groups):
            # collect the locations of lines
            lines = []
            for line_num in range(self.num_of_lines_per_group):
                one_line = [int(num.strip()) for num in self.entry_strvars[group][line_num].get().split(',')]
                one_line[0] /= vid_x
                one_line[1] /= vid_y
                one_line[2] /= vid_x
                one_line[3] /= vid_y
                lines.append(one_line)

            direction_and_lines.append({"direction": self.direction_vars[group].get(), "lines": lines})

        # TODO: add an entry to enter the output file name
        execute(os.getcwd(), self.filename, "result.txt", 0, direction_and_lines)


    def reset(self):
        ''' Reset will reset all the values on the screen.
        User will be able to choose a new file and start over
        File must be enabled
        Text boxes must be cleared and lanes must be destroyed
        '''
        self.filename = None
        self.filename_strvar.set('')  # debug should set display to empty
        self.file_browser_button.config(state=NORMAL)
        self.enter_button.config(state=NORMAL)

        # Destroy old entry boxes and next buttons
        for n in range(self.num_of_groups):
            for m in range(self.num_of_lines_per_group):
                self.next_buttons[n][m].grid_forget()
                self.line_entries[n][m].grid_remove()

            self.direction_opt_menus[n].grid_remove()

        self.submit_button.config(state=DISABLED)
        self.num_of_groups_strvar.set('')
        self.num_of_groups = 0

        self.cur_group = 0
        self.cur_line = 0

        self.image_canvas.delete("all")
        self.process_button.config(state=DISABLED)
        self.reset_button.config(state=DISABLED)
        self.file_browser_button.focus()


    def create_entries_to_hold_lines(self, num_of_groups):
        """
        Create entries to hold information about the lines that we will click/enter later.
        """
        self.num_of_groups = num_of_groups
        self.num_of_lines_per_group = 3
        self.num_of_clicks_per_line = 2
        self.entry_strvars = [[StringVar() for _ in range(self.num_of_lines_per_group)] for _ in
                              range(self.num_of_groups)]

        self.line_entries = []  # list of list of text widgets
        self.next_buttons = []  # list of list of buttons

        start_row = 3
        start_col = 4

        self.direction_opt_menus = []
        self.direction_vars = []
        option_list = ['up', 'down']
        for group in range(self.num_of_groups):
            cur_direction_var = StringVar()
            cur_direction_var.set('down')
            self.direction_vars.append(cur_direction_var)
            opt_menu = OptionMenu(self, cur_direction_var, *option_list)
            opt_menu.grid(row=start_row, column=start_col)
            self.direction_opt_menus.append(opt_menu)
            start_row += 1

        next_button_index = 0  # keeps track of next button
        for group in range(self.num_of_groups):
            line_entries_cur_group = []
            next_buttons_cur_group = []
            for row in range(self.num_of_lines_per_group):
                line_entry = Entry(self, textvariable=self.entry_strvars[group][row], state=DISABLED)

                # Create next button
                next_button_index += 1
                next_buttons_cur_group.append(
                    Button(self, text=("next" + str(next_button_index)), state=DISABLED, command=self.next_entry))
                cur_row = start_row + row + group * self.num_of_lines_per_group
                line_entry.grid(row=cur_row, column=start_col)
                next_buttons_cur_group[row].grid(row=cur_row, column=start_col + 1)
                line_entries_cur_group.append(line_entry)

            self.next_buttons.append(next_buttons_cur_group)
            self.line_entries.append(line_entries_cur_group)

        self.cur_group = 0
        self.cur_line = 0
        self.cur_click = 0


    def finish_lines_pickup(self):
        """a
        Signal to end / freeze canvas to stop allowing button clicks
        """
        self.image_canvas.unbind('<1>')  # unbind canvas
        self.process_button.config(state=NORMAL)


    def canvas_click_callback(self, event):
        """The call back function when the mouse clicks on the image canvas.
        It will fill out the entries one by one.
        Parameters
        ----------
        event : obj
            The click event.
        """
        print(f"self.cur_click: {self.cur_click}, x: {event.x}, y: {event.y}")

        if self.cur_click == 0:
            self.entry_strvars[self.cur_group][self.cur_line].set(f"{event.x}, {event.y}")
        else:
            _content = self.entry_strvars[self.cur_group][self.cur_line].get()
            _content += f", {event.x}, {event.y}"
            self.entry_strvars[self.cur_group][self.cur_line].set(_content)

        self.cur_click += 1

        if self.cur_click == self.num_of_clicks_per_line:
            self.cur_click = 0

            x_1, y_1, x_2, y_2 = [int(num.strip()) for num in self.entry_strvars[self.cur_group][self.cur_line].get().split(',')]
            self.canvas_id_one = self.image_canvas.create_line(x_1, y_1, x_2, y_2)
            self.image_canvas.after(3000, self.image_canvas.delete, self.canvas_id_one)  # Delete after 1 second

            if self.cur_line == self.num_of_lines_per_group:
                self.cur_line = 0
                self.cur_group += 1
                self.cur_group %= self.num_of_groups


    def submit_button_click(self, event=None):
        """ handle button click event and output text from entry area"""
        input = self.group_num_entry.get()
        if not input:
            return
        self.create_entries_to_hold_lines(int(input))
        self.cur_line = 0
        self.submit_button.config(state=DISABLED)
        self.next_buttons[0][0].config(state=NORMAL)  # enable first next button
        self.line_entries[0][0].config(state=NORMAL)  # enable first text entry
        self.group_num_entry.config(state=DISABLED)
        self.image_canvas.bind("<Button-1>", self.canvas_click_callback)


    def create_file_dialog_button(self):
        # Create Button to open file directory
        self.file_browser_button = ttk.Button(self.file_browser_label_frame, text="File Browser", command=self.file_browser_dialog)
        self.file_browser_button.grid(row=12, column=0)
        self.file_browser_button.focus()
        self.file_browser_button.bind('<Return>', self.file_browser_dialog)


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


    def file_browser_dialog(self, event=None):
        # Reads file to video and displays video in Gui
        global vid_x
        global vid_y

        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File")  # Read File

        self.update()  # fix the freeze issue on Mac in the File Selection popup

        if not self.check_video_file(self.filename):
            return

        # Disable buttons
        self.file_browser_button.config(state=DISABLED)
        self.enter_button.config(state=DISABLED)

        self.filename_strvar.set(self.filename)  # Display filename

        cap = cv2.VideoCapture(self.filename)  # Play video of file

        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)

        copy_of_image = img.copy()
        img = copy_of_image.resize((vid_x, vid_y))  # size of video
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_image_tk = imgtk  # keep a reference to the image, otherwise, it will be destroyed by garbage-collection
        self.image_canvas.create_image(0, 0, anchor=NW, image=imgtk)

        self.video_file_loaded = True

        cap.release()
        cv2.destroyAllWindows()

        self.reset_button.config(state=NORMAL)
        self.group_num_entry.config(state=NORMAL)
        self.submit_button.config(state=NORMAL)
        self.submit_button.bind('<Return>', self.submit_button_click)
        self.group_num_entry.focus_set()


# arg1 = sys.argv[1]

if __name__ == '__main__':
    root = Root()
    root.mainloop()

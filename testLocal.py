from main import execute
import os

desktop_path = os.path.expanduser("~/Desktop/")
vision_master_path = os.path.join(desktop_path, "vision-master")

file_name = input("Please enter the video name you want to process")


execute(vision_master_path, file_name, "result", 2)


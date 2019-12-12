import cv2
import numpy as np
import vehicles
import time
import os
from typing import List

debug = True

def execute(video_file: str, result_file: str, lines: List) -> None:
    """
    Process video and count the number of vehicles passing by

    Parameters
    ----------
    video_file : str,
        The abosulte path of the video file to be processed.
    result_file : str,
        The result file
    lines : List,
        The lines that are used to determine the moving direction of the vehicles in the video.
        Each element of the list is a dictionary, of which,
        Key is the moving direction, i.e., up or down;
        Values are three lines, and each line consists of 4 numbers (relative to width or height, range is [0, 1]),
        i.e., x_left, y_left, x_right, y_right
    """
    if debug:
        if lines:
            for direction_and_line in lines:
                print(direction_and_line['direction'])
                for line in direction_and_line['lines']:
                    print(line)

    cap = cv2.VideoCapture(video_file)

    # Find OpenCV version
    major_ver, _, _ = (cv2.__version__).split('.')
    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        if debug:
            print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if debug:
            print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Get width and height of video
    width = cap.get(3)
    height = cap.get(4)
    frame_area = height * width
    area_threshold = frame_area / 400  # the area threshold (minimum) for each single vehicle in the video;
    # TODO: should be adjustable for different camera
    # one option is to get the width of the lane
    # then use that as the baseline

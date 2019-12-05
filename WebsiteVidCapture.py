from selenium import webdriver
from PIL import Image
from main import execute
# from moviepy.editor import *
import time
import cv2
import os
import sys
from datetime import datetime
import numpy as np


desktop_path = os.path.expanduser("~/Desktop/")
chromedriver_path = os.path.join(desktop_path, "chromedriver")
vision_mater_path = os.path.join(desktop_path, "vision-master")

def get_current_time():
    """
    Get current time in an easy to read format

    Returns
    -------
    current time, type: String
        Current time in format, "YYYY-MM-DD-HH-MM-SS-Microsec".
    """
    now = datetime.fromtimestamp(time.time())
    return now.strftime("%Y-%m-%d-%H-%M-%S-%f")


def get_image_border(image_path):
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


def run(website_name):
    global desktop_path
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    # https://nyctmc.org/google_popup.php?cid=975
    driver.get(website_name)
    strTime = get_current_time()
    image_folder = os.path.join(vision_mater_path, strTime)
    if not os.path.isdir(image_folder):
        os.mkdir(image_folder)
    os.chdir(image_folder)

    # take multiple screenshots
    # figure out how many duplicates you need
    time.sleep(1)
    for x in range(10):
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

    left, top, right, down = get_image_border(images[0])
    if left >= right or top >= down:
        print(f"Error: Incorrect border of the camera has been detected from image: {images[0]} of URL {website_name}")
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

    return strTime


arg1 = sys.argv[1]

while True:
    strTime = run(arg1)
    image_folder = os.path.join(vision_mater_path, strTime)
    os.chdir(image_folder)
    tup = execute(image_folder, "video.avi", "result", 2)
    print("up: " + str(tup[0]) + " down: " + str(tup[-1]))

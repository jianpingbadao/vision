from selenium import webdriver
from PIL import Image
#from moviepy.editor import *
import time
import cv2
import os

def run(website_name):
	driver = webdriver.Chrome(executable_path='/Users/paulyp123/Desktop/chromedriver')
	#https://nyctmc.org/google_popup.php?cid=975
	driver.get(website_name)
	#driver.get('https://www.youtube.com/')
	strTime = str(time.time())
	image_folder = '/Users/paulyp123/Desktop/vision-master/' + strTime
	os.mkdir(image_folder)
	os.chdir(image_folder)

	for x in range(100):
		time.sleep(.1)
		driver.save_screenshot(str(time.time()) + ".png")

	driver.close()


	video_name = 'video.avi'

	images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
	images.sort()

	left = 848
	top = 127
	right = 1552
	down = 541
	width = right - left
	height = down - top
	#

	for image in images:
		im = Image.open(image)
		crop = im.crop((left, top, right, down))
		crop.save(image)
	time.sleep(5)
	video = cv2.VideoWriter(video_name, 0, 1, (width, height))
	video.write(cv2.imread(os.path.join(image_folder, image)))

	cv2.destroyAllWindows()
	video.release()
	for image in images:
		os.remove(image)

	return strTime
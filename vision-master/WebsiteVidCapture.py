"""
import webbrowser
import numpy as np 
import cv2 
from PIL import ImageGrab

webbrowser.open_new_tab("https://nyctmc.org/google_popup.php?cid=1257")

# four character code object for video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# video writer object
out = cv2.VideoWriter("output.avi", fourcc, 15.0, (1440, 900))

while True:
	# capture computer screen
	img = ImageGrab.grab()
	# convert image to numpy array
	img_np = np.array(img)
	# convert color space from BGR to RGB
	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
	# show image on OpenCV frame
	cv2.imshow("Screen", frame)
	# write frame to video writer
	out.write(frame)
  
	if cv2.waitKey(1) == 27:
		break

out.release()
cv2.destroyAllWindows()
conda install -c conda-forge python-chromedriver-binary 
"""
#/Users/paulyp123/Desktop/chromedriver 

from selenium import webdriver
from PIL import Image
#from moviepy.editor import *
import time
import cv2
import os


driver = webdriver.Chrome(executable_path='/Users/paulyp123/Desktop/chromedriver')

driver.get('https://nyctmc.org/google_popup.php?cid=975')
for x in range(10):
	time.sleep(.1)
	driver.save_screenshot(str(time.time()) + ".png")
	
driver.close()

image_folder = '/Users/paulyp123/Desktop/vision-master'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort()
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width,height))

for image in images:
	im = Image.open(image)
	#crop = im.crop((100,100,100,100))
	#crop.save(image)
	
	video.write(cv2.imread(os.path.join(image_folder, image)))


cv2.destroyAllWindows()
video.release()
for image in images:
	os.remove(image)




import cv2
import numpy as np
from matplotlib import pyplot as plt

#can also use "Car1.png" or "Car3.png"
img1 = cv2.imread("whitecar1.png")
img2 = cv2.imread("whitecar2.png")

hsv_test1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
hsv_test2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

#hsv_half_down = hsv_test1[hsv_test1.shape[0]//2:,:]

h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]

h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges

channels = [0, 1]

hist_test1 = cv2.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

hist_test2 = cv2.calcHist([hsv_test2], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(hist_test2, hist_test2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

result = cv2.compareHist(hist_test1, hist_test2, 0)

print(result)
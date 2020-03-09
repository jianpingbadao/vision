#make sure to import matplotlib

import cv2
import numpy as np
from matplotlib import pyplot as plt

#can also use "Car1.png" or "Car3.png"
img1 = cv2.imread("Car1.png")
img2 = cv2.imread("Car3.png")
b1, g1, r1 = cv2.split(img1)
b2, g2, r2 = cv2.split(img2)
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)


hist1 = cv2.calcHist([img1], [0,1,2], None, [8,8,8],[0,256,0,256,0,256])
hist1 = cv2.normalize(hist1,hist1).flatten()

hist2 = cv2.calcHist([img2], [0,1,2], None, [8,8,8],[0,256,0,256,0,256])
hist2 = cv2.normalize(hist2,hist2).flatten()

result = cv2.compareHist(hist1, hist2, 0)

print(result)
#hist2 = cv2.calcHist([img], [0,1,2], None, [8,8,8],[0,256,0,256,0,256])
#hist2 = cv2.normalize(hist,hist).flatten()

plt.hist(b1.ravel(), 256, [0, 256])
plt.hist(g1.ravel(), 256, [0, 256])
plt.hist(r1.ravel(), 256, [0, 256])

plt.hist(b2.ravel(), 256, [0, 256])
plt.hist(g2.ravel(), 256, [0, 256])
plt.hist(r2.ravel(), 256, [0, 256])

plt.show()
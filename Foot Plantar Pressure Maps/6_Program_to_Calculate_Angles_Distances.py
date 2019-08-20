###############
#Program finds the angle between 2 metatarsals
#Author: Jesu Kiran Spurgen
#Example: Between MT1-MT2, MT1-MT5
#
#Future work: Looping and creation of ROI
#
################


from pylab import *
from skimage import data
from skimage.viewer.canvastools import RectangleTool
from skimage.viewer import ImageViewer
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math as mt

im1 = cv2.imread("right.png", 0)
imgray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

im2 = cv2.imread("right.png")
imgray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

def get_rect_coord(extents):
    global viewer,coord_list
    coord_list.append(extents)

def get_ROI(im):
    global viewer,coord_list

    selecting=True
    while selecting:
        viewer = ImageViewer(im)
        coord_list = []
        rect_tool = RectangleTool(viewer, on_enter=get_rect_coord)
        print "Draw your selections, press ENTER to validate one and close the window when you are finished"
        viewer.show()
        finished=raw_input('Is the selection correct? [y]/n: ')
        if finished!='n':
            selecting=False
    return coord_list


######
###### Metatarsal of your choice 1
rect_coord1 = get_ROI(im1)
print "Rect coord1 is :", rect_coord1


coord1 = np.asarray(rect_coord1[0])

X1 = (coord1[0].astype(np.int32))
X2 = (coord1[1].astype(np.int32))


Y1 = (coord1[2].astype(np.int32))
Y2 = (coord1[3].astype(np.int32))

roi1 = im1[Y1:Y2, X1:X2]

edges1 = cv2.Canny(roi1, 40, 200)

contours1, hierarchy1 = cv2.findContours(edges1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierarchy1 = hierarchy1[0]


cv2.drawContours(roi1, contours1, -1, (0, 0, 0), -1)
ret1, thresh1 = cv2.threshold(im1, 0, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("A1.jpg", thresh1)

img = cv2.imread("A1.jpg",0)
h, w = img.shape
mat = []
for col in range(w):
    for row in range(h):
        if img[row, col] != 0:
            mat.append([col, row])
mat = np.array(mat).astype(np.float32)
m , e = cv2.PCACompute(mat, np.mean(mat, axis=0).reshape(1, -1))

centerA = tuple(m[0])
print(centerA)
endpointA = tuple(m[0] + e[0]*500)
print(endpointA)

endpoint11 = tuple(m[0] + e[0]*-500)
endpoint2 = tuple(m[0] + e[1]*50)

imgray =cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.circle(imgray, centerA, 5, (255, 0, 0))
cv2.line(imgray, centerA, endpointA, (0, 255, 0))
cv2.imwrite("Result1.jpg", imgray)
######
###### Metatarsal of your choice 2
rect_coord2 = get_ROI(im2)
print "Rect coord2 is :", rect_coord2
coord2 = np.asarray(rect_coord2[0])

X1 = (coord2[0].astype(np.int32))
X2 = (coord2[1].astype(np.int32))


Y1 = (coord2[2].astype(np.int32))
Y2 = (coord2[3].astype(np.int32))


roi2 = im2[Y1:Y2, X1:X2]

edges2 = cv2.Canny(roi2, 40, 200)

contours2, hierarchy2 = cv2.findContours(edges2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierarchy2 = hierarchy2[0]

cv2.drawContours(roi2, contours2, -1, (0, 0, 0), -1)


ret2, thresh2 = cv2.threshold(im2, 0, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("A2.jpg", thresh2)

######
img = cv2.imread("A2.jpg",0)
h, w = img.shape
mat = []
for col in range(w):
    for row in range(h):
        if img[row, col] != 0:
            mat.append([col, row])
mat = np.array(mat).astype(np.float32)
m , e = cv2.PCACompute(mat, np.mean(mat, axis=0).reshape(1, -1))

centerB = tuple(m[0])
print(centerB)
endpointB = tuple(m[0] + e[0]*500)
print(endpointB)

endpoint11 = tuple(m[0] + e[0]*-500)
endpoint2 = tuple(m[0] + e[1]*50)

imgray =cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.circle(imgray, centerB, 5, (255, 0, 0))
cv2.line(imgray, centerB, endpointB, (0, 255, 0))
cv2.imwrite("Result2.jpg", imgray)

#### Angle Measurement #####
############################


x1 = [centerA[0], endpointA[0]]
y1 = [centerA[1], endpointA[1]]

x2 = [centerB[0], endpointB[0]]
y2 = [centerB[1], endpointB[1]]

# Calculate the coefficients. This line answers the initial question.
coefficients1 = np.polyfit(x1, y1, 1)
coefficients2 = np.polyfit(x2, y2, 1)

# Print the findings
print 'a =', coefficients1[0]
print 'b =', coefficients2[0]

m1 = coefficients1[0]
m2 = coefficients2[0]

tan_theta = np.abs((m2 - m1)/(1+(m1*m2)))
#print(tan_theta)
theta =  mt.atan(tan_theta)

th= mt.degrees(theta)
print"The Angle between these 2 metatarsals is:", th

# -*- coding: utf-8 -*-
"""
First step in preprocessing stage. Thresholding an image removes the color
information.
Inputs: Original image
Outputs: Thresholded image.
Resources: http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        
"""
import cv2
import numpy as np
import math

def thresholdImage(img):
    grayImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#    retval, threshImg = cv2.threshold(grayImg,0,255,cv2.THRESH_OTSU) 
    threshImg = cv2.adaptiveThreshold(grayImg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,99,10)
    numWhite = cv2.countNonZero(threshImg)
    numBlack = threshImg.size - numWhite
    if (numWhite < numBlack): # invert the image if the background is mostly white
        return threshImg
    else:
        return 255-threshImg
    

def rotate90_counter_clockwise(img):
    timg = cv2.transpose(img)
    timg = cv2.flip(timg,0) 
    return timg
    
def distancePts(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)
        
    
img = cv2.imread(r'C:\Users\Mihailo\Documents\Embedded Systems\RPi_Translator\test_images\test7_eng.jpg')

# Rotate counter clockwise by 90 degrees
img = rotate90_counter_clockwise(img)

# Apply adaptive threshold
threshImg = thresholdImage(img) 
#cv2.namedWindow('threshImg', cv2.WINDOW_NORMAL)
#cv2.imshow('threshImg',threshImg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Apply dilation to join the gaps
# http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
# http://docs.opencv.org/master/d1/dee/tutorial_moprh_lines_detection.html
binaryImg = (threshImg==255).astype(np.uint8)
kernel = np.zeros([5,5]) #horizontal structuring element
kernel[2,:] = np.ones([1,5])
kernel = kernel.astype(np.uint8)
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
dilateImg = cv2.dilate(binaryImg,kernel,iterations=4)
dilateImg = dilateImg*255
#cv2.namedWindow('dilateImg', cv2.WINDOW_NORMAL)
#cv2.imshow('dilateImg',dilateImg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Find the contours to get blocks that correspond to words
# https://opencvpython.blogspot.com/2012/06/hi-this-article-is-tutorial-which-try.html
# http://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html
dilateImg_copy = dilateImg.copy()
im2, contours, hierarchy = cv2.findContours(dilateImg_copy,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
imgContours = img.copy()
imgContours = cv2.drawContours(imgContours,contours,-1,(0,255,0),3)
#cv2.namedWindow('imgContours', cv2.WINDOW_NORMAL)
#cv2.imshow('imgContours',imgContours)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# For each contour, find the bounding rectangle and draw it
# http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
fixedPt_x = 670
fixedPt_y = 575
minDistance = img.shape[0]
for contour in contours:
#    x,y,w,h = cv2.boundingRect(contour)
#    if (w>10) and (h>20): # filter out small boxes created from noise
#        distanceFromFixed = distancePts(fixedPt_x,fixedPt_y,x+w/2,y+h/2)
#        if (distanceFromFixed < minDistance):
#            minDistance = distanceFromFixed
#            minContour = contour
    center,dimensions,theta = cv2.minAreaRect(contour)
    if (dimensions[0]>10) and (dimensions[1]>20): # filter out small boxes created from noise
        distanceFromFixed = distancePts(fixedPt_x,fixedPt_y,center[0],center[1])
        if (distanceFromFixed < minDistance):
            minDistance = distanceFromFixed
            minContour = contour

rotateImg = threshImg.copy()
            
x,y,w,h = cv2.boundingRect(minContour)
img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

center,dimensions,theta = cv2.minAreaRect(minContour)
if(dimensions[0] < dimensions[1]):
    w = dimensions[1]
    h = dimensions[0]
    theta = theta+90
box = cv2.boxPoints((center,(w,h),theta))
box = np.int0(box)
cv2.drawContours(img,[box],0,(0,0,255),2)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

rotateMatrix = cv2.getRotationMatrix2D(center,theta,1.0)
rotateImg = cv2.warpAffine(threshImg, rotateMatrix, (rotateImg.shape[0], rotateImg.shape[0]))
#cv2.namedWindow('rotateImg', cv2.WINDOW_NORMAL)
#cv2.imshow('rotateImg',rotateImg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

wordSegmented = cv2.getRectSubPix(rotateImg, (np.int0(w),np.int0(h)), center)
wordSegmented = cv2.copyMakeBorder(wordSegmented,10,10,10,10,cv2.BORDER_CONSTANT,0)
cv2.namedWindow('wordSegmented', cv2.WINDOW_NORMAL)
cv2.imshow('wordSegmented',wordSegmented)
cv2.waitKey(0)
cv2.destroyAllWindows()




#ix,iy = -1,-1
## mouse callback function
#def draw_circle(event,x,y,flags,param):
#    global ix,iy
#    if event == cv2.EVENT_LBUTTONDBLCLK:
#        ix,iy = x,y
#        print(ix,iy)
#
## Create a black image, a window and bind the function to window
#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.setMouseCallback('image',draw_circle)
#
#while(1):
#    cv2.imshow('image',img)
#    k = cv2.waitKey(0) & 0xFF
#    if k == 27:
#        break
#cv2.destroyAllWindows()
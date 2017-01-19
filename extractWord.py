# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 22:31:03 2017

@author: Mihailo
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

def extractWord(img):
    # Rotate counter clockwise by 90 degrees
    img = rotate90_counter_clockwise(img)
    
    # Apply adaptive threshold
    threshImg = thresholdImage(img) 
    
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
    
    # Find the contours to get blocks that correspond to words
    # https://opencvpython.blogspot.com/2012/06/hi-this-article-is-tutorial-which-try.html
    # http://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html
    dilateImg_copy = dilateImg.copy()
    im2, contours, hierarchy = cv2.findContours(dilateImg_copy,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    imgContours = img.copy()
    imgContours = cv2.drawContours(imgContours,contours,-1,(0,255,0),3)
    
    # For each contour, find the bounding rectangle and draw it
    # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
    fixedPt_x = 670
    fixedPt_y = 575
    minDistance = img.shape[0]
    for contour in contours:
        center,dimensions,theta = cv2.minAreaRect(contour)
        if (dimensions[0]>10) and (dimensions[1]>20): # filter out small boxes created from noise
            distanceFromFixed = distancePts(fixedPt_x,fixedPt_y,center[0],center[1])
            if (distanceFromFixed < minDistance):
                minDistance = distanceFromFixed
                minContour = contour
    
    center,dimensions,theta = cv2.minAreaRect(minContour)
    if(dimensions[0] < dimensions[1]):
        w = dimensions[1]
        h = dimensions[0]
        theta = theta+90
    else:
        w = dimensions[0]
        h = dimensions[1]
    box = cv2.boxPoints((center,(w,h),theta))
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),2)
    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(r'/home/pi/Documents/RPi_Translator/images/wordSegmented.jpg',img)
    
    rotateImg = threshImg.copy()    
    rotateMatrix = cv2.getRotationMatrix2D(center,theta,1.0)
    rotateImg = cv2.warpAffine(threshImg, rotateMatrix, (rotateImg.shape[0], rotateImg.shape[0]))
    
    wordSegmented = cv2.getRectSubPix(rotateImg, (np.int0(w),np.int0(h)), center)
    wordSegmented = cv2.copyMakeBorder(wordSegmented,10,10,10,10,cv2.BORDER_CONSTANT,0)
    wordSegmented = 255-wordSegmented
    
    return wordSegmented

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 22:45:15 2017

@author: Mihailo
"""
import cv2
import numpy as np
from PIL import Image
import regex as re
from picamera import PiCamera
from picamera.array import PiRGBArray
from gpiozero import Button
from time import sleep
import requests
import xml.etree.ElementTree as ET # https://docs.python.org/3/library/xml.etree.elementtree.html
import os
from extractWord import extractWord
import tesserocr
from mstranslator import Translator

### initialization
##button = Button(17)
##camera = PiCamera()
##rawCapture = PiRGBArray(camera)
##
### choose operation mode
opMode = input('Select operation mode: [0 for Dictionary] [1 for Translator] \n')
if(opMode == 0):
    opMode = 'English Dictionary'
    language = 'eng'
else:
    opMode = 'Translator'
    language = 'srp_latn'

##
### start camera
##camera.start_preview()
##sleep(0.1) # camera warm-up time
##button.wait_for_press()
##camera.capture(rawCapture, format="bgr")
##camera.stop_preview()
##img = rawCapture.array

# word segmentation
##img = cv2.imread(r'/home/pi/Documents/RPi_Translator/test_images/test1_eng.jpg')
##word = extractWord(img)
##cv2.namedWindow('word', cv2.WINDOW_NORMAL)
##cv2.imshow('word',word)
##cv2.waitKey(0)
##cv2.destroyAllWindows()
##cv2.imwrite('word.jpg',word)

# tesseract OCR
textOCR = tesserocr.file_to_text(r'/home/pi/Documents/RPi_Translator/images/word_srb.jpg', lang=language)
textOCR = ''.join(ch for ch in textOCR if ch.isalnum()) #remove special characters (e.g. /n) and punctuation
print("Detected word is: " + textOCR)

# Merriam-Webster API
if(opMode == 'English Dictionary'):
    api_key = os.environ['MW_COLLEGIATE_DICTIONARY_KEY']
    dictCollegiateURL = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"
    apiRequestURL = dictCollegiateURL + textOCR + "?key=" + api_key

    r = requests.get(apiRequestURL)
    tree = ET.ElementTree(ET.fromstring(r.text))
    definition_list = []
    for definition in tree.iter('dt'): # extract defintions from API response
        definition_list.append("".join(definition.itertext()))

    if(len(definition_list)):
        print("Definition(s):\n") 
        for definiton in definition_list:
            print(definiton + "\n")
    else:
        print("No definition found for " + word + ".\n")

# Microsoft Translate API
if(opMode == 'Translator'):
    translator = Translator(os.environ['MICROSOFT_AZURE_COG_SERV_KEY'])
    print("Translating " + textOCR + " to English:")
    print(translator.translate(textOCR, lang_from='sr-Latn', lang_to='en'))

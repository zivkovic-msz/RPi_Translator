from picamera import PiCamera
from time import sleep
from gpiozero import Button

button = Button(17)
camera = PiCamera()

camera.start_preview()
button.wait_for_press()
camera.capture('/home/pi/Documents/RPi_Translator/test_images/test7_eng.jpg')
camera.stop_preview()

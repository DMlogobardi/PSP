from gpiozero import Button
import RPi.GPIO as GPIO
import time
import os
import motore

GPIO.setmode(GPIO.BCM)
pin = 3
GPIO.setup(pin,GPIO.IN)

def MOTION(pin):
    print("MOVIMENTO")
    motore.start()
    

try:
    GPIO.add_event_detect(pin,GPIO.RISING,callback=MOTION)
    while 1:
        time.sleep(0.1)
except KeyboardInterrupt:
    print ("QUIT")
    
GPIO.cleanup()
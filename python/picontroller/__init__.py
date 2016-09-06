import RPi.GPIO as GPIO

initialized = False
def ioinit():
    global initialized 
    if not initialized:
        GPIO.setmode(GPIO.BCM)
        initialized = True

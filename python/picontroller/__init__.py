
initialized = False
def ioinit():
    global initialized 
    if not initialized:
    	import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        initialized = True

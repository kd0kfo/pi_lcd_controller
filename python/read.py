#!/usr/bin/env python

from sys import stderr, argv
import RPi.GPIO as GPIO
from time import sleep

LED_OFF = GPIO.HIGH
LED_ON = GPIO.LOW

LEDS = {'green': 4, 'yellow': 5}
BUTTONS = {0: 6}


def led_on(led):
    GPIO.output(LEDS[led], LED_ON)


def led_off(led):
    GPIO.output(LEDS[led], LED_OFF)


def led_state(led, state):
    if state:
        led_on(led)
    else:
        led_off(led)

# IO Setup
GPIO.setmode(GPIO.BCM)
for led in LEDS:
    GPIO.setup(LEDS[led], GPIO.OUT)
    led_off(led)
for button in BUTTONS:
    GPIO.setup(BUTTONS[button], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
# If run alone.
if __name__ == "__main__":
    import signal

    def sighandler(signum, frame):
	led_on('green')
	led_on('yellow')
        print("Shutting down")
	sleep(1)
	led_off('green')
	led_off('yellow')
	exit(0)

    signal.signal(signal.SIGTERM, sighandler)
    led_on('green')
    sleep(1)
    led_on('yellow')
    sleep(1)
    led_off('green')
    led_off('yellow')
    while True:
        btn6 = GPIO.input(6)
        led_state('green', btn6) 
        sleep(0.5)

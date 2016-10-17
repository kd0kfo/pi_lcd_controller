#!/usr/bin/env python

from sys import stderr
import RPi.GPIO as GPIO
from time import sleep
from picontroller import ioinit

LED_OFF = GPIO.HIGH
LED_ON = GPIO.LOW
BUTTON_POLL_PERIOD = 0.5

LEDS = {'green': 4, 'yellow': 5}
BUTTONS = {0: 6, 1: 12, 2: 13, 3: 16, 4: 17, 5: 18}

def btn_state(button):
    return GPIO.input(BUTTONS[button])


def btn_state_json():
    import json
    state = dict((int(button), btn_state(button)) for button in BUTTONS)
    return json.dumps(state)


def encoded_state():
    state = 0
    for button in BUTTONS:
        if btn_state(button):
            state |= 1 << button
    return state

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
ioinit()
for led in LEDS:
    GPIO.setup(LEDS[led], GPIO.OUT)
    led_off(led)
for button in BUTTONS:
    GPIO.setup(BUTTONS[button], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
# If run alone.
if __name__ == "__main__":
    import signal
    from sys import argv
    
    driver = open(argv[1], "w")


    def sighandler(signum, frame):
        led_on('green')
        led_on('yellow')
        print("Shutting down")
        sleep(1)
        led_off('green')
        led_off('yellow')
        driver.close()
        exit(0)

    led_on('green')
    sleep(1)
    led_on('yellow')
    sleep(1)
    led_off('green')
    led_off('yellow')
    while True:
        led_state('green', 0)
        for btn in BUTTONS:
            if btn_state(btn):
	            led_on('green')
        driver.write(chr(encoded_state()))
        driver.flush() # need for python to do the write immediately
        sleep(0.1)

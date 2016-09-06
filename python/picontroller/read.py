#!/usr/bin/env python

from sys import stderr, argv
import RPi.GPIO as GPIO
from time import sleep
from picontroller import ioinit

LED_OFF = GPIO.HIGH
LED_ON = GPIO.LOW

LEDS = {'green': 4, 'yellow': 5}
BUTTONS = {0: 6, 1: 12, 2: 13}

def btn_state(button):
    return GPIO.input(BUTTONS[button])


def btn_state_json():
    import json
    state = dict((int(button), btn_state(button)) for button in BUTTONS)
    return json.dumps(state)


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
    import socket

    def sighandler(signum, frame):
        led_on('green')
        led_on('yellow')
        print("Shutting down")
        sleep(1)
        led_off('green')
        led_off('yellow')
        exit(0)

    IP = '127.0.0.1'
    PORT = 9191
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    signal.signal(signal.SIGTERM, sighandler)
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
        sock.sendto(btn_state_json(), (IP, PORT))
        sleep(0.5)

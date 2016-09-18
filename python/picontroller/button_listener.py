#!/usr/bin/env python

from time import sleep


class ButtonListener():
    """
    Service that polls the button status device and calls a 
    callback funtion for each button pressed.

    Callback function should return a boolean to show whether 
    or not the listening should continue.
    """
    def __init__(self, button_callback, device_filename="/dev/buttons", num_buttons=8):
        self.button_callback = button_callback
        self.button_device = open(device_filename, "r")
        self.num_buttons = num_buttons
        self.last_state = {"0": 0}

    def listen(self):
        while True:
            raw_state = [ord(ch) for ch in self.button_device.read(self.num_buttons)]
            state = dict(zip(range(0, len(raw_state)), raw_state))
            for (button, isup) in state.iteritems():
                if isup:
                    state[button] = 1
                else:
                    state[button] = 0
                if not isup and button in self.last_state and self.last_state[button]:
                    if not self.button_callback(button):
                        return
            self.last_state = state
            sleep(0.5)


if __name__ == "__main__":
    def print_button(button):
        print("Button %s pressed" % button)
        return True
    service = ButtonListener(print_button)
    service.listen()	

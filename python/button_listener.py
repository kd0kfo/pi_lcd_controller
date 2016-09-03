#!/usr/bin/env python

import socket
import json
from time import sleep


IP = '127.0.0.1'
PORT = 9191


class ButtonListener():
    """
    Service that listens to Button UDP messages and calls a 
    callback funtion for each button pressed.

    Callback function should return a boolean to show whether 
    or not the listening should continue.
    """
    def __init__(self, button_callback, ip=IP, port=PORT):
        self.button_callback = button_callback
        self.ip = ip
        self.port = port
        self.last_state = {"0":0}

    def listen(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.ip, self.port))
            state = json.loads(sock.recv(128))
            for (button, isup) in state.iteritems():
                if not isup and button in self.last_state and self.last_state[button]:
                    if not self.button_callback(button):
                        return
            self.last_state = state
            sock.close()
            #sleep(0.5)


if __name__ == "__main__":
    def print_button(button):
        print("Button %s pressed" % button)
        return True
    service = ButtonListener(print_button)
    service.listen()	

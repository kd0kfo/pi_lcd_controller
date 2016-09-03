#!/usr/bin/env python

import socket
import json
from time import sleep


IP = '127.0.0.1'
PORT = 9191

last_state = {"0":0}

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    state = json.loads(sock.recv(128))
    for (button, isup) in state.iteritems():
        if not isup and button in last_state and last_state[button]:
            print("Button %s pressed" % button)
    last_state = state
    sock.close()
    #sleep(0.5)

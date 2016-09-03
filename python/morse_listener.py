#!/usr/bin/env python

from sys import argv
import morse
import button_listener

BTN_FUNCT = '0'
BTN_DIT = '1'
BTN_DAH = '2'

out = open(argv[1], "w")
mcode = morse.MorseEncoder()

def morse_encode(button):
    global mcode
    global out
    global argv
    if button == BTN_FUNCT:
        out.write(mcode.char())
        out.close()
        out = open(argv[1], "w")
        mcode.reset()
    elif button == BTN_DIT:
        mcode.add_dit()
    elif button == BTN_DAH:
        mcode.add_dah()


service = button_listener.ButtonListener(morse_encode)
service.listen()

#!/usr/bin/env python
#
# LCD Driver
#
# TODO: refactor ugly functions with gross globals to class.

from sys import stderr, argv
from RPLCD import CharLCD
from time import sleep

COLS = 8
ROWS = 2
BUFFER_SIZE = COLS * ROWS
READ_LIMIT = 1024
lcdbuffer = u""

smiley = (
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b10001,
    0b10001,
    0b01010,
    0b00100,
    )

lcd = CharLCD(cols=COLS, rows=ROWS)
lcd.create_char(0, smiley)


def clear_screen():
    global lcdbuffer
    lcd.clear()
    lcdbuffer = u""

def write_text(text):
    global lcdbuffer
    global lcd

    if not text:
        return

    while text and text[0] == "\x7f":
        lcdbuffer = lcdbuffer[:-1]
        text = text[1:]
    if text and text[0] == "\x0C":
        clear_screen()
        return

    lcdbuffer += text.replace(u"\x01", unichr(0))
    lcd.clear()
    lcd.write_string(lcdbuffer[:BUFFER_SIZE])
    while len(lcdbuffer) > BUFFER_SIZE:
        sleep(1)
        lcdbuffer = lcdbuffer[1:]
        lcd.clear()
        lcd.write_string(lcdbuffer[:BUFFER_SIZE])


if __name__ == "__main__":
    if len(argv) < 2:
        print("Missing FIFO path")
        exit(1)

    fifo_path = argv[1]

    if fifo_path.lower() == "--clear":
        exit()

    if len(argv) > 3 and argv[2] == "--start_message":
        write_text(" ".join(argv[3:]))

    while True:
        with open(fifo_path, "r") as fifo:
            text = fifo.read(READ_LIMIT).decode("latin1")
            while text and text[-1] == "\n":
                text = text[:-1]
            write_text(text)

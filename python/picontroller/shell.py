#!/usr/bin/env python

from sys import stdout
from morse import MorseEncoder
from write import write_text, clear_screen
from button_listener import ButtonListener

BTN_FUNCT = 0
BTN_DIT = 1
BTN_DAH = 2
BTN_SPACE = 3
BTN_RTN = 4


class Shell():
    def __init__(self, debug=False):
        self.debug = debug
        self.word_buffer = ""
        self.mcode = MorseEncoder()
        self.commands = {}

    def output(self, msg):
        if self.debug:
            stdout.write(msg)
        write_text(msg)

    def morse_word_reader(self, button):
        if button == BTN_RTN:
            self.word_buffer += '\n'
            return False
        elif button == BTN_FUNCT:
            self.word_buffer += self.mcode.char()
            self.mcode.reset()
            if self.word_buffer[-1] == '\n':
                return False
            self.output(self.word_buffer[-1])
        elif button == BTN_DIT:
            self.mcode.add_dit()
        elif button == BTN_DAH:
            self.mcode.add_dah()
        elif button == BTN_SPACE:
            self.word_buffer += ' '
            self.output(self.word_buffer[-1])
        return True

    def readline(self):
        self.word_buffer = ""
        self.mcode.reset()
        service = ButtonListener(self.morse_word_reader)
        service.listen() # this is a blocking call
        return self.word_buffer

    def run(self, commands):
        self.commands = commands
        if self.debug:
            print("Running with commands: %s" % ", ".join("'%s'" % key for key in commands.keys()))
        while True:
            self.output(">")
            try:
                line = self.readline().split()
                (command, args) = line[0], line[1:]
            except Exception as e:
                stdout.write("Error:\n")
                stdout.write(repr(e))
                stdout.write("\n")
                continue
		    
            # For prototyping.
            # TODO: fill in with commands
            clear_screen()
            if command in commands:
                try:
                    response = commands[command](*args)  
                except Exception as e:
                    response = "ERROR!"
                    stdout.write(repr(e))
                    stdout.write("\n")
                if response:
                    self.output(response)
            else:
                self.output("Unknown '%s'" % command)
            sleep(2)
            clear_screen()
            stdout.write("\n")


def exit_shell():
    clear_screen()
    write_text("Bye!")
    exit(0)


def echo(*msg):
    if msg:
        shell.output(" ".join(msg))

def demo_morse():
    from time import sleep
    from morse import morse_to_ditdat, char_to_morse
    for ch in range(ord('a'), ord('z')+1) + range(ord('0'), ord('9')+1):
        clear_screen()
        curr = chr(ch)
        shell.output("%s\n%s" % (curr, morse_to_ditdat(char_to_morse(ch))))
        sleep(1)


def ls(path="."):
    from os import listdir
    shell.output(" ".join(listdir(path)))


def help(*args):
    shell.output("Commands are %s" % " ".join(shell.commands.keys()))


DEFAULT_COMMANDS = {'test': lambda: "Works!",
    'date': lambda:strftime("%m/%d/%y%H:%M:%S", localtime()),
    'demo': demo_morse,
    'exit': exit_shell,
    'echo': echo,
    'help': help,
    'ls': ls,
    'date': lambda:strftime("%m/%d/%y%H:%M:%S", localtime()),
}

if __name__ == "__main__":
    from time import sleep, localtime, strftime

    shell = Shell(debug=True)

    shell.run(DEFAULT_COMMANDS)

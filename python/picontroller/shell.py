#!/usr/bin/env python

from sys import stdout
from morse import MorseFile
from write import write_text, clear_screen
from button_listener import ButtonListener


class Shell():
    def __init__(self, debug=False):
        self.debug = debug
        self.commands = {}
        self.prompt = "> "
        self.use_morse()

    def use_morse(self):
        self.infile = MorseFile(read_callback=self.output)
        self.prompt = "> "

    def use_keys(self):
        from sys import stdin
        self.infile = stdin
        self.prompt = "? "

    def get_int(self):
        from sys import stdin
        from number_listener import NumberListener
        retval = None
        if self.infile == stdin:
            line = self.readline()
            retval = int(line.strip())
        else:
            numbers = NumberListener(read_callback=self.output)
            numbers.listen()
            retval = numbers.get_int()

        return retval

    def output(self, msg):
        if self.debug:
            stdout.write(msg)
        write_text(msg)

    def clear(self):
        clear_screen()

    def readline(self):
        return self.infile.readline().strip()
    
    def run(self, commands):
        from time import sleep
        self.commands = commands
        if self.debug:
            print("Running with commands: %s" % ", ".join("'%s'" % key for key in commands.keys()))
        while True:
            self.output(self.prompt)
            try:
                line = self.readline().split()
                (command, args) = line[0], line[1:]
            except Exception as e:
                stdout.write("Error:\n")
                stdout.write(repr(e))
                stdout.write("\n")
                continue
		    
            clear_screen()
            if command in commands:
                try:
                    response = commands[command](self, *args)  
                except Exception as e:
                    response = "ERROR!"
                    stdout.write("%s\n" % e)
                if response:
                    self.output(response)
            else:
                self.output("Unknown '%s'" % command)
            sleep(2)
            clear_screen()
            stdout.write("\n")


def exit_shell(theshell):
    theshell.clear()
    theshell.output("Bye!")
    exit(0)


def echo(theshell, *msg):
    if msg:
        theshell.output(" ".join(msg))

def demo_morse(theshell):
    from time import sleep
    from morse import morse_to_ditdat, char_to_morse
    for ch in range(ord('a'), ord('z')+1) + range(ord('0'), ord('9')+1):
        theshell.clear()
        curr = chr(ch)
        theshell.output("%s\n%s" % (curr, morse_to_ditdat(char_to_morse(ch))))
        sleep(1)


def number_demo(theshell):
    from sys import stdout
    theshell.output("Enter number: ")
    val = theshell.get_int()
    clear_screen()
    theshell.output("You entered %s" % val)


def ls(theshell, path="."):
    from os import listdir
    theshell.output(" ".join(listdir(path)))


def help_command(theshell, *args):
    theshell.output("Commands are %s" % " ".join(theshell.commands.keys()))


def show_date(theshell, *args):
    from time import strftime, localtime
    return strftime("%m/%d/%y%H:%M:%S", localtime())

DEFAULT_COMMANDS = {'test': lambda theshell: "Works!",
    'date': show_date,
    'demo': demo_morse,
    'exit': exit_shell,
    'echo': echo,
    'help': help_command,
    'int': number_demo,
    'ls': ls,
}

if __name__ == "__main__":
    from time import sleep, localtime, strftime

    shell = Shell(debug=True)

    shell.run(DEFAULT_COMMANDS)

#!/usr/bin/env python

from sys import stdout
import morse
import read
from write import write_text, clear_screen
from button_listener import ButtonListener


class Shell():
	def __init__(self, debug=False):
		self.debug = False
		self.word_buffer = ""
		self.mcode = MorseEncoder()

	def output(self, msg):
		if self.debug:
			stdout.write(msg)
		write_text(msg)

	def morse_word_reader(self, button):
		from lcdconfig import BTN_FUNCT, BTN_DIT, BTN_DAH
	    if button == BTN_FUNCT:
	        self.word_buffer += self.mcode.char()
	        self.mcode.reset()
	        if word_buffer[-1] == '\n':
	        	return False
	        output(self.word_buffer[-1])
	    elif button == BTN_DIT:
	        self.mcode.add_dit()
	    elif button == BTN_DAH:
	        self.mcode.add_dah()
	    return True

	def readline(self):
		self.mcode.reset()
		service = button_listener.ButtonListener(self.morse_word_reader)
		service.listen() # this is a blocking call
		return self.word_buffer

if __name__ == "__main__":
	shell = Shell(debug=True)
	while True:
		shell.output("> ")
		try:
			command = shell.readline()
		except Exception as e:
			stdout.write("Error:\n")
			stdout.write(repr(e))
			stdout.write("\n")
			continue
		shell.output(command)
		
		# For prototyping.
		# TODO: fill in with commands
		sleep(2)
		clear_screen()
		stdout.write("\n")



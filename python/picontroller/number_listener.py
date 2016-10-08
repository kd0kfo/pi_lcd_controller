#!/usr/bin/env python

import button_listener

BUTTON_SHIFT = 0

class InvalidNumber(Exception):
	def __init__(self, bad_number):
		self.bad_number = bad_number

	def __str__(self):
		return repr(self.bad_number)

class NumberListener(button_listener.ButtonListener):
	def __init__(self, *args, **kw):
		args = tuple([self.number_callback] + list(args))
		button_listener.ButtonListener.__init__(self, *args, **kw)
		self.shift_pressed = False
		self.number_string = ""

	def get_int(self):
		if not self.number_string.isdigit():
			raise InvalidNumber(self.number_string())
		return int(self.number_string)


	def number_callback(self, button):
		if button == BUTTON_SHIFT:
			if self.shift_pressed:
				self.shift_pressed = False
				return False
			self.shift_pressed = True
			return True
		currval = button
		if self.shift_pressed:
			currval = (5 + currval) % 10
		self.shift_pressed = False
		self.number_string += "%d" % currval
		return True



if __name__ == "__main__":
	listener = NumberListener()
	listener.listen()
	print(listener.get_int())

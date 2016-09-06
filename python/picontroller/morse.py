#!/usr/bin/env python

class UnencodableCharacter(Exception):
	def __init__(self, ch):
		self.ch = ch

	def __str__(self):
		return repr(self.ch)


class EncodingOverflow(Exception):
	def __init__(self):
		self.msg = "Exceeded character size"

	def __str__(self):
		return self.msg

class InvalidEncoding(Exception):
	def __init__(self, encoding):
		self.encoding = encoding

	def __str__(self):
		return "0x%x" % self.encoding


LENGTH_MASK = 7
MAX_ENCODED_LENGTH = 5 # Only 5 characters allowed
MORSE_MSB = 0x80
MORSE_LSB = 0x08
MORSE_WHOLE_MASK = 0xff
ENCODING = { 0b01000010: 'a',
    0b10000100: 'b',
    0b10100100: 'c',
    0b10000011: 'd',
    0b00000001: 'e',
    0b00100100: 'f',
    0b11000011: 'g',
    0b00000100: 'h',
    0b00000010: 'i',
    0b01110100: 'j',
    0b10100011: 'k',
    0b01000100: 'l',
    0b11000010: 'm',
    0b10000010: 'n',
    0b11100011: 'o',
    0b01100100: 'p',
    0b11010100: 'q',
    0b01000011: 'r',
    0b00000011: 's',
    0b10000001: 't',
    0b00100011: 'u',
    0b00010100: 'v',
    0b01100011: 'w',
    0b10010100: 'x',
    0b10110100: 'y',
    0b11000100: 'z',
    0b11111101: '0',
    0b01111101: '1',
    0b00111101: '2',
    0b00011101: '3',
    0b00001101: '4',
    0b00000101: '5',
    0b10000101: '6',
    0b11000101: '7',
    0b11100101: '8',
    0b11110101: '9',
    0b00101101: '\x00',
    0b00100101: '\x0C',
    0b10101101: '\n',
}


class MorseEncoder():
	def __init__(self):
		self.reset()

	def reset(self):
		self.morse = 0
		self.currbit = MORSE_MSB  

	def size(self):
		return self.morse & LENGTH_MASK

	def shift_morse(self):
		if (self.morse & LENGTH_MASK) >= MAX_ENCODED_LENGTH or self.currbit < MORSE_LSB:
			raise EncodingOverflow()
		length = (self.morse & LENGTH_MASK) + 1
		self.morse = self.morse & ~LENGTH_MASK
		self.morse = (self.morse | length) & MORSE_WHOLE_MASK
		self.currbit >>= 1

	def add_dit(self):
		self.shift_morse()

	def add_dah(self):
		self.morse = self.morse | self.currbit
		self.shift_morse()


	def char(self):
		if not self.morse in ENCODING:
			raise InvalidEncoding(self.morse)
		
		return ENCODING[self.morse]
		


def char_to_morse(ch):
	for (encoding, char) in ENCODING.iteritems():
		if ord(char) == ch:
			return encoding
	raise UnencodableCharacter(ch)

def word_to_morse(word):
	return (char_to_morse(ord(ch)) for ch in word)


def morse_to_ditdat(morse):
	morselen = morse & LENGTH_MASK
	morse_code = ""
	while morselen:
		if morse & MORSE_MSB:
			morse_code += "-"
		else:
			morse_code += "."
		morselen -= 1
		morse = (morse << 1) & MORSE_WHOLE_MASK
	return morse_code


if __name__ == "__main__":
	from sys import argv, stdout
	if argv[1][0] in ('-','.'):
		morse = MorseEncoder()
		for word in argv[1:]:
			for ch in word:
				if ch == '-':
					morse.add_dah()
				else:
					morse.add_dit()
			stdout.write(morse.char())
			morse.reset()
	else:
		for word in argv[1:]:
			stdout.write(" ".join(morse_to_ditdat(ch) for ch in  word_to_morse(word)))
			stdout.write(" ")
	print("")

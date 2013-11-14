class RobotEncryption(object):
	"""
	A class for encrypting / decrypting messages.
	"""
	def __init__(self, offset=40):
		self.offset = offset
		self.dictionary = {
			" ": 0,
			"a": 1,
			"b": 2,
			"c": 3,
			"d": 4,
			"e": 5,
			"f": 6,
			"g": 7,
			"h": 8,
			"i": 9,
			"j": 10,
			"k": 11,
			"l": 12,
			"m": 13,
			"n": 14,
			"o": 15,
			"p": 16,
			"q": 17,
			"r": 18,
			"s": 19,
			"t": 20,
			"u": 21,
			"v": 22,
			"w": 23,
			"x": 24,
			"y": 25,
			"z": 26,
			"!": 27,
			'"': 28,
			"#": 29,
			"$": 30,
			"%": 31,
			"&": 32,
			"'": 33,
			"(": 34,
			")": 35,
			"*": 36,
			"+": 37,
			",": 38,
			"-": 39,
			".": 40,
			"/": 41,
			"0": 42,
			"1": 43,
			"2": 44,
			"3": 45,
			"4": 46,
			"5": 47,
			"6": 48,
			"7": 49,
			"8": 50,
			"9": 51,
			":": 52,
			";": 53,
			"<": 54,
			"=": 55,
			">": 56,
			"?": 57,
			"@": 58
		}
	def _ord(self, char):
		return self.dictionary[char]
	def _chr(self, num):
		for eachKey in self.dictionary:
			if self.dictionary[eachKey]==num:
				return eachKey
		return 59
	def encrypt(self, string):
		return "".join([self._chr((self._ord(eachChar) + self.offset) % 59) for eachChar in string])
	def decrypt(self, string):
		return "".join([self._chr((self._ord(eachChar) - self.offset) % 59) for eachChar in string])
	def toIR(self, string):
		return [self._ord(eachChar) for eachChar in string]
	def fromIR(self, num_list):
		return "".join([self._chr(eachNum) for eachNum in num_list])

if __name__ == '__main__':
	robotEncryption = RobotEncryption(1)
	print(robotEncryption.encrypt("abcdefgz"))
	print(robotEncryption.decrypt("bcdefgha"))
	print(robotEncryption.toIR("bcdefghxyza"))
	print(robotEncryption.fromIR([98, 99, 100, 101, 102, 103, 104]))
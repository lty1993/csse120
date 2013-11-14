class RobotEncryption(object):
	"""
	A class for encrypting / decrypting messages.
	"""
	def __init__(self, offset=40):
		self.offset = offset
	def encrypt(self, string):
		return "".join([chr((ord(eachChar) + self.offset) % 127) for eachChar in string])
	def decrypt(self, string):
		return "".join([chr((ord(eachChar) - self.offset) % 127) for eachChar in string])
	def toIR(self, string):
		return [ord(eachChar) for eachChar in string]
	def fromIR(self, num_list):
		return "".join([chr(eachNum) for eachNum in num_list])

if __name__ == '__main__':
	robotEncryption = RobotEncryption(1)
	print(robotEncryption.encrypt("abcdefgz"))
	print(robotEncryption.decrypt("bcdefgha"))
	print(robotEncryption.toIR("bcdefghxyza"))
	print(robotEncryption.fromIR([98, 99, 100, 101, 102, 103, 104]))
from Crypto.Cipher import DES


class Encryption:
	def __init__(self, key):
		self.DES = DES.new(key, DES.MODE_ECB)

	def encrypt(self, data):
		return self.DES.encrypt(data)

	def decrypt(self, data):
		return self.DES.decrypt(data)

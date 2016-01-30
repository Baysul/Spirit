import hashlib
from random import choice
from string import ascii_letters, digits

class Crypto:

	@staticmethod
	def generateRandomKey():
		characterSelection = ascii_letters + digits

		return "".join(choice(characterSelection) for i in range(16))

	@staticmethod
	def encryptPassword(password):
		hash = hashlib.md5(password.encode('utf-8')).hexdigest()
		swappedHash = hash[16:32] + hash[0:16]

		return swappedHash

	@staticmethod
	def getLoginHash(password, rndK):
		key = Crypto.encryptPassword(password).upper()
		key += rndK
		key += "a1ebe00441f5aecb185d0ec178ca2305Y(02.>'H}t\":E1_root"

		hash = Crypto.encryptPassword(key)

		return hash
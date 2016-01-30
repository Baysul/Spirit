import hashlib
from random import choice
from string import ascii_letters, digits

class Crypto:

	@staticmethod
	def hash(string):
		if isinstance(string, (int, long)):
			string = str(string)

		return hashlib.md5(string.encode("utf-8")).hexdigest()

	@staticmethod
	def generateRandomKey():
		characterSelection = ascii_letters + digits

		return "".join(choice(characterSelection) for _ in range(16))

	@staticmethod
	def encryptPassword(password, hash=True):
		if hash:
			password = Crypto.hash(password)

		swappedHash = password[16:32] + password[0:16]

		return swappedHash

	@staticmethod
	def getLoginHash(password, rndK):
		key = Crypto.encryptPassword(password, False)
		key += rndK
		key += "a1ebe00441f5aecb185d0ec178ca2305Y(02.>'H}t\":E1_root"

		hash = Crypto.encryptPassword(key)

		return hash
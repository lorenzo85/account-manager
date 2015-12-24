import json
from encryption import *


class Manager:
	def __init__(self, file, key):
		self.file = file
		self.key = key

	def list(self):
		return self.load()

	def show(self, alias):
		accounts = self.load()
		matched = [account for account in accounts if account['alias'].lower() == alias.lower()]
		if len(matched) > 1 or len(matched) == 0:
			raise Exception('Found 0 or more than one matching the alias: \'%s\'' % alias)
		return matched[0]

	def add(self, alias, username, password, url='', notes=''):
		account = { 'alias': alias, 'username': username, 'password': password, 'url': url, 'notes': notes }
		accounts = self.load()
		matched = [account for account in accounts if account['alias'].lower() == alias.lower()]
		if matched:
			raise Exception('Could not add alias %s because it exists already!!' % alias)
		accounts.append(account)
		self.save(accounts)

	def delete(self, alias):
		accounts = self.load()
		filtered = filter(lambda account: account['alias'] != alias, accounts)
		self.save(list(filtered))

	def load(self):
		data = self.file_read()
		return json.loads(data.decode())

	def save(self, data):
		json_data = json.dumps(data, indent=4, sort_keys=True)
		self.file_write(json_data)

	def apply_padding(self, data):
		length = len(data)
		if not length % 8 == 0:
			delta = length % 8
			return data.ljust(length + 8 - delta)
		return data

	def encrypter(func):
		def func_wrapper(self, data):
			data = self.apply_padding(data)
			encryption = Encryption(self.key)
			data = encryption.encrypt(data)
			func(self, data)
		return func_wrapper

	def decrypter(func):
		def func_wrapper(self):
			data = func(self)
			data = self.apply_padding(data)
			encryption = Encryption(self.key)
			return encryption.decrypt(data)
		return func_wrapper

	@decrypter
	def file_read(self):
		with open(self.file, 'rb') as file:
			return file.read()

	@encrypter
	def file_write(self, data):
		with open(self.file, 'wb') as file:
			file.write(data)

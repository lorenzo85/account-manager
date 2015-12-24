from manager import *
import os.path as path
import getpass

OP_ADD = 'ADD'
OP_LIST = 'LIST'
OP_SHOW = 'SHOW'
OP_DELETE = 'DELETE'

OPERATIONS = [OP_LIST, OP_SHOW, OP_ADD, OP_DELETE]

class AccountManager:
	def __init__(self, file):
		self.file = file

	def execute(self, operation, args):
		function = self.operations[operation]
		return function(self, args)

	def accessmanager(func):
		def func_wrapper(self, args):
			if not hasattr(self, 'password'):
				self.password = getpass.getpass('Enter password: ')
			manager = Manager(self.file, self.password)
			func(self, manager, args)
		return func_wrapper

	def storecheck(func):
		def func_wrapper(self, manager, args):
			if not path.isfile(manager.file):
				result = input('A store file needs to be created, create one [yes/no] ? ')
				if not None and result.lower() == 'yes':
					manager.save([])
					print('Store file successfully created in %s' % manager.file)
				else:
					raise Exception('No store available! Aborting!')
			func(self, manager, args)
		return func_wrapper
	
	@accessmanager
	@storecheck
	def do_list(self, manager, args):
		""" Lists all the account aliases stored in the file """
		accounts = manager.list()
		print('*****************************************')
		print('\t%d account/s found' % len(accounts))
		for account in accounts:
			print('\tAlias: %s' % account['alias'])
		print('*****************************************')

	@accessmanager
	@storecheck
	def do_show(self, manager, args):
		""" Returns the username, password and url for a given alias """
		alias = self.get_alias(args)
		account = manager.show(alias)
		print('*****************************************')
		print('\tAlias: %s' % account['alias'])
		print('\tUsername: %s' % account['username'])
		print('\tPassword: %s' % account['password'])
		print('\tURL: %s' % account['url'])
		print('\tNotes: %s' % account['notes'])
		print('*****************************************')

	@accessmanager
	@storecheck
	def do_add(self, manager, args):
		""" Adds a new alias and corresponding username, password and url """
		alias = self.get_alias(args)
		url = input('URL: ')
		username = input('Username: ')
		password = input('Password: ')
		notes = input('Notes: ')
		manager.add(alias, username, password, url, notes)
		print('Account %s successfully added.' % alias)
	
	@accessmanager
	@storecheck
	def do_delete(self, manager, args):
		""" Deletes alias entry from the file """
		alias = self.get_alias(args)
		manager.delete(alias)
		print('Account %s successfully deleted.' % alias)

	operations = {OP_LIST: do_list, OP_SHOW: do_show, OP_ADD: do_add, OP_DELETE: do_delete}

	def get_alias(self, args):
		return args[0] if args else input('Alias: ') 


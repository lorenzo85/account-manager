import argparse
from controller import *

VERSION = 0.1

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-fs", "--filestore", dest = "filestore", default = "data.x", help="Filestore name")
	args = parser.parse_args()

	manager = AccountManager(args.filestore)
	print('Accounts manager v%.2f' % VERSION)
	while True:
		try:
			operation = input('Select operation [%s]: ' % ','.join(OPERATIONS + ['EXIT']))
			operation, *args = operation.split()
			operation = operation.upper()
			if operation in OPERATIONS:
				manager.execute(operation, args)
			elif operation == 'EXIT':
				break
			else:
				raise Exception('Operation %s not available!' % operation)
		except Exception as e:
			print('ERROR: %s' % str(e))
		

if __name__ == "__main__": main()
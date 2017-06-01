import os
import sys

import keyUtils


def main(names):
	if not os.path.exists('certs'):
		os.makedirs('certs')
	for i in names:
		i = i.lower()
		keyName = 'certs/' + i
		if os.path.isfile(keyName + 'Public.pem') or os.path.isfile(keyName + 'Private.pem'):
			print(i + ' already exists, not generating key pair')
			continue
		else:
			keyUtils.generateFullPEM(i)
			print('Created pem files for ' + i)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1:])
	else:
		raise Exception("No names, exiting")

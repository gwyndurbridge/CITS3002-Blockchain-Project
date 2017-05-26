import json, time
import minerUtil as mu

pendingTransactions = {}
pastTransactions = {}
name = ''
numActualBalance = 0
numAvailableFunds = 0

def avaliableFunds(self, arg):
	# actual - transactions pending
	pass


def actualBalance(self, arg):
	pass


def importBlockChain(self, arg):
	pass


# updates balance and blockchain file
def update(newBlockchain):
	global numActualBalance, numAvailableFunds, pendingTransactions, pastTransactions

	# Create blockchain file if it doesnt already exist
	with open('blockchain.json', 'a') as temp:
		pass

	with open('blockchain.json', 'r+') as blockchainFile:
		# create list of hashes of pending transactions
		pendingKeys = []
		for key in pendingTransactions:
			pendingKeys.append(key)

		oldBlockchain = blockchainFile.read()
		# if the chain is empty give exception
		if oldBlockchain == '' or oldBlockchain == '\n':
			raise Exception('no blocks in old chain')
		elif newBlockchain == '' or newBlockchain == '\n':
			raise Exception('no blocks in new chain')
		else:
			# if blockchains are not empty
			oldBlockchainOpen = json.loads(oldBlockchain)
			newBlockchainOpen = json.loads(newBlockchain)

			# if received blockchain is shorter than the current one, reject it
			if len(newBlockchainOpen) < len(oldBlockchainOpen):
				raise Exception('receiving older blockchain - reject')

			numBlocksMissing = len(newBlockchainOpen) - len(oldBlockchainOpen)

			#amount actualBalance and availableFunds need to be updated by
			actualBalanceChange = 0
			availableFundsChange = 0
			for i in range(-numBlocksMissing, 0, 1):
				# loop through new blocks
				# get the body
				blockBody = newBlockchainOpen[i]['body']
				for key in blockBody:
					# check if you're included in any transactions
					transaction = json.loads(json.loads(blockBody[key])['transaction'])

					if key in pendingKeys:
						# if you are the sender pay 'value' and regain 'change' and move it from pending to past
						actualBalanceChange += transaction['change'] - transaction['value']

						pastTransactions[key] = transaction
						pendingTransactions.pop(key)
					elif transaction['sender'] == name:
						# if you are a sender but you dont remember sending it check past transactions
						raise Exception('found unexpected payment')
					elif transaction['receiver'] == name:
						# if you are the receiver gain payment
						actualBalanceChange += transaction['payment']
						availableFundsChange += transaction['payment']

			numActualBalance += actualBalanceChange
			numAvailableFunds += availableFundsChange

			blockchainFile.seek(0)
			blockchainFile.write(newBlockchain)


def generateTransaction(self, arg):
	# will use client.py to send transaction
	# needs to keep an eye on unverified transactions
	pass


# example - make update read blockchain1 and make blockchain1 == blockchain
'''name = 'Jill'

t1 = json.dumps({'sender': name, 'receiver': 'jerry', 'value': 50, 'payment': 40, 'change': 5, 'time': time.ctime()})
t1 = json.dumps({'transaction': t1, 'signature': 'u4h298h4g92'})
t2 = json.dumps({'sender': name, 'receiver': 'bobba', 'value': 30, 'payment': 20, 'change': 1, 'time': time.ctime()})
t2 = json.dumps({'transaction': t2, 'signature': 'u4h298h4g92'})

pendingTransactions[mu.hashInput(t1)] = t1
pendingTransactions[mu.hashInput(t2)] = t2

import miner
miner.run([t1, t2])

with open('blockchain.json', 'r') as bc:
	bcr = bc.read()
	update(bcr)

print(numActualBalance, numAvailableFunds)'''
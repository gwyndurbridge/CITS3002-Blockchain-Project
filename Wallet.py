import minerUtil
import transactionMaker,json, time
import os

class Wallet:

	def __init__(self,givenName):
		self.name = givenName
		self.pendingTrans = {} #should be in the form hash:value
		self.numAvailableFunds = 0
		self.numActualBalance = 0
		print(self.name)
		self.readPending()
		self.update()

	def end(self, arg):
		self.writePending()

	def readPending(self):
		pendingName = self.name+'Pending.json'
		if os.path.isfile(pendingName):
			with open(pendingName,'r') as f:
				json.load(self.pendingTrans,f)


	def writePending(self):
		with open(self.name+'Pending.json','w') as f:
			json.dump(self.pendingTrans,f)

	def generateTransaction(self,reciever,value,payment,change):
		#will use client.py to send transaction
		transactionDump = transactionMaker.generateTransaction(self.name,reciever,value,payment,change)
		transactionHash = minerUtil.hashInput(transactionDump)
		transactionLoss = value - change
		self.pendingTrans[transactionHash] = transactionLoss
		self.numAvailableFunds -= transactionLoss
		return transactionDump

	def update(self, newBlockchain):
		# Create blockchain file if it doesnt already exist
		with open('blockchain.json', 'a') as temp:
			pass

		with open('blockchain1.json', 'r+') as blockchainFile:
			# create list of hashes of pending transactions
			pendingKeys = []
			for key in self.pendingTrans:
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

				# amount actualBalance and availableFunds need to be updated by
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
							self.pendingTrans.pop(key)
						elif transaction['sender'] == self.name:
							# if you are a sender but you dont remember sending it check past transactions
							raise Exception('found unexpected payment')
						elif transaction['receiver'] == self.name:
							# if you are the receiver gain payment
							actualBalanceChange += transaction['payment']
							availableFundsChange += transaction['payment']

				self.numActualBalance += actualBalanceChange
				self.numAvailableFunds += availableFundsChange

				blockchainFile.seek(0)
				blockchainFile.write(newBlockchain)

	def transFailiure(self, arg):
		#TODO
		#needs to remove and undo the Incorrect transaction from the avaliableFunds and pendingTrans
		pass

	def test(self):
		# example - make update read blockchain1 and make blockchain1 == blockchain
		self.name = 'Jill'

		t1 = json.dumps({'sender': self.name, 'receiver': 'jerry', 'value': 50, 'payment': 40, 'change': 5, 'time': time.ctime()})
		t1 = json.dumps({'transaction': t1, 'signature': 'u4h298h4g92'})
		t2 = json.dumps({'sender': self.name, 'receiver': 'bobba', 'value': 30, 'payment': 20, 'change': 1, 'time': time.ctime()})
		t2 = json.dumps({'transaction': t2, 'signature': 'u4h298h4g92'})

		self.pendingTrans[minerUtil.hashInput(t1)] = t1
		self.pendingTrans[minerUtil.hashInput(t2)] = t2

		import miner
		miner.run([t1, t2])

		with open('blockchain.json', 'r') as bc:
			bcr = bc.read()
			self.update(bcr)

		print(self.numActualBalance, self.numAvailableFunds)

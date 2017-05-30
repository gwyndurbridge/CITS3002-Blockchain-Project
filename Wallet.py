import minerUtil
import miner
import transactionMaker,json, time
import os
from shutil import copyfile

class Wallet:
	def __init__(self,givenName):
		self.name = givenName
		self.pendingTrans = {} #should be in the form hash:value
		self.numAvailableFunds = 0
		self.numActualBalance = 0
		self.readPending()
		self.loadBlockchain()

	def end(self):
		self.writePending()

	def readPending(self):
		pendingName = 'json/'+self.name+'Pending.json'
		if os.path.isfile(pendingName):
			with open(pendingName,'r') as f:
				json.load(self.pendingTrans,f)


	def writePending(self):
		with open('json/'+self.name+'Pending.json','w') as f:
			json.dump(self.pendingTrans,f)

	def generateTransaction(self,receiver,value,payment,change):
		#will use client.py to send transaction
		if value <= self.numAvailableFunds:
			transactionDump = transactionMaker.generateTransaction(self.name,receiver,value,payment,change)
			transactionHash = minerUtil.hashInput(transactionDump)
			transactionLoss = value - change
			self.pendingTrans[transactionHash] = transactionLoss
			self.numAvailableFunds -= transactionLoss
			return transactionDump
		else:
			print("Not enough funds")
			return -1

	# loads blockchain from file on startup
	def loadBlockchain(self):
		with open('json/andyBlockchain.json', 'a') as temp:
			pass
		with open('json/andyBlockchain.json', 'r+') as blockchainFile:
			blockchain = blockchainFile.read()
			if blockchain == '' or blockchain == '\n':
				#if blockchain is empty create empty list to hold chain. Balance is 0 by default
				blockchainFile.seek(0)
				blockchainFile.write(json.dumps([]))
			else:
				actualBalanceChange = 0
				availableFundsChange = 0
				blockchainOpen = json.loads(blockchain)
				for block in blockchainOpen:
					body = block['body']
					for key in body:
						transaction = json.loads(body[key])['transaction']
						if transaction['sender'] == self.name:
							# if you are the sender lose the payment value and get change
							actualBalanceChange += transaction['change'] - transaction['value']
							availableFundsChange += transaction['change'] - transaction['value']
						elif transaction['receiver'] == self.name:
							# if you are the receiver gain payment
							actualBalanceChange += transaction['payment']
							availableFundsChange += transaction['payment']
				self.numActualBalance += actualBalanceChange
				self.numAvailableFunds += availableFundsChange

	# takes blockchain json, updates balances, pending transactions and local blockchain file
	def update(self, newBlockchain):
		# Create blockchain file if it doesnt already exist
		with open('json/andyBlockchain.json', 'a') as temp:
			pass

		with open('json/andyBlockchain.json', 'r+') as blockchainFile:
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

				#make sure all blocks are valid
				for block in newBlockchainOpen:
					blockHeader = block['header']

					#if the block is not valid then dont update
					if not miner.checkNonce(blockHeader):
						print("blockchain received not valid")
						return -1

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
						transaction = json.loads(blockBody[key])['transaction']
						if transaction['sender'] == None or transactionMaker.checkSign(blockBody[key]):
							if key in pendingKeys:
								# if you are the sender pay 'value' and regain 'change' and move it from pending to past
								actualBalanceChange += transaction['change'] - transaction['value']
								self.pendingTrans.pop(key)
							elif transaction['sender'] == self.name:
								# if you are a sender but you dont remember sending it check past transactions. Future work do something about this
								raise Exception('found unexpected payment')
							elif transaction['receiver'] == self.name:
								# if you are the receiver gain payment
								actualBalanceChange += transaction['payment']
								availableFundsChange += transaction['payment']

				self.numActualBalance += actualBalanceChange
				self.numAvailableFunds += availableFundsChange

				blockchainFile.seek(0)
				blockchainFile.write(newBlockchain)

	# returns transaction json corresponding to the hash of the failed
	def transFailiure(self, failedHash):
		# make list of hashes in current pending transaction dict
		transactionKeys = []
		for key in self.pendingTrans:
			transactionKeys.append(key)
		# if the failed transaction was pending for this wallet, return it o it can resend
		if failedHash in transactionKeys:
			return self.pendingTrans[failedHash]
		# if it was not in there return 0 so client knows theres nothing to resend
		return 0

	def test(self):
		print('test')
		print("availablefunds: ", self.numAvailableFunds, "  actualBalance: ", self.numActualBalance)
		mineman = miner.Miner()
		mineman.setDifficulty(10, True)
		mineman.run([])

		copyfile("json/minerBlockchain.json", "json/andyBlockchain.json")

		t1 = self.generateTransaction('testio',20,15,3)
		print("availablefunds: ", self.numAvailableFunds, "  actualBalance: ", self.numActualBalance)

		if t1 != -1:
			mineman.run([t1])

		with open('json/minerBlockchain.json', 'r') as newchain:
			newchainOpen = newchain.read()
			self.update(newchainOpen)

		print("availablefunds: ", self.numAvailableFunds, "  actualBalance: ", self.numActualBalance)

#andy = Wallet('andy')
#andy.test()
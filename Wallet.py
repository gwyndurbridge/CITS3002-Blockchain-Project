import minerUtil
import transactionMaker,json
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
		writePending()

	def readPending(self):
		pendingName = self.name+'Pending.json'
		if os.path.isfile(pendingName):
			with open(pendingName,'r') as f:
				json.load(pendingTrans,f)


	def writePending(self):
		with open(self.name+'Pending.json','w') as f:
			json.dump(pendingTrans,f)

	def generateTransaction(self,reciever,value,payment,change):
		#will use client.py to send transaction
		transactionDump = transactionMaker.generateTransaction(self.name,reciever,value,payment,change)
		transactionHash = minerUtil.hashInput(transactionDump)
		transactionLoss = value - change
		self.pendingTrans[transactionHash] = transactionLoss
		self.numAvailableFunds -= transactionLoss
		return transactionDump

	def update(self):
		#kevin
		pass

	def transFailiure(self, arg):
		#TODO
		#needs to remove and undo the Incorrect transaction from the avaliableFunds and pendingTrans
		pass

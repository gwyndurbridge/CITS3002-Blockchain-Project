import json, random, time, sys
import transactionMaker as tm
import minerUtil as ut
debugging = False
random.seed()

def calculateDifficulty(defaultDifficulty):
	with open('json/minerBlockchain.json', 'r+') as blockchainFile:
		blockchain = blockchainFile.read()
		#return default if its the first one
		if blockchain == '' or blockchain == '\n':
			return defaultDifficulty
		blockchain = json.loads(blockchain)

		#find time bewteen last two blocks
		timeDiff = blockchain[-1]['header']['timeStamp'] - blockchain[-2]['header']['timeStamp']

		#if average is more than 2 minutes return previous block difficulty - 2
		if timeDiff > 120:
			return blockchain[-1]['header']['difficultyTarget'] - 2
		#if average is less than 2 minutes return previous block difficulty + 2
		return  blockchain[-1]['header']['difficultyTarget'] + 2

#creates money out of nowhere for the miner and adds transaction fees
#return json string of coinbase transaction
def createCoinbaseTransaction(transactions):
	generation = 50
	fee = 0
	for transaction in transactions:
		transaction = json.loads(transaction)
		transaction = json.loads(transaction['transaction'])
		fee += transaction['value'] - transaction['payment'] - transaction['change']

	coinbaseTransaction = {'sender' : None ,'receiver' : ut.getMinerKey(), 'value' : fee+generation, 'payment' : fee+generation, 'change' : 0, 'time' : time.ctime()}
	coinbaseTransactionDump = json.dumps(coinbaseTransaction)
	coinbaseTransactionFull = {'transaction' : coinbaseTransactionDump, 'signature' : None}

	return json.dumps(coinbaseTransactionFull)

def generateBlockBody(transactions):
	dict = {}
	for transaction in transactions:
		#if sender is none, then its the coinbase transaction to dont worry about it
		outerTransaction = json.loads(transaction)
		innerTransaction = json.loads(outerTransaction['transaction'])
		if innerTransaction['sender'] == None:
			digest = ut.hashInput(transaction)
			dict[digest] = transaction
		#if its not the coinbase transcation make sure the signature matches the transaction
		elif tm.checkSign(transaction):
			digest = ut.hashInput(transaction)
			dict[digest] = transaction
		else:
			#send nack
			pass

	return dict

#creates a header for the block without a nonce
def generateBlockHeader(difficulty, transactions):
	blockHeader = {'prevBlockHash':ut.getLastBlockHash(), 'timeStamp':time.time(), 'difficultyTarget':difficulty, 'nonce':None, 'merkleRoot':ut.merkleRoot(transactions)}
	return  blockHeader

def generateNonce(header):
	loop = True
	best = 0
	timer = time.time()

	while loop:
		#generate random nonce
		nonce = random.randint(0,9999999999999)

		#add nonce to header
		header['nonce'] = nonce
		difficulty = header['difficultyTarget']

		digest = ut.hashInput(json.dumps(header))

		#create string to hold bits as int rather than byte type
		bits = ''

		#takes bits one at a time and convert to 8-bit binary string
		for i in digest:
			#add binary string representation of byte into bits string
			bits += bin(int(i,16))[2:].zfill(8)

		for i in range(0,difficulty + 1):
			#check if value of bit is 0
			if int(bits[i]) == 0:
				#This whole section is just to help visualise progress
				# write current highest bit reached, to help visualise progress. Not necessary
				if int(i) > best:
					best = int(i)
				sys.stdout.write('Best: %d  \r' % best)
				sys.stdout.flush()

				#if you have a run of 0s long enough then break out of the loop
				if int(i) == difficulty:
					loop = False
			#if this bit isnt zero move one to next nonce
			else:
				break
	#add time taken
	if debugging:
		print("\n\nTime taken: ", time.time() - timer)
	#header['processingTime'] = processingTime
	return header

#add block to blockchain
def addToBlockchain(header, body):
	header = json.dumps(header)
	block = {'header':header, 'body':body}

	with open('json/minerBlockchain.json', 'r+') as blockchainFile:
		blockchain = blockchainFile.read()
		# if the chain is empty put the block in an array first
		if blockchain == '' or blockchain == '\n':
			block = [block]
			blockchainFile.write(json.dumps(block))
			return True

		#if there is already blocks there append it to the chain array
		blockchain = json.loads(blockchain)
		blockchain.append(block)
		blockchainFile.seek(0)
		blockchainFile.write(json.dumps(blockchain))

		return json.dumps(blockchain)

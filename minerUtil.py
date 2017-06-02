import hashlib, json

def getMinerKey():
	return 'miner'

def pairList(list):
	#go through list in steps of 2
	pairs = []
	for i in range(0, len(list), 2):
		#if first of pair is last element in list it has nothing to pair with so pair with self
		if i == len(list)-1:
			pairs.append([list[i],list[i]])
		else:
			pairs.append([list[i],list[i+1]])
	return pairs

def hashInput(inp):
	hash = hashlib.sha256()
	val = (inp).encode('utf-8')
	hash.update(val)
	return hash.hexdigest()

def merkleRoot(transactions):
	treeNextLevel = transactions

	loop = True
	while loop:
		#split list into pairs
		pairs = pairList(treeNextLevel)
		#start new list
		treeNextLevel = []
		for pair in pairs:
			pairCombinedHash = ''
			#hash each element of pair and add together
			for half in pair:
				digest = hashInput(half)
				pairCombinedHash += digest
			#add combined hash to list to use in next level of tree
			treeNextLevel.append(pairCombinedHash)
		if len(treeNextLevel) == 1:
			loop = False

	root = treeNextLevel[0]

	return root

#reference blockchain to get hash of previous block
def getLastBlockHash():
	#open and read the blockchain
	with open('json/minerBlockchain.json', 'r+') as blockchainFile:
		blockchain = blockchainFile.read()
		#if empty
		if blockchain == '' or blockchain == '\n':
			return None
		else:
		#load the blockchain and grab the last element
			blockchain = json.loads(blockchain)
			if len(blockchain) > 0:
				lastBlock = blockchain[-1]
				return hashInput(json.dumps(lastBlock['header'])+json.dumps(lastBlock['body'],sort_keys=True))
			else:
				return None

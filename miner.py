import hashlib, sys, time, random, json, os.path

random.seed()
defaultDifficulty = 35

def getMinerKey():
    return 'miner'

#creates money out of nowhere for the miner and adds transaction fees
#return json string of coinbase transaction
def createCoinbaseTransaction(transactions):
    fee = 0
    for transaction in transactions:
        transaction = json.loads(transaction)
        fee += transaction['value'] - transaction['payment'] - transaction['change']

    coinbaseTransaction = {'reciever' : getMinerKey(), 'value' : fee, 'payment' : fee, 'change' : 0}

    return json.dumps(coinbaseTransaction)

#creates a header for the block without a nonce
def generateBlockHeader(difficulty, transactions):
    blockHeader = {'prevBlockHash':getLastBlockHash(), 'timeStamp':time.time(), 'difficultyTarget':difficulty, 'nonce':None, 'merkleRoot':merkleRoot(transactions)}
    return  blockHeader

def generateBlockBody(transactions):
    dict = {}

    for transaction in transactions:
        digest = hashInput(transaction)
        dict[digest] = transaction

    return dict

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

#reference blockchain to get hash of previous block
def getLastBlockHash():
    #open and read the blockchain
    with open('blockchain.json', 'r+') as blockchainFile:
        blockchain = blockchainFile.read()
        #if empty
        if blockchain == '' or blockchain == '\n':
            return None
        else:
        #load the blockchain and grab the last element
            blockchain = json.loads(blockchain)
            return hashInput(json.dumps(blockchain[-1]))

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

        digest = hashInput(json.dumps(header))

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
    processingTime = time.time() - timer
    header['processingTime'] = processingTime

    return header

#take hash as input to check against
def checkNonce(header):
    digest = hashInput(json.dumps(header))
    bits = ''
    #change so prints in bits and returns true if correct
    for i in digest:
        # add binary string representation of byte into bits string
        bits += bin(int(i,16))[2:].zfill(8)
    #print('header hash bits:', bits)

    #count leading 0s
    count = 0
    for bit in bits:
        if bit == '0':
            count += 1
        else:
            break
    #return true if valid
    if count >= header['difficultyTarget']:
        return True
    #return False if not valid
    return False

#add block to blockchain
def addToBlockchain(header, body):

    block = {'header':header, 'body':body}

    with open('blockchain.json', 'r+') as blockchainFile:
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

def calculateDifficulty():
    with open('blockchain.json', 'r+') as blockchainFile:
        blockchain = blockchainFile.read()
        #return default if its the first one
        if blockchain == '' or blockchain == '\n':
            return defaultDifficulty
        blockchain = json.loads(blockchain)

        average = 0
        #find average time taken
        for block in blockchain:
            average += block['header']['processingTime']
            average = average/2

        #if average is more than 2 minutes return previous block difficulty - 1
        if average > 120:
            return blockchain[-1]['header']['difficultyTarget'] - 1
        #if average is less than 2 minutes return previous block difficulty + 1
        return  blockchain[-1]['header']['difficultyTarget'] + 1


def run(transactions):
    #if there's no blockchain file, make one
    if not os.path.isfile('blockchain.json'):
        open('blockchain.json','w+')
        difficulty = defaultDifficulty
    else:
        difficulty = calculateDifficulty()

    coinbaseTransaction = createCoinbaseTransaction(transactions)
    transactions.append(coinbaseTransaction)
    body = generateBlockBody(transactions)

    #print('body: ', body)

    head = generateBlockHeader(difficulty, transactions)
    head = generateNonce(head)

    #print('head: ', head)

    addToBlockchain(head, body)

"""example"""

t1 = {'sender':'Andy', 'receiver':'jerry', 'value':50, 'payment': 40, 'change':5, 'signature':'u4h298h4g92'}
t2 = {'sender':'James', 'receiver':'Billy', 'value':35, 'payment': 10, 'change':15, 'signature':'u4h298h4g92'}
ts1 = json.dumps(t1)
ts2 = json.dumps(t2)
transactions = [ts1, ts2]

run(transactions)

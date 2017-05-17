import hashlib, sys, time, random, json
random.seed()

#creates money out of nowhere for the miner and adds transaction fees
#return json string of coinbase transaction
def createCoinbaseTransaction(transactions):
    fee = 0
    for transaction in transactions:
        transaction = json.loads(transaction)
        fee += transaction['value'] - transaction['payment'] - transaction['change']

    coinbaseTransaction = {'reciever' : getMinerKey(), 'value' : fee, 'payment' : fee, 'change' : 0}

    return json.dumps(coinbaseTransaction)

def getMinerKey():
    return 'miner'

#creates a header for the block without a nonce
def generateBlockHeader(difficulty, transactions):
    blockHeader = {'prevBlockHash':getLastBlockHash(), 'timeStamp':time.time(), 'difficultyTarget':difficulty, 'nonce':None, 'merkleRoot':merkleRoot(transactions)}
    return  blockHeader

#should return dict of transactions with has as key
def generateBlockBody(transactions):
    dict = {}

    for transaction in transactions:
        digest = hashInput(transaction)
        dict[digest] = transaction

    return dict

#hash pair of transactions, add them together. Hash again
#just returning array rn. Need to do properly
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
    print('merkel root: ', root)

    return root

def pairList(list):
    #go through list in steps of 2
    pairs = []
    for i in range(0, len(list), 2):
        #if first of pair is last element in list it has nothing to pair with so pair with self
        if list[i] == len(list)-1:
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
    #get last block
    #hash it
    #return hash
    return '0000smileyface'

def generateNonce(header):
    loop = True
    best = 0
    timer = time.time()

    while loop:
        #generate random nonce
        nonce = random.randint(0,9999999999999)

        #add nonce to header
        header['nonce'] = nonce

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

    #print time taken
    print(time.time() - timer)
    print('successful nonce: ', nonce)
    return header

#take hash as input to check against
def checkNonce(header):
    digest = hashInput(json.dumps(header))
    bits = ''
    #change so prints in bits and returns true if correct
    for i in digest:
        # add binary string representation of byte into bits string
        bits += bin(int(i,16))[2:].zfill(8)
    print('header hash bits:', bits)

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
    return True

"""example"""
difficulty = 10

#example transaction
transaction = {'sender':'Alice', 'receiver':'Bob', 'value':50, 'payment': 40, 'change':5, 'signature':'u4h298h4g92'}
transactionString = json.dumps(transaction)

coinbaseTransaction = createCoinbaseTransaction([transactionString])

print('body: ', generateBlockBody([transactionString, coinbaseTransaction]))

header = generateBlockHeader(difficulty, [transactionString, coinbaseTransaction])
headerWithNonce = generateNonce(header)
print('header:', header)
print(checkNonce(header))



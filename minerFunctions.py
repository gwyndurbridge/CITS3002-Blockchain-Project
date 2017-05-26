import json, random, time, sys
import minerUtil as ut

random.seed()
defaultDifficulty = 35
useDefaultDifficulty = False

def setDefaults(diff, use):
    global defaultDifficulty, useDefaultDifficulty
    defaultDifficulty = diff
    useDefaultDifficulty = use

def calculateDifficulty():
    with open('blockchain.json', 'r+') as blockchainFile:
        blockchain = blockchainFile.read()
        #return default if its the first one
        if blockchain == '' or blockchain == '\n':
            return defaultDifficulty
        blockchain = json.loads(blockchain)

        average = 0
        #find average time taken
        for i in range(1,len(blockchain)):
            #add up time between release of blocks.
            #skips first block because there's no previous reference
            average += blockchain[i]['header']['timeStamp'] - blockchain[i-1]['header']['timeStamp']
        average = average/len(blockchain)

        #if average is more than 2 minutes return previous block difficulty - 2
        if average > 120:
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

    coinbaseTransaction = json.dumps({'sender' : None ,'receiver' : ut.getMinerKey(), 'value' : fee+generation, 'payment' : fee+generation, 'change' : 0, 'time' : time.ctime()})
    coinbaseTransactionFull = {'transaction' : coinbaseTransaction, 'signature' : None}

    return json.dumps(coinbaseTransactionFull)

def generateBlockBody(transactions):
    dict = {}

    for transaction in transactions:
        digest = ut.hashInput(transaction)
        dict[digest] = transaction

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
    #processingTime = time.time() - timer
    #header['processingTime'] = processingTime
    return header

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
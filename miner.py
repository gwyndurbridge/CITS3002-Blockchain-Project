import os.path, json, time
import mainFunctions as mf
import util as ut

#take hash as input to check against
def checkNonce(header):
    digest = ut.hashInput(json.dumps(header))
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

def setDifficulty(difficulty, alwaysUse):
    mf.setDefaults(difficulty, alwaysUse)

def run(transactions):
    defaultDifficulty = mf.defaultDifficulty
    useDefaultDifficulty = mf.useDefaultDifficulty

    #if there's no blockchain file, make one
    if not os.path.isfile('blockchain.json'):
        open('blockchain.json','w+')
        difficulty = defaultDifficulty
    elif useDefaultDifficulty:
        difficulty = defaultDifficulty
    else:
        difficulty = mf.calculateDifficulty()

    coinbaseTransaction = mf.createCoinbaseTransaction(transactions)
    transactions.append(coinbaseTransaction)
    body = mf.generateBlockBody(transactions)

    #print('body: ', body)

    head = mf.generateBlockHeader(difficulty, transactions)
    head = mf.generateNonce(head)

    #print('head: ', head)

    mf.addToBlockchain(head, body)

"""example"""

'''t1 = json.dumps({'sender':'Andy', 'receiver':'jerry', 'value':50, 'payment': 40, 'change':5, 'time' : time.ctime()})
t1 = json.dumps({'transaction' : t1, 'signature' : 'u4h298h4g92'})
t2 = json.dumps({'sender':'James', 'receiver':'Billy', 'value':35, 'payment': 10, 'change':15, 'time' : time.ctime()})
t2 = json.dumps({'transaction': t2, 'signature':'u4h298h4g92'})

transactions = [t1, t2]

setDifficulty(31, True)
run(transactions)
run([])'''

import json
import os.path

import minerFunctions as mf
import minerUtil as ut


class Miner():
    def __init__(self):
        self.defaultDifficulty = 35
        self.useDefaultDifficulty = False

    def setDifficulty(self, difficulty, alwaysUse):
        self.defaultDifficulty = difficulty
        self.useDefaultDifficulty = alwaysUse

    def run(self, transactions):
        defaultDifficulty = self.defaultDifficulty
        useDefaultDifficulty = self.useDefaultDifficulty

        # if there's no blockchain file, make one
        if not os.path.isfile('json/minerBlockchain.json'):
            open('json/minerBlockchain.json', 'w+')
            difficulty = defaultDifficulty
        elif useDefaultDifficulty:
            difficulty = defaultDifficulty
        else:
            difficulty = mf.calculateDifficulty()

        coinbaseTransaction = mf.createCoinbaseTransaction(transactions)
        transactions.append(coinbaseTransaction)
        body = mf.generateBlockBody(transactions)

        head = mf.generateBlockHeader(difficulty, transactions)
        head = mf.generateNonce(head)

        return mf.addToBlockchain(head, body)


# take hash as input to check against
def checkNonce(header):
    digest = ut.hashInput(json.dumps(header))
    bits = ''
    # change so prints in bits and returns true if correct
    for i in digest:
        # add binary string representation of byte into bits string
        bits += bin(int(i, 16))[2:].zfill(8)
    # print('header hash bits:', bits)

    # count leading 0s
    count = 0
    for bit in bits:
        if bit == '0':
            count += 1
        else:
            break
    # return true if valid
    if count >= header['difficultyTarget']:
        return True
    # return False if not valid
    return False


"""example"""

# kt.test_PEMcreation()

'''
import keyTest as kt
t1 = tm.generateTransaction('andy','testy',50,30,10)

transactions = [t1]

miner = Miner()
miner.setDifficulty(31, True)
print(miner.run([]))'''

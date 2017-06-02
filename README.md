# CITS3002-Blockchain-Project

## Required Files
```
client.py
cli.py
keyGen.py
keyTest.py
keyUtils.py
minerFunctions.py
miner.py
minerUtil.py
printStyle.py
/rsa
server.py
settings.py
setup.py
transactionMaker.py
Wallet.py
```

## Setup

Run `python3 setup.py [NAMES]`
- This will produce a /certs foler with all the public and private key pairs for the given names.
- If this implementation is being used on multiple different computers, copy the certs folder directly over.
- Private keys may be discarded if the user will not log on to the machine.
- If no names are specified, the default "Alice" and "Bob" are used.
- A /json folder is also formed. If persistancy is not desired, delete the contents after use.
If any extra keys are requried, run `python3 keyGen.py [NAMES]` and follow the steps as above.

## Usage
### CLI
Run `python3 cli.py` for each wallet or miner instance you want to create
- Please only run one instance of the miner; there is no support for multiple miners
	- Each instance will guide you through the process of instantiating the relevant files
- Follow the prompts


## Classes
### Wallet
#### Transaction (dict with these keys)
    - 'transaction':dict
        - 'sender':string
        - 'receiver':string
        - 'value': int
        - 'payment': int
        - 'change': int
        - 'time':ctime
    - 'signature':string

#### To use
    - Create instance of Wallet class with user name as the argument
        e.g. joe = Wallet('Joe')
    - Create transaction with generateTransaction()
        returns json string transaction
    - Pass generated transaction to client
    - Use update() when new blockchain is received
    - Use end() before closing wallet to save pending transactions

#### Class Functions
    - end()
    - readPending()
    - writePending()
    - generateTransaction(str receiver,float value, float payment, float change) : json transaction
    - loadBlockchain()
    - update(json newBlockchain)
    - transFailure(str transactionHash) : json transaction OR 0

### Miner
#### Block (dict with 'header' and 'body' keys)
    Header (dict with these keys):
        - prevBlockHash : string
        - timeStamp : float
        - processingTime : float
        - difficultyTarget : int
        - merkleRoot : string
        - nonce : int
    Body (dict with hash as key to transactions):
        - {hash : transaction}
#### Blockchain
        Array of blocks. Each block is a dict with 'header' and 'body' keys.
        Entire blockchain array stored as json string
#### To use:
    setDifficulty(d, b)
        where    :    d = int, desired difficulty
                      b = bool, whether should always use d, or auto-update
    run(t)
        where    :    t = list of json string transactions
        returns  :    json string blockchain

Only the header of the block is hashed to find the correct nonce, so the merkle root is what actually
ties the transactions to the block and makes sure they were not changed.
If we are not using a merkle root the entire block (header and body) should be hashed to tie the transcations
to the hash.
#### Functions:
    - setDifficulty(int difficulty, bool alwaysUse)
    - run(json[] transactions, int difficulty)
    - createCoinbaseTransaction(json[] transactions) : json coinbaseTransaction
    - generateBlockHeader(int difficulty, json[] transactions) : dict header
    - generateBlockBody(json[] transactions) : dict{hash:transaction]
    - generateNonce(dict header) : dict headerWithNonce
    - checkNonce(dict header) : bool isValid
    - merkleRoot(json[] transactions) : str root
    - pairList([] list) : [] pairs
    - hashInput(str input) : str(hex) hash
    - getLastBlockHash() : str lastBlockHash
    - addToBlockchain(dict header, dict body)
    - calculateDifficulty() : int difficultyTarget
    - getMinerKey() : str minerKey

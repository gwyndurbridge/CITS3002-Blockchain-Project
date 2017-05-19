# CITS3002-Blockchain-Project

# Transaction (dict with these keys)
- 'sender':string
- 'receiver':string
- 'value': int
- 'payment': int
- 'change': int
- 'signature':string

# Block
Header:
- prevBlockHash
- timeStamp
- difficultyTarget
- merkle root
- nonce

Body:
- hash : transaction

# Blockchain
Array of blocks. Each block is a dict with 'header' and 'body' keys.
Entire blockchain array stored as json string

# Miner
#To use:

run(t, d)
    where
        t = list of json transactions
        d = (int) difficulty

Only the header of the block is hashed to find the correct nonce, so the merkle root is what actually
ties the transactions to the block and makes sure they were not changed.
If we are not using a merkle root the entire block (header and body) should be hashed to tie the transcations
to the hash.

# Miner functions:
Complete:
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

Incomplete:
- (returning dummy value) getMinerKey() : str minerKey


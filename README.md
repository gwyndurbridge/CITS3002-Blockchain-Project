# CITS3002-Blockchain-Project

# Block
Header:
- prevBlockHash
- timeStamp
- difficultyTarget
- (extension) merkle root
- nonce

Body:
- Coinbase transaction
- Rest of transcations

Only the header of the block is hashed to find the correct nonce, so the merkle root is what actually
ties the transactions to the block and makes sure they were not changed.
If we are not using a merkle root the entire block (header and body) should be hashed to tie the transcations
to the hash.

# Miner functions:
Complete:
- createCoinbaseTransaction(json[] transactions) : json coinbaseTransaction
- generateBlockHeader(int difficulty, json[] transactions) : dict header
- generateNonce(dict header) : dict headerWithNonce
- checkNonce(dict header) : bool isValid

Incomplete:
- (returning dummy value) getMinerKey() : str minerKey
- (probably not needed. Just added for completeness) generateBlockBody(json[] transactions) : json[] transactions
- (just concatenating them rn) merkleRoot(json[] transactions) : str root
- (returning dummy value) getLastBlockHash() : str lastBlockHash

To use:
    - cb = createCoinbaseTransaction([transactions])
    - hd = generateBlockHeader([transactions, cb])
    - generateNonce(hd)
- See example

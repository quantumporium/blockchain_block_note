from hashlib import sha256
import json # deal with json in python
from datetime import datetime

# interface
from flask import Flask, request
import request

# create the Block class
class Block:
    def __init__(self, index, nonce, timestamp, block_hash, previous_hash, transactions):
        self.index = index
        self.nonce = nonce
        self.timestamp = timestamp
        self.block_hash  = block_hash
        self.previous_hash = previous_hash
        self.transactions = transactions


# hash the block - digital signature of the block
    def hash_block(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_data.encode()).hexdigest()


# create the Blockchain class that will hold all the structure
class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    @property
    def last_block(self):
        return self.chain[-1]

    def create_genesis_block(self):
        genesis_data = '' # type the first transaction-data you whant to be in the blockchain
        genesis_block = Block(index = 0, nonce = 0, timestamp = str(datetime.now()), block_hash = '', previous_hash = '', transactions = [genesis_data] )
        genesis_block.block_hash = genesis_block.hash_block()
        self.chain.append(genesis_block)

# add new transaction in a giving block
    def add_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    difficulty = 2
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.hash_block()
        while computed_hash[:Blockchain.difficulty] != ('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.hash_block()
            print(block.nonce, block.hash_block())

        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.block_hash
        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.block_hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return ((block_hash[:blockchain.difficulty] == 0) and (block_hash == block.hash_block()))

    def mine(self):
        if not self.unconfimed_transactions:
            return False
        
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1, nonce = '', timestamp = str(datetime.now()), block_hash = '', previous_hash = last_block.block_hash, transactions = self.unconfimed_transactions)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfimed_transaction = []
        return new_block.index

# all the code above work well


app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return json.dumps({'lenght': len(chain_data), 'chain': chain_data})

app.run(debug=True, port=5000)
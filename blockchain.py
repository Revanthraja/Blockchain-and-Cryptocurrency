# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 21:31:39 2022

@author: Revanth raja M
"""
import datetime
import hashlib
import json # encodes the function
from flask import Flask,jsonify # for web application and postman interaction

# Part 1 Bulid a Blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,prev_hash="0")#creating a block
    def create_block(self,proof,prev_hash):
        block={"index":len(self.chain)+1,"timestamp":str(datetime.datetime.now()),
               "proof":proof,
               "prev_hash":prev_hash}
        self.chain.append(block)
        return block
    def get_prevblock(self):
        return self.chain[-1]
# proof of work
    def proof_of_work(self,prev_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-prev_proof**2).encode()).hexdigest()#for hashtable
            if hash_operation[:4]=="0000":
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):#it will hash each block
        encoded_block=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):#checking a validity
        prevs_block=chain[0]
        block_index=1
        while block_index<len(chain):            
            block=chain[block_index]
            if block['prev_hash']!=self.hash(prevs_block):#uses the hash method
                return False
            prev_proof=prevs_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]!="0000":
                return False
            prevs_block=block
            block_index+=1
        return True
#Mining of blockchain

#creating a flask webapplication
app = Flask(__name__)

#creating a blockchain
blockchain=Blockchain()

#Mining a BlockChain
@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block=blockchain.get_prevblock()
    prev_proof=prev_block['proof']
    proof=blockchain.proof_of_work(prev_proof)
    prev_hash=blockchain.hash(prev_block)
    block=blockchain.create_block(proof, prev_hash)
    response={"message":"Congradulation you just mined the block","index":block['index'],
              "timestamp":block['timestamp'],
              "proof":block['proof'],
              "prev_hash":block["prev_hash"]}
    return jsonify(response),200

#geting a full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response={"chain":blockchain.chain,
              "length":len(blockchain.chain)}
    return jsonify(response),200

# checking a blockchain is valid

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={"message":"All good . The Blockchain is valid"}
    else:
        response={"message":"Block chain have a problem"}
    return jsonify(response),200
    

app.run(host = '0.0.0.0',port=5000)

            
        
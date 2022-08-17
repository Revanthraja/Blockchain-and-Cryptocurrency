

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 21:31:39 2022

@author: Revanth raja M
"""
import datetime #for exact time
import hashlib #sha256
import json # encodes the function
from flask import Flask,jsonify,request # for web application and postman interaction
import requests

from uuid import uuid4
from urllib.parse import urlparse

# Part 1 Bulid a Blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.create_block(proof=1,prev_hash="0")#creating a block
        self.nodes=set()
    def create_block(self,proof,prev_hash):
        block={"index":len(self.chain)+1,"timestamp":str(datetime.datetime.now()),
               "proof":proof,
               "prev_hash":prev_hash,
               "transactions":self.transactions}
        self.transactions=[]
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
    def add_transactions(self,sender,receiver,amount):
        self.transactions.append({"sender":sender,
                                  "reciver":receiver,"amount":amount})
        prev_block=self.get_prevblock()
        return prev_block["index"]+1
    def add_node(self,address):
        parsed_url=urlparse(address)
        self.node.add(parsed_url.netloc)
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
           response= requests.get(f'http://{node}/get_chain')
           if response.status_code==200:
               length=response.json()["length"]
               chain=response.json()['chain']
               if length>max_length and self.is_chain_valid(chain):
                   max_length=length
                   longest_chain=chain
        if longest_chain:
            self.chain=longest_chain
            return True
        return False
    

       
#Mining of blockchain

#creating a flask webapplication
app = Flask(__name__)

#creating address for the node on port 5000
node_address=str(uuid4()).replace('-','')

#creating a blockchain
blockchain=Blockchain()

#Mining a BlockChain
@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block=blockchain.get_prevblock()
    prev_proof=prev_block['proof']
    proof=blockchain.proof_of_work(prev_proof)
    prev_hash=blockchain.hash(prev_block)
    blockchain.add_transactions(sender=node_address, receiver="King", amount=1)
    block=blockchain.create_block(proof, prev_hash)
    response={"message":"Congradulation you just mined the block","index":block['index'],
              "timestamp":block['timestamp'],
              "proof":block['proof'],
              "prev_hash":block["prev_hash"],
              "transactions":block['transactions']}
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

#Adding a new transactions to blockchain
@app.route('/add_transactions', methods=['POST'])
def add_transactions():
    json=request.get_json()
    transaction_keys=['sender','receiver','amount']
    if not all (key in json for key in transaction_keys):
        return "some elements of the transactions are missing",400
    index=blockchain.add_transactions(json['sender'],json['receiver'],json['amount'])
    response={"message":f'This transactions will be added{index}'}
    return jsonify(response),201
#Connecting a new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
    if nodes is None:
        return "no Node",400
    for node in nodes:
        blockchain.add_node(node)
    response={"message":"All the node are connected ","total_nodes":list(blockchain.nodes)}
    return jsonify(response),201
#Repalce  chain with a longest_chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced:
        response={"message":"Node  has diffrent chain so that was repalced by longest one",
                  "new_chain":blockchain.chain}
    else:
        response={"message":"All Good the chain is largest one","actual_chain":blockchain.chain}
    return jsonify(response),200
    
    

app.run(host = '0.0.0.0',port=5000)
# Decentralization of Blockchain

            
        


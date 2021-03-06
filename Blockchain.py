#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#region import
import datetime
import hashlib
import json
import requests # pip install requests
from urllib.parse import urlparse
#endregion


#region Blockchain  
class Blockchain(object):
    def __init__(self) -> None:
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.new_block(previous_hash="MetalicamenteDePutaMadre", proof=1)
    def new_block(self, proof:int , previous_hash:str) -> dict:
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block
    def get_previous_block(self) -> dict:
        return self.chain[-1]
    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha3_512(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    def hash(self, block: dict) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha3_512(encoded_block).hexdigest()
    def is_chain_valid(self, chain: list) -> bool:
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha3_512(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    def add_transaction(self, Mtype: str, company: str, client: str, taskCode: str, deadline: str,  amount: int, currency: str) -> int:
        self.current_transactions.append({
            'type': Mtype,
            'company': company,
            'client': client,
            'taskcode': taskCode,
            'deadline': deadline,
            'amount': amount,
            'currency': currency
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    def add_node(self, address : str) -> None:
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    def replace_chain(self) -> bool:
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
#endregion
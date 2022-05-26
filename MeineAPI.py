#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#region imports
from flask import Flask, jsonify, request # pip install Flask
from uuid import uuid4
import json
import requests # pip install requests
from urllib.parse import urlparse
from flask_ngrok import run_with_ngrok # pip install flask-ngrok
from Blockchain import*
#endregion

#region Global Variables
MeineAPI = Flask(__name__)
run_with_ngrok(MeineAPI)
node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()
#endregion

#region MeineAPI_Methods
@MeineAPI.route('/mine_block', methods=['GET'])
def mine_block() -> str:
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(Mtype='contract', company='Z', client=node_address, taskCode='MDPM-001', deadline='2023-05-27 05:30:00', amount=1, currency='P')
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@MeineAPI.route("/get_chain", methods=['GET'])
def get_chain() -> str:
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@MeineAPI.route("/is_valid", methods=['GET'])
def is_valid() -> str:
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

@MeineAPI.route("/add_transaction", methods=['POST'])
def add_transaction() -> str:
    json = request.get_json()
    transaction_keys = ['type', 'company', 'client', 'taskcode', 'deadline', 'amount', 'currency']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['type'], json['company'], json['client'], json['taskcode'], json['deadline'], json['amount'], json['currency'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@MeineAPI.route('/connect_node', methods=['POST'])
def connect_node() -> str:
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes:',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@MeineAPI.route('/replace_chain', methods=['GET'])
def replace_chain() -> str:
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'new_chain': blockchain.chain}
    return jsonify(response), 200
#endregion

MeineAPI.run()
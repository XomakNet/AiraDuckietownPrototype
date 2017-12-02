#!/usr/bin/env python

import ipfsapi
import time

from web3 import HTTPProvider
from web3 import Web3

from core.contracts import RobotLiabilityFactoryContract, RobotLiabilityContract
from core.utils import MultihashConverter

__author__ = 'Xomak'


web3_rpc_url = "http://localhost:8545/"
factory_contract_address = "0x12301cb37191136a70c2cb8c5ec1240b69ad3668"
sender_address = "0x7262e87595e3bb70f31cc465b28b2b8b2355faa3"

active_liability = None
web3 = Web3(HTTPProvider(web3_rpc_url, request_kwargs={'timeout': 60}))
ipfs_client = ipfsapi.connect()

factory_contract = RobotLiabilityFactoryContract(web3, factory_contract_address, sender_address)
active_liabilities = []


def callback(block):
    print("New block")
    new_contracts = factory_contract.get_new_contracts(sender_address)
    for contract_address in new_contracts:
        print("New contract: "+contract_address)
        active_liabilities.append(RobotLiabilityContract(web3, contract_address, sender_address))

    for liability in active_liabilities:
        objective = liability.get_objective()
        if objective is not None:
            print("We have objective: "+objective)

new_block_filter = web3.eth.filter('latest')
new_block_filter.watch(callback)

while True:
    time.sleep(1)

#!/usr/bin/env python3
import argparse

import ipfsapi
import time
import tempfile
import os

from web3 import HTTPProvider
from web3 import Web3

from core import settings
from core.contracts import RobotLiabilityFactoryContract, RobotLiabilityContract
from core.objective_extractor import ObjectiveExtractor
from core.result_extractor import ResultExtractor

from validator.validate import *

web3_rpc_url = settings.WEB3_RPC_URL
factory_contract_address = settings.WEB3_RPC_URL


active_liabilities = []


def make_validation(liability):
    objective = liability.get_objective()
    result = liability.get_result()

    model = ObjectiveExtractor(ipfs_client).get_robot_model(objective)
    model_path, _ = tempfile.mkstemp()
    os.write(model_path, model)
    os.close(model_path)

    log = ResultExtractor(ipfs_client).get_log(result)
    log_path, _ = tempfile.mkstemp()
    os.write(log_path, log)
    os.close(log_path)

    if validate(model_path, log_path, DEFAULT_PRISM_PATH, PropertyType.WEAK) == 0:
        liability.confirm_result()
    else:
        liability.reject_result()

    os.remove(model_path)
    os.remove(log_path)

def callback(block):
    print("New block")
    new_contracts = factory_contract.get_new_contracts(sender_address)
    for contract_address in new_contracts:
        print("New contract: "+contract_address)
        active_liabilities.append(RobotLiabilityContract(web3, contract_address, sender_address))

    validated_liabilities = []
    for liability in active_liabilities:
        result = liability.get_result()
        if result is not None:
            print("We have result to validate: " + result)
            make_validation(liability)
            validated_liabilities.append(liability)

    for liability in validated_liabilities:
        active_liabilities.remove(liability)


parser = argparse.ArgumentParser()

parser.add_argument('--account', help='Validator\'s account', dest='address', type=str, required=True)

args = parser.parse_args()
sender_address = args.address

if sender_address is not None:
    active_liability = None
    web3 = Web3(HTTPProvider(web3_rpc_url, request_kwargs={'timeout': 60}))
    ipfs_client = ipfsapi.connect()

    factory_contract = RobotLiabilityFactoryContract(web3, factory_contract_address, sender_address)
    new_block_filter = web3.eth.filter('latest')
    new_block_filter.watch(callback)

    while True:
        time.sleep(1)

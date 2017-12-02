#!/usr/bin/env python
import argparse
import ipfsapi

from web3 import HTTPProvider
from web3 import Web3
from core.contracts import RobotLiabilityFactoryContract, RobotLiabilityContract
from core.data_publisher import IPFSConnector
from core.objective_generator import ObjectiveGenerator
from core import settings as settings

__author__ = 'Xomak'

parser = argparse.ArgumentParser()

parser.add_argument('--client', help='Client address', dest='client', type=str, required=True)
parser.add_argument('--car', help='Car address', dest='car', type=str, required=True)
parser.add_argument('--actions', help='Route action', nargs='+', required=True)

args = parser.parse_args()

web3 = Web3(HTTPProvider(settings.WEB3_RPC_URL, request_kwargs={'timeout': 60}))
ipfs_client = ipfsapi.connect()

sender_address = args.client.lower()
car_address = args.car.lower()
factory_address = settings.FACTORY_CONTRACT_ADDRESS.lower()
service_contract = RobotLiabilityFactoryContract(web3, factory_address, sender_address)

print("Creating contract...")
contract_address = service_contract.create_liability(bytes(0), 1, sender_address, car_address)
print("Created: %s" % contract_address)

signs_list = []

for action in args.actions:
    signs_list.append(action.split(':'))

ipfs_connector = IPFSConnector(ipfs_client)
print("Generating objective and publishing to IPFS...")
objective_hash = ipfs_connector.create_objective(signs_list)
print("Published: %s" % objective_hash)

if objective_hash is not None:
    print("Set objective...")
    contract = RobotLiabilityContract(web3, contract_address, sender_address)
    contract.set_objective(objective_hash)
    print("Finished.")

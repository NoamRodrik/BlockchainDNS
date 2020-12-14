import time
from web3 import Web3, HTTPProvider
import json

contract_address     = "0x440bf216C419A1EEA047250bb4885A1ceFEb9FC3"
wallet_private_key   = "f3580b39cfcafbcdad850f1c092e8729b40ad07ed771ff180dccafaee7851e82"
wallet_address       = "0xCfB75984d2003DF710530b6cA94247cbe34c303D"
url = "http://127.0.0.1:7545"

w3 = Web3(HTTPProvider(url))
w3.eth.defaultAccount = w3.eth.accounts[0]

abi = json.loads('''[{"constant":false,"inputs":[{"name":"newAddress","type":"string"}],"name":"setAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getCreator","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getURL","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getAddress","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newCreator","type":"address"}],"name":"setCreator","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"entry","outputs":[{"name":"ip","type":"string"},{"name":"url","type":"string"},{"name":"dateOfCreation","type":"uint256"},{"name":"expireTimeAmount","type":"uint256"},{"name":"creator","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newURL","type":"string"}],"name":"setURL","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"constructor","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newDateOfCreation","type":"uint256"}],"name":"setDateOfCreation","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newExpireTimeAmount","type":"uint256"}],"name":"setExpireTimeAmount","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getDateOfCreation","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getExpireTimeAmount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]''')
contract = w3.eth.contract(address=contract_address, abi=abi)

tx_hash = contract.functions.setURL("BCD.com").transact()
w3.eth.waitForTransactionReceipt(tx_hash)
tx_hash = contract.functions.setExpireTimeAmount(1).transact()
w3.eth.waitForTransactionReceipt(tx_hash)
tx_hash = contract.functions.setAddress("142.250.74.206").transact()
w3.eth.waitForTransactionReceipt(tx_hash)

contract = w3.eth.contract(address=contract_address, abi=abi)

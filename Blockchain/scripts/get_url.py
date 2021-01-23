import time
from web3 import Web3, HTTPProvider
import json
import sys
import datetime

contract_address     = "0x7E9B3758D7FE3699449d0029A55483A77eE1efcf"
wallet_private_key   = "bf15adc8c2b23e09b0ce81ea09495b2ea40864627133ab0f736e8009d3088121"
wallet_address       = "0xA33AfE1FC2FFbE5c41a0f6c52548c2B71391cD52"
url = "http://10.10.248.102:7545"

w3 = Web3(HTTPProvider(url))
w3.eth.defaultAccount = w3.eth.accounts[0]

abi = json.loads('''[{"constant":false,"inputs":[{"name":"newAddress","type":"string"}],"name":"setAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getCreator","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getURL","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getAddress","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newCreator","type":"address"}],"name":"setCreator","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"entry","outputs":[{"name":"ip","type":"string"},{"name":"url","type":"string"},{"name":"dateOfCreation","type":"uint256"},{"name":"expireTimeAmount","type":"uint256"},{"name":"creator","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newURL","type":"string"}],"name":"setURL","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newDateOfCreation","type":"uint256"}],"name":"setDateOfCreation","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newExpireTimeAmount","type":"uint256"}],"name":"setExpireTimeAmount","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getDateOfCreation","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getExpireTimeAmount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]''')

def _add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def fetch_dns(requested_url : str = "") -> str:
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # TODO: Parse requested_url for URL in HashTable
    date = datetime.datetime.fromtimestamp(datetime.datetime.utcnow().timestamp())
    expire = contract.functions.getExpireTimeAmount().call()
    creation = datetime.datetime.fromtimestamp(contract.functions.getDateOfCreation().call())

    expire_date = _add_years(creation, expire)
    if date < expire_date:
        return contract.functions.getAddress().call()

    # Failure
    return ""


# TEST CALL:
print(fetch_dns("BCD2.com"))

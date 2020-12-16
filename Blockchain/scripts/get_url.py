import time
from web3 import Web3, HTTPProvider
import json
import sys
import datetime

contract_address     = "0x5054f6D117E71a374F4C2b5Cd8508fA578aF439D"
wallet_private_key   = "d5e56c6fbb9441cc7c3e996ed1c5d785d96b665482c7f34e08e11249ad2a36ce"
wallet_address       = "0xBAb3632832DAdD4338dbB17227521b13FeD38c76"
url = "http://127.0.0.1:7545"

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
#fetch_dns("BCD2.com")

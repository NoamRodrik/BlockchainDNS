import json
from web3 import Web3, HTTPProvider

import consts


class BlockchainDns():
    def __init__(self, node_url: str = consts.DEFAULT_NODE_URL, contract_address: str = None, abi: str = None, account: str = None) -> None:
        with open(consts.CONTRACT_DEPLOYMENT_INFO_PATH, 'rt') as f:
            data = json.load(f)
            abi = abi or data['abi']
            contract_address = contract_address or list(data['networks'].values())[0]['address']
        self.w3 = Web3(HTTPProvider(node_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)

        self.w3.eth.defaultAccount = account or self.w3.eth.accounts[0]

    def calculateReservationTime(self, domainName: str, paymentAmount: int) -> int:
        return self.contract.functions.calculateReservationTime(domainName, paymentAmount).call()

    def isDomainNameReserved(self, domainName: str) -> bool:
        return self.contract.functions.isDomainNameReserved(domainName).call()

    def reserveDomainName(self, domainName: str, paymentAmount: int) -> None:
        tx_hash = self.contract.functions.reserveDomainName(domainName).transact({'value': paymentAmount})
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def extendDomainNameReservation(self, domainName: str, paymentAmount: int) -> None:
        tx_hash = self.contract.functions.extendDomainNameReservation(domainName).transact({'value': paymentAmount})
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def releaseDomainName(self, domainName: str) -> None:
        tx_hash = self.contract.functions.releaseDomainName(domainName).transact()
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def pullDeposit(self) -> None:
        tx_hash = self.contract.functions.pullDeposit().transact()
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def setDomainAddress(self, domainName: str, domainAddress: str) -> None:
        tx_hash = self.contract.functions.setDomainAddress(domainName, domainAddress).transact()
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def setCustomDomainAddress(self, domainName: str, customDomainAddress: str) -> None:
        tx_hash = self.contract.functions.setCustomDomainAddress(domainName, customDomainAddress).transact()
        self.w3.eth.waitForTransactionReceipt(tx_hash)

    def getDomainAddress(self, domainName: str) -> str:
        return self.contract.functions.getDomainAddress(domainName).call()

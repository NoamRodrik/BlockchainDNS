# Blockchain DNS

## Setup a VM

Blockchain Ledger VM Install:
https://drive.google.com/file/d/1Jf55FoD9BSrN9vJaul9ct97CYkXR0Dls/view?usp=sharing

Snapshot:
https://drive.google.com/file/d/1uiBftLOV0Yz7yBsnY0ldqGAYgzStDll_/view?usp=sharing

## Setup localy

### Setup Python

Download and install Python from: https://www.python.org/downloads/.  
You may also need Microsoft C++ Build Tools, install it from: https://visualstudio.microsoft.com/visual-cpp-build-tools.

Install the following packages:

```
python -m pip install -U dnslib web3
```

### Setup Truffle

Download and install NPM from: https://nodejs.org/en/download/.

Install the following packages:

```
npm install -g truffle
```

### Setup Ganache

Download and install Ganache from: https://www.trufflesuite.com/ganache.

Launch Ganache and select `new workspace (Ether)`, then fill the following:

- WORKSPACE NAME = `BlockchainDNS`.
- TRUFFLE PROJECTS = `${WORKSPACE}/Blockchian/truffle-config.js`.
- IP = `localhost`.
- PORT = 7545.

### Deploy contracts

In order to deploy the contracts to Ganache run the commands:

```bash
cd Blockcain
truffle compile
truffle migrate
```

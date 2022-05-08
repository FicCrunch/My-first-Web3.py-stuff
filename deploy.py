# Smart contracts come to life on a blockcahin
# oracles help blockchains to relate with real world data
# block explorers: Like etherscan they allow you to view transactions about an account(by address,0x....)
# The more ETH you get the more gas you pay
# the gas limit: if i send some ETH to someone, if it is going to cost me more than 21000 gas then don't do it(21000 gas is the gas limit)
# gas price: how much it const per unit of gas
# txn fee: gas used * gas price
# hash: a unique fixed length string meant to identify a piece of data. they are created by putting some pice of data into a hash function
#


from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv
# from web3.middleware import geth_poa_middleware


load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            },
        },
    },
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

######################--DEPLOYING CONTRACTS--##############################
# get bycode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to rinkeby
w3 = Web3(Web3.HTTPProvider(""))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
chain_id = 4

my_address = "0xAfc285c75395D7fba5E20E04CCa96bee8bE02373"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. build a transaction
# 2. sign a transaction
# 3. send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying contract")

# send it
# hash is the lengthed encryted form of your message

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Deployed!')

######################--WORKING(UPDATING) WITH CONTRACTS--##############################
# working with the contract, you need
# contract abi
# contract address

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call -> simulate making the call and getting a return value, don't make state-changes
#                                       ^
# transact - make state changes         |
# remember: calls are just simulations --

# Initial value of favoriteNumber
# Just calling NOT TRANSACTING
print(simple_storage.functions.retrieve().call())
print('Updating contract')
print(simple_storage.functions.store(15).call())

# store the transaction
# if you want to just call then .call()
# if you want to transact then buildTransaction(id, your address, nonce - (nonce + 1))
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainid": chain_id, "from": my_address, "nonce": nonce + 1}
)

# sign it
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# send it
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

# wait for the transaction to finish
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print('Updated')
print(simple_storage.functions.retrieve().call())

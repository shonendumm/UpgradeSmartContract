from brownie import accounts, network, config
from web3 import Web3
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"] 


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts[id]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    # using metamask wallet
    return accounts.add(config["wallets"]["from_key"])

# initializer=box.store, 1, 2, 3, 4, 5
def encode_function_data(initializer=None, *args):
    # there's a bug if args == 0,
    # we check if initializer is None or args == 0
    if len(args) == 0 or not initializer:
        # return nothing or zero in hex
        return eth_utils.to_bytes(hexstr="0x")
    # brownie has a function that encodes it and returns the encode bytes
    return initializer.encode_input(*args)

def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    transaction = None
    # check if there's a admin contract for the proxy
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(proxy.address, new_implementation_address, {"from": account})
    # If no admin contract for the proxy, we can just upgrade on the proxy
    else:
        if initializer:
                encoded_function_call = encode_function_data(initializer, *args)
                transaction = proxy.upgradeAndCall(new_implementation_address, encoded_function_call,{"from": account})
        else:
            transaction = proxy.upgrade(new_implementation_address, {"from": account})

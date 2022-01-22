from scripts.helpful_scripts import get_account, encode_function_data
from brownie import network, Box, BoxV2, ProxyAdmin

def main():
    account = get_account()
    print(f"deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    # print(box.increment())

    # the contract that controls the proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})

    
    # if box.store is the constructor function we want to call with arg 1, then use
    # initializer = box.store, 1
    # box_encoded_initializer_function = encode_function_data(initializer, 1)
    # where we need to encode the initial function data first
    # but here we are not doing any constructor function
    box_encoded_initializer_function = encode_function_data()
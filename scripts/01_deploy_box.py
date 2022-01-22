from scripts.helpful_scripts import get_account, encode_function_data
from brownie import network, Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract

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
    # but here we are not doing any initializer function
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000_000}
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to V2!")
    # Proxy deployed, but we assign the Box abi to the proxy address, so that we can call its functions
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(13, {"from": account})
    print(proxy_box.retrieve())
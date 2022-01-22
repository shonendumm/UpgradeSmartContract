from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, BoxV2
from brownie import exceptions
import pytest

def test_contract_upgrade():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000_000}
    )

    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    # there's a bug with ganache-cli which won't raise the VirtualMachineError
    # need to start Ganache GUI app first, then run this test for exceptions
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
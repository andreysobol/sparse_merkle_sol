#!/usr/bin/env python

from brownie import PublicSpt, accounts

def main():
    tree = PublicSpt.deploy(10, {"from": accounts[0]})

    gas_used_add = []
    for item in range(0, 1024):
        tx = tree._addElement(item, b'apple')
        gas_used_add.append(tx.gas_used)

    gas_used_remove = []
    for item in range(0, 1024):
        tx = tree._removeElement(item)
        gas_used_remove.append(tx.gas_used)

    print("ADD")
    print("Median: ")
    print(sorted(gas_used_add)[512])
    print("Average: ")
    print(sum(gas_used_add)/1024)
    print("Min: ")
    print(min(gas_used_add))
    print("Max: ")
    print(max(gas_used_add))
    print("")
    print("REMOVE")
    print("Median: ")
    print(sorted(gas_used_remove)[512])
    print("Average: ")
    print(sum(gas_used_remove)/1024)
    print("Min: ")
    print(min(gas_used_remove))
    print("Max: ")
    print(max(gas_used_remove))

    kv = {
        "gas_used_add": gas_used_add,
        "gas_used_remove": gas_used_remove,
    }

    import json
    with open('raw_data.json', 'w') as f:
        json.dump(kv, f)
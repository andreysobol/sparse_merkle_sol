#!/usr/bin/env python

from brownie import PublicSpt, accounts

def main():
    tree = PublicSpt.deploy(10, {"from": accounts[0]})

    gas_used = []
    for item in range(0, 1024):
        tx = tree._modifyElement(item, b'apple')
        gas_used.append(tx.gas_used)

    print("Median: ")
    print(sorted(gas_used)[512])
    print("Average: ")
    print(sum(gas_used)/1024)
    print("Min: ")
    print(min(gas_used))
    print("Max: ")
    print(max(gas_used))
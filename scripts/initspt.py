#!/usr/bin/env python

from brownie import PublicSmtSha, accounts

def main():
    tree = PublicSmtSha.deploy(40, {"from": accounts[0]})
    tx0 = tree._addElement(0, b"1")
    tx1 = tree._decreaseDepth(20)
    tx2 = tree._increaseDepth(20)
    print(tx1.gas_used + tx2.gas_used)

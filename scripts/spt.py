#!/usr/bin/env python

from brownie import PublicSpt, accounts

def main():
    c = PublicSpt.deploy(20, {'from': accounts[0]})
    t = c._modifyElement(0, b'a'*96)
    print('Modify element:', t.gas_used)

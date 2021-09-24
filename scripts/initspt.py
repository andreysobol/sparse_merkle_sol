#!/usr/bin/env python

from brownie import PublicSpt, accounts

def main():
    tree = PublicSpt.deploy(40, {"from": accounts[0]})


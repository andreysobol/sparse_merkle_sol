#!/usr/bin/env python

from brownie import PublicSha256Spt, accounts

def main():
    tree = PublicSha256Spt.deploy(40, {"from": accounts[0]})


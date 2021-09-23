#!/usr/bin/env python

from brownie import PublicSpt, accounts

def main():
    tree = PublicSpt.deploy(2, {"from": accounts[0]})

    tree._modifyElement(0, b'apple')
    elements = [b''] * 4
    elements[0] = b'apple'

    print('level 0')
    for i in range(4):
        print(tree.tree(0, i))

    print('level 1')
    for i in range(2):
        print(tree.tree(1, i))

    print('level 2')
    for i in range(1):
        print(tree.tree(2, i))
    # assert '0x' + root.hex() == tree.getRoot()

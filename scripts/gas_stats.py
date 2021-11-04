#!/usr/bin/env python

from brownie import PublicSmtKeccak, PublicSmtSha, accounts
import os
import json

def print_stats(label, stats, leafs):
    print(label)
    print("Median:  ", sorted(stats)[leafs // 2])
    print("Average: ", sum(stats) // leafs)
    print("Min:     ", min(stats))
    print("Max:     ", max(stats))
    print()

def gas_stats(hashname, depth):
    print(f'HASH  = {hashname}')
    print(f'DEPTH = {depth}')

    contract = PublicSmtKeccak if hashname == 'keccak' else PublicSmtSha
    tree = contract.deploy(depth, {"from": accounts[0]})

    gas_used_add = []
    for item in range(2**depth):
        tx = tree._addElement(item, b'apple')
        gas_used_add.append(tx.gas_used)

    gas_used_remove = []
    for item in range(2**depth):
        tx = tree._removeElement(item)
        gas_used_remove.append(tx.gas_used)

    print_stats("--- ADD ---", gas_used_add, 2**depth)
    print_stats("-- REMOVE --", gas_used_remove, 2**depth)

    kv = {
        "gas_used_add": gas_used_add,
        "gas_used_remove": gas_used_remove,
    }

    with open(f'raw_data_{hashname}.json', 'w') as f:
        json.dump(kv, f)

def main():
    hashname = os.environ.get('HASH')
    if hashname not in ['sha', 'keccak']:
        print('$HASH has to be either "sha" or "keccak"')
        exit(1)

    depth = int(os.environ.get('DEPTH', 10))
    gas_stats(hashname, depth)

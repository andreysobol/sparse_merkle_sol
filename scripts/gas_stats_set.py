#!/usr/bin/env python

from brownie import PublicSmtSetKeccak, PublicSmtSetSha, accounts
from hashlib import sha256
import os
import json

def print_stats(label, stats, leafs):
    print(label)
    print("Median:  ", sorted(stats)[leafs // 2])
    print("Average: ", sum(stats) // leafs)
    print("Min:     ", min(stats))
    print("Max:     ", max(stats))
    print()

def deterministic_random(seed, r):
    hb = sha256(seed).digest()
    long = int.from_bytes(hb, 'big')
    lr = list(r)
    i = long % len(lr) 
    return (
        hb,
        lr[i],
    )

def gas_stats(hashname, depth):
    print(f'HASH  = {hashname}')
    print(f'DEPTH = {depth}')

    contract = PublicSmtSetKeccak if hashname == 'keccak' else PublicSmtSetSha
    tree = contract.deploy(depth, {"from": accounts[0]})

    gas_used_add = []
    for _ in range(2**depth):
        tx = tree.addToNextEmpty(b'apple')
        gas_used_add.append(tx.gas_used)

    gas_used_remove_last = []
    for item in range(2**depth):
        last = 2**depth - 1 - item
        tx = tree.removeAndRebase(last)
        gas_used_remove_last.append(tx.gas_used)

    contract = PublicSmtSetKeccak if hashname == 'keccak' else PublicSmtSetSha
    tree = contract.deploy(depth, {"from": accounts[0]})

    for _ in range(2**depth):
        tx = tree.addToNextEmpty(b'apple')

    gas_used_remove_random = []
    seed = b"seed"
    for item in range(2**depth):
        r = range(0, 2**depth - item)
        seed, index = deterministic_random(seed, r)
        tx = tree.removeAndRebase(index)
        gas_used_remove_random.append(tx.gas_used)

    print_stats("------ ADD ------", gas_used_add, 2**depth)
    print_stats("-- REMOVE LAST --", gas_used_remove_last, 2**depth)
    print_stats("- REMOVE RANDOM -", gas_used_remove_random, 2**depth)

    kv = {
        "gas_used_add": gas_used_add,
        "gas_used_remove_last": gas_used_remove_last,
        "gas_used_remove_random": gas_used_remove_random,
    }

    with open(f'raw_data_set_{hashname}.json', 'w') as f:
        json.dump(kv, f)

def main():
    hashname = os.environ.get('HASH')
    if hashname not in ['sha', 'keccak']:
        print('$HASH has to be either "sha" or "keccak"')
        exit(1)

    depth = int(os.environ.get('DEPTH', 10))
    gas_stats(hashname, depth)

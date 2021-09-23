from brownie import PublicSpt, accounts
import hashlib

import pytest

def test_setup_depth(public_spt, accounts):
    public_spt._setupDepth(1)
    root = public_spt.getRoot()
    empty_hash = hashlib.sha256(b'').digest()
    empty_root = '0x' + hashlib.sha256(empty_hash * 2).hexdigest()
    assert root == empty_root

def test_empty_roots(public_spt, accounts):
    check_size = range(1, 15)
    trees = { i: PublicSpt.deploy(i, {"from": accounts[0]}) for i in check_size }
    empty_hash = hashlib.sha256(b'').digest()
    for i in check_size:
        empty_hash = hashlib.sha256(empty_hash * 2).digest()
        assert trees[i].getRoot() == '0x' + empty_hash.hex()


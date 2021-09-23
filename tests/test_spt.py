from brownie import PublicSpt, accounts
from hashlib import sha256

import pytest

def get_root_4(elements):
    h_elements = [sha256(item).digest() for item in elements]
    left = sha256(h_elements[0] + h_elements[1]).digest()
    right = sha256(h_elements[2] + h_elements[3]).digest()
    root = sha256(left + right).digest()
    return root

def test_setup_depth(public_spt, accounts):
    root = public_spt.getRoot()
    empty_hash = sha256(b'').digest()
    empty_root = '0x' + sha256(empty_hash * 2).hexdigest()
    assert root == empty_root

def test_empty_roots(public_spt, accounts):
    check_size = range(1, 15)
    trees = { i: PublicSpt.deploy(i, {"from": accounts[0]}) for i in check_size }
    empty_hash = sha256(b'').digest()
    for i in check_size:
        empty_hash = sha256(empty_hash * 2).digest()
        assert trees[i].getRoot() == '0x' + empty_hash.hex()

def test_one_element(public_spt, accounts):

    trees = [PublicSpt.deploy(2, {"from": accounts[0]}) for i in range(4)]

    for i in range(4):
        trees[i]._modifyElement(i, b'apple')
        elements = [b''] * 4
        elements[i] = b'apple'
        root = get_root_4(elements)
        assert '0x' + root.hex() == trees[i].getRoot()

def test_element_hash(public_spt, accounts):
    public_spt._modifyElement(0, b'apple')
    apple_hash = public_spt.tree(0, 0)
    assert apple_hash == '0x' + sha256(b'apple').hexdigest()


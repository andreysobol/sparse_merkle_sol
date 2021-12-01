from brownie import PublicSmtSetSha, SMTSha, accounts
from hashlib import sha256

import pytest

def get_root_4(elements):
    h_elements = [sha256(item).digest() for item in elements]
    left = sha256(h_elements[0] + h_elements[1]).digest()
    right = sha256(h_elements[2] + h_elements[3]).digest()
    root = sha256(left + right).digest()
    return '0x' + root.hex()

#def test_setup_depth(public_spt, accounts):
#    root = public_spt.getRoot()
#    empty_hash = sha256(b'').digest()
#    empty_root = '0x' + sha256(empty_hash * 2).hexdigest()
#    assert root == empty_root

#def test_empty_roots(accounts):
#    check_size = range(1, 15)
#    trees = { i: PublicSmtSetSha.deploy(i, 20, {"from": accounts[0]}) for i in check_size }
#    empty_hash = sha256(b'').digest()
#    for i in check_size:
#        empty_hash = sha256(empty_hash * 2).digest()
#        assert trees[i].getRoot() == '0x' + empty_hash.hex()

def test_empty(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    empty_hash = sha256(b'').digest()
    empty_root = '0x' + sha256(empty_hash * 2).hexdigest()
    assert contract.getRoot() == empty_root

def test_empty_depth(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    assert contract.getDepth() == 1

def test_add_element(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    assert contract.getDepth() == 1
    assert contract.getFirstEmptySlot() == 0
    contract.addToNextEmpty(b"apple")
    assert contract.getFirstEmptySlot() == 1
    root = '0x' + sha256(sha256(b'apple').digest() + sha256(b'').digest()).hexdigest()
    assert contract.getRoot() == root

def test_remove_element(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    assert contract.getDepth() == 1
    assert contract.getFirstEmptySlot() == 0
    contract.addToNextEmpty(b"apple")
    assert contract.getFirstEmptySlot() == 1
    root = '0x' + sha256(sha256(b'apple').digest() + sha256(b'').digest()).hexdigest()
    assert contract.getRoot() == root
    contract.removeAndRebase(0)
    empty_hash = sha256(b'').digest()
    empty_root = '0x' + sha256(empty_hash * 2).hexdigest()
    assert contract.getRoot() == empty_root
    assert contract.getFirstEmptySlot() == 0
    assert contract.getDepth() == 1

def test_remove_last(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    contract.addToNextEmpty(b"apple")
    contract.addToNextEmpty(b"fish")
    contract.addToNextEmpty(b"banana")
    contract.addToNextEmpty(b"ice")
    assert contract.getRoot() == get_root_4([b"apple", b"fish", b"banana", b"ice"])
    contract.removeAndRebase(3)
    assert contract.getRoot() == get_root_4([b"apple", b"fish", b"banana", b""])

def test_remove_first(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    contract.addToNextEmpty(b"apple")
    contract.addToNextEmpty(b"fish")
    contract.addToNextEmpty(b"banana")
    contract.addToNextEmpty(b"ice")
    assert contract.getRoot() == get_root_4([b"apple", b"fish", b"banana", b"ice"])
    contract.removeAndRebase(0)
    assert contract.getRoot() == get_root_4([b"ice", b"fish", b"banana", b""])

def test_remove_second(accounts):
    contract = PublicSmtSetSha.deploy(10, {"from": accounts[0]})
    contract.addToNextEmpty(b"apple")
    contract.addToNextEmpty(b"fish")
    contract.addToNextEmpty(b"banana")
    contract.addToNextEmpty(b"ice")
    assert contract.getRoot() == get_root_4([b"apple", b"fish", b"banana", b"ice"])
    contract.removeAndRebase(1)
    assert contract.getRoot() == get_root_4([b"apple", b"ice", b"banana", b""])
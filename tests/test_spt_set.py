from brownie import PublicSmtSetSha, SMTSha, accounts
from hashlib import sha256

import pytest
import math

def get_root_4(elements):
    h_elements = [sha256(item).digest() for item in elements]
    left = sha256(h_elements[0] + h_elements[1]).digest()
    right = sha256(h_elements[2] + h_elements[3]).digest()
    root = sha256(left + right).digest()
    return '0x' + root.hex()

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

def test_limit(accounts):
    contract = PublicSmtSetSha.deploy(4, {"from": accounts[0]})

    for i in range(0, 2**4):
        bs = b"just" + (b"bla" * i)
        contract.addToNextEmpty(bs)
        assert contract.getFirstEmptySlot() == i + 1

    reverted = False
    try:
        tx = contract.addToNextEmpty(b"try")
    except Exception as e:
        reverted = True
        assert "Index out of range" in e.message

    assert reverted

def test_sizes(accounts):
    contract = PublicSmtSetSha.deploy(8, {"from": accounts[0]})

    for exp in range(1, 8):

        for i in range(0, 2**exp):
            assert contract.getFirstEmptySlot() == i
            if i == 0 or i == 1:
                depth = 1
            else:
                depth = math.ceil(math.log2(i))
            bs = b"just" + (b"bla" * i)
            contract.addToNextEmpty(bs)
            assert contract.getFirstEmptySlot() == i + 1
            if i + 1 == 0 or i + 1 == 1:
                depth = 1
            else:
                depth = math.ceil(math.log2(i + 1))
            assert contract.getDepth() == depth

        for i in range(0, 2**exp):
            assert contract.getFirstEmptySlot() == 2**exp - i
            contract.removeAndRebase(0)
            q = 2**exp - i - 1
            assert contract.getFirstEmptySlot() == q 
            if q == 0 or q == 1:
                depth = 1
            else:
                depth = math.ceil(math.log2(q))
            assert contract.getDepth() == depth

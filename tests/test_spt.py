from brownie import PublicSmtSha, accounts
from hashlib import sha256

import pytest

def get_root_4(elements):
    h_elements = [sha256(item).digest() for item in elements]
    left = sha256(h_elements[0] + h_elements[1]).digest()
    right = sha256(h_elements[2] + h_elements[3]).digest()
    root = sha256(left + right).digest()
    return '0x' + root.hex()

def test_setup_depth(public_spt, accounts):
    root = public_spt._getRoot()
    empty_hash = sha256(b'').digest()
    empty_root = '0x' + sha256(empty_hash * 2).hexdigest()
    assert root == empty_root

def test_empty_roots(public_spt, accounts):
    check_size = range(1, 15)
    trees = { i: PublicSmtSha.deploy(i, {"from": accounts[0]}) for i in check_size }
    empty_hash = sha256(b'').digest()
    for i in check_size:
        empty_hash = sha256(empty_hash * 2).digest()
        assert trees[i]._getRoot() == '0x' + empty_hash.hex()

def test_one_element(public_spt, accounts):

    trees = [PublicSmtSha.deploy(2, {"from": accounts[0]}) for i in range(4)]

    for i in range(4):
        trees[i]._modifyElement(i, b'apple')
        elements = [b''] * 4
        elements[i] = b'apple'
        root = get_root_4(elements)
        assert root == trees[i]._getRoot()

def test_step_by_step(public_spt, accounts):
    spt = PublicSmtSha.deploy(2, {"from": accounts[0]})

    spt._modifyElement(0, b'apple')
    root = spt._getRoot()
    test_result = get_root_4([b'apple', b'', b'', b''])
    assert root == test_result

    spt._modifyElement(1, b'avocado')
    root = spt._getRoot()
    test_result = get_root_4([b'apple', b'avocado', b'', b''])
    assert root == test_result

    spt._modifyElement(2, b'clock')
    root = spt._getRoot()
    test_result = get_root_4([b'apple', b'avocado', b'clock', b''])
    assert root == test_result

    spt._modifyElement(3, b'great')
    root = spt._getRoot()
    test_result = get_root_4([b'apple', b'avocado', b'clock', b'great'])
    assert root == test_result

def test_remove(public_spt, accounts):
    spt = PublicSmtSha.deploy(2, {"from": accounts[0]})

    spt._modifyElement(1, b'fish')
    root = spt._getRoot()
    test_result = get_root_4([b'', b'fish', b'', b''])
    assert root == test_result

    spt._modifyElement(3, b'ice')
    root = spt._getRoot()
    test_result = get_root_4([b'', b'fish', b'', b'ice'])
    assert root == test_result

    spt._removeElement(1)
    root = spt._getRoot()
    test_result = get_root_4([b'', b'', b'', b'ice'])
    assert root == test_result


def test_remove_empty(public_spt, accounts):
    spt = PublicSmtSha.deploy(2, {"from": accounts[0]})
    reverted = False

    try:
        tx = spt._removeElement(1)
    except Exception as e:
        reverted = True
        assert "Can't remove empty element" in e.message

    assert reverted

def test_add_existing(public_spt, accounts):
    spt = PublicSmtSha.deploy(2, {"from": accounts[0]})
    reverted = False

    spt._addElement(1, b'apple')

    try:
        tx = spt._addElement(1, b'banana')
    except Exception as e:
        reverted = True
        assert "Element already exists" in e.message

    assert reverted

def test_incorrect_index(public_spt, accounts):
    spt = PublicSmtSha.deploy(2, {"from": accounts[0]})
    reverted = False

    try:
        tx = spt._addElement(4, b'banana')
    except Exception as e:
        reverted = True
        assert "Index out of bounds" in e.message

    assert reverted

def test_increase_depth(public_spt, accounts):
    spt = PublicSmtSha.deploy(1, {"from": accounts[0]})
    
    spt._addElement(0, b'apple')
    spt._addElement(1, b'banana')
    spt._increaseDepth(1)
    root = spt._getRoot()

    assert root == get_root_4([b'apple', b'banana', b'', b''])


def test_decrease_depth(public_spt, accounts):
    spt = PublicSmtSha.deploy(3, {"from": accounts[0]})
    
    spt._addElement(0, b'apple')
    spt._addElement(2, b'banana')
    spt._decreaseDepth(1)
    root = spt._getRoot()

    assert root == get_root_4([b'apple', b'', b'banana', b''])


def test_decrease_non_empty(public_spt, accounts):
    spt = PublicSmtSha.deploy(3, {"from": accounts[0]})

    tx = spt._addElement(2, b'banana')
    tx = spt._addElement(5, b'super banana')

    reverted = False

    try:
        tx = spt._decreaseDepth(1)
    except Exception as e:
        reverted = True
        assert "Subtree must be empty" in e.message

    assert reverted


def test_insert_and_decrease(public_spt, accounts):

    spt = PublicSmtSha.deploy(10, {"from": accounts[0]})
    spt._addElement(0, b"lol")

    elhash = sha256(b"lol").digest()
    empty = sha256(b"").digest()
    r = elhash
    for item in range(0, 10):
        r = sha256(r + empty).digest()
        empty = sha256(empty + empty).digest()
    
    assert spt._getRoot() == '0x' + r.hex()
    
    spt._decreaseDepth(9)

    assert spt._getRoot() == '0x' + sha256(sha256(b"lol").digest() + sha256(b"").digest()).hexdigest()
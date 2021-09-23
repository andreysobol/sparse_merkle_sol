from brownie import PublicSpt, accounts
import hashlib

import pytest

def test_setup_depth(public_spt, accounts):
    public_spt._setupDepth(1)
    root = public_spt.getRoot()
    empty_hash = hashlib.sha256(b'').digest()
    empty_root = '0x' + hashlib.sha256(empty_hash * 2).hexdigest()
    assert root == empty_root

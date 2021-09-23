from brownie import PublicSpt, accounts

import pytest

def test_create(public_spt, accounts):
    public_spt._setupDepth(20)

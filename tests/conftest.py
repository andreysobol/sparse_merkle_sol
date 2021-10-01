import pytest

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    pass

@pytest.fixture(scope="module")
def public_spt(PublicSmtSha, accounts):
    return PublicSmtSha.deploy(1, {'from': accounts[0]})

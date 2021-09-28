import pytest

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    pass

@pytest.fixture(scope="module")
def public_spt(PublicSha256Spt, accounts):
    return PublicSha256Spt.deploy(1, {'from': accounts[0]})

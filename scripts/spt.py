from brownie import Spt, accounts

def main():
    c = Spt.deploy({'from': accounts[0]})
    c.setupDepth(20)
    t = c.calculateEmptyLeafHash(20)
    print(t.gas_used)
    a = []
    for i in range(0, 1023):
        t = c.modifyHashedElement(i, '0xfcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9')
        a.append(t.gas_used)
    print(a)
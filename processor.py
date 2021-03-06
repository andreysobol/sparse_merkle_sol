#!/usr/bin/env python3

from functools import reduce

def ifcondition(contract):

    def split_one(st, spliter):
        sst = st.split(spliter)
        sstlenm1 = len(sst) - 1
        res = list(reduce(lambda x,y: x + list(y), zip(sst[:-1], [spliter]*sstlenm1), []) + [sst[-1]])
        return res
    
    ls = [contract]
    ls = list(reduce(lambda x,y: x + split_one(y, "{{ if SET }}"), ls, []))
    ls = list(reduce(lambda x,y: x + split_one(y, "{{ else }}"), ls, []))
    ls = list(reduce(lambda x,y: x + split_one(y, "{{ endif }}"), ls, []))

    if_is = [i for i in range(0, len(ls)) if ls[i] == "{{ if SET }}"]
    else_is = [i for i in range(0, len(ls)) if ls[i] == "{{ else }}"]
    endif_is = [i for i in range(0, len(ls)) if ls[i] == "{{ endif }}"]

    ranges = reduce(lambda x,y: x + y, [list(range(r[0], r[1] + 1)) for r in zip(else_is, endif_is)], [])
    toremove = ranges + if_is
    withset = [ls[i] for i in range(0, len(ls)) if not (i in toremove)]
    withset = "".join(withset)

    ranges = reduce(lambda x,y: x + y, [list(range(r[0], r[1] + 1)) for r in zip(if_is, else_is)], [])
    toremove = ranges + endif_is
    withoutset = [ls[i] for i in range(0, len(ls)) if not (i in toremove)]
    withoutset = "".join(withoutset)

    return (withset, withoutset)

with open("contracts/Smt.metasol") as smt:
    contract = smt.read()

with open("contracts/SmtSha.sol", 'w') as smt_sha:
    pre = contract.replace("{{hash}}", "sha256").replace("{{subcontractname}}", "Sha")
    (_, withoutset) = ifcondition(pre)
    smt_sha.write(withoutset)
    print("contracts/SmtSha.sol generated")

with open("contracts/SmtSetSha.sol", 'w') as set_smt_sha:
    pre = contract.replace("{{hash}}", "sha256").replace("{{subcontractname}}", "SetSha")
    (withset, _) = ifcondition(pre)
    set_smt_sha.write(withset)
    print("contracts/SmtSetSha.sol generated")

with open("contracts/SmtKeccak.sol", 'w') as smt_keccak:
    pre = contract.replace("{{hash}}", "keccak256").replace("{{subcontractname}}", "Keccak")
    (_, withoutset) = ifcondition(pre)
    smt_keccak.write(withoutset)
    print("contracts/SmtKeccak.sol generated")

with open("contracts/SmtSetKeccak.sol", 'w') as smt_keccak:
    pre = contract.replace("{{hash}}", "keccak256").replace("{{subcontractname}}", "SetKeccak")
    (withset, _) = ifcondition(pre)
    smt_keccak.write(withset)
    print("contracts/SmtSetKeccak.sol generated")

with open("contracts/PublicSmt.metasol") as p_smt:
    public_contract = p_smt.read()

with open("contracts/PublicSmtSha.sol", 'w') as p_smt_sha:
    p_smt_sha.write(public_contract.replace("{{subcontractname}}", "Sha"))
    print("contracts/PublicSmtSha.sol generated")

with open("contracts/PublicSmtKeccak.sol", 'w') as p_smt_keccak:
    p_smt_keccak.write(public_contract.replace("{{subcontractname}}", "Keccak"))
    print("contracts/PublicSmtKeccak.sol generated")

with open("contracts/PublicSmtSet.metasol") as p_smt:
    public_set_contract = p_smt.read()

with open("contracts/PublicSmtSetSha.sol", 'w') as p_smt_sha:
    p_smt_sha.write(public_set_contract.replace("{{subcontractname}}", "SetSha"))
    print("contracts/PublicSmtSetSha.sol generated")

with open("contracts/PublicSmtSetKeccak.sol", 'w') as p_smt_keccak:
    p_smt_keccak.write(public_set_contract.replace("{{subcontractname}}", "SetKeccak"))
    print("contracts/PublicSmtSetKeccak.sol generated")

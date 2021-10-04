#!/usr/bin/env python3

with open("contracts/Smt.metasol") as smt:
    contract = smt.read()

with open("contracts/SmtSha.sol", 'w') as smt_sha:
    smt_sha.write(contract.replace("{{hash}}", "sha256").replace("{{hashname}}", "Sha"))
    print("contracts/SmtSha.sol generated")

with open("contracts/SmtKeccak.sol", 'w') as smt_keccak:
    smt_keccak.write(contract.replace("{{hash}}", "keccak256").replace("{{hashname}}", "Keccak"))
    print("contracts/SmtKeccak.sol generated")

with open("contracts/PublicSmt.metasol") as p_smt:
    public_contract = p_smt.read()

with open("contracts/PublicSmtSha.sol", 'w') as p_smt_sha:
    p_smt_sha.write(public_contract.replace("{{hashname}}", "Sha"))
    print("contracts/PublicSmtSha.sol generated")

with open("contracts/PublicSmtKeccak.sol", 'w') as p_smt_keccak:
    p_smt_keccak.write(public_contract.replace("{{hashname}}", "Keccak"))
    print("contracts/PublicSmtKeccak.sol generated")

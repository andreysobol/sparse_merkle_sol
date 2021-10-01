with open("contracts/Smt.metasol") as smt:
    contract = smt.read()

with open("contracts/SmtSha.sol", 'w') as smt_sha:
    smt_sha.write(contract.replace("{{hash}}", "sha256"))
    print("contracts/SmtSha.sol generated")

with open("contracts/SmtKeccak.sol", 'w') as smt_keccak:
    smt_keccak.write(contract.replace("{{hash}}", "keccak256"))
    print("contracts/SmtKeccak.sol generated")

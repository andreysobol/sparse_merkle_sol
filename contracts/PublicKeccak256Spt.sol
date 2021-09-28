// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./PublicSpt.sol";

contract PublicKeccak256Spt is PublicSpt{
    constructor(uint _depth) PublicSpt(_depth) public {}

    function hash(bytes memory data) override internal returns (bytes32) {
        return keccak256(data);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./Spt.sol";

contract Keccak256Spt is Spt {

    constructor(uint _depth) Spt(_depth) public {}

    function hash(bytes memory data) override internal returns (bytes32) {
        return keccak256(data);
    }
}

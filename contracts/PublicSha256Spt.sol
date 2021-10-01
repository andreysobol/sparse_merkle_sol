// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./PublicSpt.sol";

contract PublicSha256Spt is PublicSpt {
    constructor(uint8 _depth) PublicSpt(_depth) public {}

    function hash(bytes memory data) override internal returns (bytes32) {
        return sha256(data);
    }
}

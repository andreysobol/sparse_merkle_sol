// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./Sha256Spt.sol";

contract PublicSpt is Sha256Spt {
    constructor(uint _depth) Sha256Spt(_depth) public {}

    function _increaseDepth(uint depthDifference) public {
        super.increaseDepth(depthDifference);
    }

    function _decreaseDepth(uint depthDifference) public {
        super.decreaseDepth(depthDifference);
    }

    function _modifyElement(uint index, bytes calldata element) public {
        super.modifyElement(index, element);
    }

    function _addElement(uint index, bytes calldata element) public {
        super.addElement(index, element);
    }

    function _removeElement(uint index) public {
        super.removeElement(index);
    }
}

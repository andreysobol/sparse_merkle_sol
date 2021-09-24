// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./Spt.sol";

contract PublicSpt is Spt {
    constructor(uint _depth) Spt(_depth) public {}

    function _setupDepth(uint depth) public {
        super.setupDepth(depth);
    }

    function _increaseDepth(uint depthDifference) public {
        super.increaseDepth(depthDifference);
    }

    function _decreaseDepth(uint depthDifference) public {
        super.decreaseDepth(depthDifference);
    }

    function _modifyHash(uint index, bytes32 hashedElement) public {
        super.modifyHash(index, hashedElement);
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

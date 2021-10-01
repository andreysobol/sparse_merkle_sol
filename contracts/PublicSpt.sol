// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./Spt.sol";

abstract contract PublicSpt is Spt {
    constructor(uint8 _depth) Spt(_depth) {}

    function _increaseDepth(uint8 depthDifference) public {
        super.increaseDepth(depthDifference);
    }

    function _decreaseDepth(uint8 depthDifference) public {
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

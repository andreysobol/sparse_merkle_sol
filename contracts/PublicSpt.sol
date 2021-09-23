// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import './Spt.sol';

contract PublicSpt is Spt {


    function _setupDepth(uint depth) public {
        super.setupDepth(depth);
    }

    function _increaseDepth(uint amountOfLevel) public {
        super.increaseDepth(amountOfLevel);
    }

    function _decreaseDepth(uint amountOfLevel) public {
        super.decreaseDepth(amountOfLevel);
    }

    function _modifyHashedElement(uint index, bytes32 hashedElement) public {
        super.modifyHashedElement(index, hashedElement);
    }

}

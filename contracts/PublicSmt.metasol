// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

import "./Spt.sol";

contract PublicSpt {
    using SMT for SMT.MerkleTree;
    SMT.MerkleTree public tree;

    constructor(uint8 _depth) {
        tree.initialize(_depth);
    }

    function _increaseDepth(uint8 depthDifference) public {
        tree.increaseDepth(depthDifference);
    }

    function _decreaseDepth(uint8 depthDifference) public {
        tree.decreaseDepth(depthDifference);
    }

    function _modifyElement(uint index, bytes calldata element) public {
        tree.modifyElement(index, element);
    }

    function _addElement(uint index, bytes calldata element) public {
        tree.addElement(index, element);
    }

    function _removeElement(uint index) public {
        tree.removeElement(index);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract Spt {
    mapping(uint256 => bytes32) public cacheEmptyValues;

    uint public depth;
    uint public maxElements;

    // tree level => index inside level => element hash
    mapping(uint256 => mapping(uint256 => bytes32)) public tree;
    mapping(uint256 => bytes) public elementData; 

    bytes32 constant internal EMPTY_LEAF = 0x00;

    constructor(uint _depth) public {
        require(_depth > 0, "Depth must be non-zero");
        setupDepth(_depth);
        calculateEmptyLeafHash(0, _depth);
    }

    function setupDepth(uint _depth) internal {
        depth = _depth;
        maxElements = 2**depth;
    }

    function increaseDepth(uint depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint oldDepth = depth;
        require(depthDifference < uint256(-1) - oldDepth, "Overflow protection");
        uint newDepth = oldDepth + depthDifference;

        calculateEmptyLeafHash(oldDepth+1, newDepth);

        for (uint level = oldDepth+1; level <= newDepth; level++) {
            updateLeaf(level, 0);
        }
        setupDepth(newDepth);
    }

    function decreaseDepth(uint depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint oldDepth = depth;
        require(depthDifference < oldDepth, "Overflow protection");
        uint newDepth = oldDepth - depthDifference;

        for (uint level = newDepth; level < oldDepth; level++) {
            require(tree[level][1] == EMPTY_LEAF, "Subtree must be empty");
        }
        setupDepth(newDepth);
    }

    function getRoot() public view returns (bytes32) {
        if (tree[depth][0] == EMPTY_LEAF) {
            return cacheEmptyValues[depth];
        } else {
            return tree[depth][0];
        }
    }

    function calculateEmptyLeafHash(uint fromLevel, uint toLevel) internal {
        bytes32 prev;
        if (fromLevel == 0) {
            cacheEmptyValues[0] = prev = sha256("");
            fromLevel = 1;
        } else {
            prev = cacheEmptyValues[fromLevel-1];
        }

        for (uint index = fromLevel; index <= toLevel; index += 1) {
            // we write the hash to both memory and storage at the same time
            // in order to use it in the next iteration. it is cheaper to read
            // from memory instead of storage, so we save it here.
            cacheEmptyValues[index] = prev = sha256(abi.encodePacked(prev, prev));
        }
    }

    function updateLeaf(uint level, uint i) internal {
        uint i0 = 2*i;
        uint i1 = 2*i+1;

        bytes32 v0 = tree[level-1][i0];
        bytes32 v1 = tree[level-1][i1];

        if ((v0 == EMPTY_LEAF) && (v1 == EMPTY_LEAF)) {
            delete tree[level][i];
            return;
        }

        if (v0 == EMPTY_LEAF) {
            v0 = cacheEmptyValues[level-1];
        }

        if (v1 == EMPTY_LEAF) {
            v1 = cacheEmptyValues[level-1];
        }

        tree[level][i] = sha256(abi.encodePacked(v0, v1));
    }

    function modifyHashedElement(uint index, bytes32 hashedElement) internal {
        require(index < maxElements, "Index out of bounds");
        tree[0][index] = hashedElement;
        for (uint level = 1; level <= depth; level++) {
            // 1<<level == 2**level
            uint currentIndex = index / (1<<level);
            updateLeaf(level, currentIndex);
        }
    }

    function modifyElement(uint index, bytes calldata data) internal {
        elementData[index] = data;
        bytes32 hashedElement = sha256(data);
        modifyHashedElement(index, hashedElement);
    }

    function addElement(uint index, bytes calldata data) internal {
        require(elementData[index].length == 0, "Element already exists");
        modifyElement(index, data);
    }

    function removeElement(uint index) internal {
        require(elementData[index].length != 0, "Can't remove empty element");
        delete elementData[index];
        modifyHashedElement(index, EMPTY_LEAF);
    }
}

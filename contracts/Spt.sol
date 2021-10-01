// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

abstract contract Spt {
    // because maxElements = 2**depth, so 256 will overflow
    uint constant MAX_DEPTH = 255;
    bytes32 constant internal EMPTY_LEAF = 0x00;

    mapping(uint256 => bytes32) public cacheEmptyValues;

    uint public depth;
    uint public maxElements;

    // tree level => index inside level => element hash
    mapping(uint256 => mapping(uint256 => bytes32)) public tree;
    mapping(uint256 => bytes) public elementData; 

    constructor(uint _depth) {
        require(_depth > 0, "Depth must be non-zero");
        require(_depth <= MAX_DEPTH, "Overflow protection");
        cacheEmptyValues[0] = hash("");
        // current depth == 0
        calculateEmptyLeafHash(_depth);
        setupDepth(_depth);
    }

    function setupDepth(uint _depth) private {
        depth = _depth;
        // 1<<depth == 2**depth
        maxElements = 1<<depth;
    }

    function increaseDepth(uint depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint oldDepth = depth;
        require(depthDifference <= MAX_DEPTH - oldDepth, "Overflow protection");
        uint newDepth = oldDepth + depthDifference;

        calculateEmptyLeafHash(newDepth);

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
        }
        return tree[depth][0];
    }

    function calculateEmptyLeafHash(uint toLevel) private {
        uint256 currentDepth = depth;
        bytes32 prev = cacheEmptyValues[currentDepth];

        for (uint index = currentDepth+1; index <= toLevel; index += 1) {
            // We write the hash to both memory and storage at the same time
            // in order to use it in the next iteration. It is cheaper to read
            // from memory instead of storage, so we save it here.
            cacheEmptyValues[index] = prev = hash(abi.encodePacked(prev, prev));
        }
    }

    function updateLeaf(uint level, uint i) private {
        // level MUST be > 0

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

        tree[level][i] = hash(abi.encodePacked(v0, v1));
    }

    function modifyHash(uint index, bytes32 hashedElement) private {
        require(index < maxElements, "Index out of bounds");
        tree[0][index] = hashedElement;
        for (uint level = 1; level <= depth; level++) {
            // index >> level == index / 2**level
            uint currentIndex = index >> level;
            updateLeaf(level, currentIndex);
        }
    }

    function modifyElement(uint index, bytes calldata data) internal {
        elementData[index] = data;
        bytes32 hashedElement = hash(data);
        modifyHash(index, hashedElement);
    }

    function addElement(uint index, bytes calldata data) internal {
        require(elementData[index].length == 0, "Element already exists");
        modifyElement(index, data);
    }

    function removeElement(uint index) internal {
        require(elementData[index].length != 0, "Can't remove empty element");
        delete elementData[index];
        modifyHash(index, EMPTY_LEAF);
    }

    // don't use abstract method in production. +7% gas
    function hash(bytes memory data) virtual internal returns (bytes32);
}

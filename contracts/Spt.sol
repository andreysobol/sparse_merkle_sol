// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

abstract contract Spt {
    // because maxElements = 2**depth, so 256 will overflow
    uint8 constant MAX_DEPTH = 255;
    bytes32 constant internal EMPTY_SUBTREE = 0x00;

    mapping(uint256 => bytes32) public cacheEmptyValues;

    uint8 public depth;

    // tree level => index inside level => element hash
    mapping(uint256 => mapping(uint256 => bytes32)) public tree;
    mapping(uint256 => bytes) public elementData; 

    constructor(uint8 _depth) {
        require(_depth > 0, "Depth must be non-zero");
        //require(_depth <= MAX_DEPTH, "Overflow protection");
        cacheEmptyValues[0] = hash("");
        // current depth == 0
        _calculateEmptyLeafHash(_depth);
        depth = _depth;
    }

    function totalElements() public view returns (uint256) {
        // 1<<depth == 2**depth
        return 1<<depth;
    }

    function increaseDepth(uint8 depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint8 oldDepth = depth;
        require(depthDifference <= MAX_DEPTH - oldDepth, "Overflow protection");
        uint8 newDepth = oldDepth + depthDifference;

        _calculateEmptyLeafHash(newDepth);

        for (uint8 level = oldDepth+1; level <= newDepth; level += 1) {
            _updateLeaf(level, 0);
        }
        depth = newDepth;
    }

    function decreaseDepth(uint8 depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint8 oldDepth = depth;
        require(depthDifference < oldDepth, "Overflow protection");
        uint8 newDepth = oldDepth - depthDifference;

        for (uint8 level = newDepth; level < oldDepth; level += 1) {
            require(tree[level][1] == EMPTY_SUBTREE, "Subtree must be empty");
        }
        depth = newDepth;
    }

    function getRoot() public view returns (bytes32) {
        if (tree[depth][0] == EMPTY_SUBTREE) {
            return cacheEmptyValues[depth];
        }
        return tree[depth][0];
    }

    function _calculateEmptyLeafHash(uint8 toLevel) private {
        uint8 currentDepth = depth;
        bytes32 prev = cacheEmptyValues[currentDepth];

        for (uint8 level = currentDepth+1; level <= toLevel; level += 1) {
            // We write the hash to both memory and storage at the same time
            // in order to use it in the next iteration. It is cheaper to read
            // from memory instead of storage, so we save it here.
            cacheEmptyValues[level] = prev = hash(abi.encodePacked(prev, prev));
        }
    }

    function _updateLeaf(uint8 level, uint i) private {
        // level MUST be > 0

        uint i0 = 2*i;
        uint i1 = 2*i+1;

        bytes32 v0 = tree[level-1][i0];
        bytes32 v1 = tree[level-1][i1];

        if ((v0 == EMPTY_SUBTREE) && (v1 == EMPTY_SUBTREE)) {
            delete tree[level][i];
            // If we will use:
            // tree[level][i] = EMPTY_SUBTREE;
            // We will spend much more gas
            return;
        }

        if (v0 == EMPTY_SUBTREE) {
            v0 = cacheEmptyValues[level-1];
        }

        if (v1 == EMPTY_SUBTREE) {
            v1 = cacheEmptyValues[level-1];
        }

        tree[level][i] = hash(abi.encodePacked(v0, v1));
    }

    function _modifyHash(uint index, bytes32 hashedElement) private {
        require(index < totalElements(), "Index out of bounds");
        tree[0][index] = hashedElement;
        for (uint8 level = 1; level <= depth; level += 1) {
            // index >> level == index / 2**level
            uint currentIndex = index >> level;
            _updateLeaf(level, currentIndex);
        }
    }

    function modifyElement(uint index, bytes calldata data) internal {
        elementData[index] = data;
        bytes32 hashedElement = hash(data);
        _modifyHash(index, hashedElement);
    }

    function addElement(uint index, bytes calldata data) internal {
        require(elementData[index].length == 0, "Element already exists");
        modifyElement(index, data);
    }

    function removeElement(uint index) internal {
        require(elementData[index].length != 0, "Can't remove empty element");
        delete elementData[index];
        // If we will use:
        // elementData[index] = "";
        // We will spend much more gas
        _modifyHash(index, EMPTY_SUBTREE);
    }

    // don't use abstract method in production. +7% gas
    function hash(bytes memory data) virtual internal returns (bytes32);
}

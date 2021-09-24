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

    constructor(uint _depth) {
        assert(_depth > 0);
        setupDepth(_depth);
        calculateEmptyLeafHash(_depth);
        tree[depth][0] = cacheEmptyValues[depth];
    }

    function setupDepth(uint _depth) internal {
        depth = _depth;
        maxElements = 2**depth;
    }

    function increaseDepth(uint depthDifference) internal {
        assert(depthDifference > 0);
        uint oldDepth = depth;
        uint newDepth = oldDepth + depthDifference;

        calculateEmptyLeafHash(newDepth);

        uint currentIndex = 0;
        for (uint level = oldDepth; level < newDepth; level++) {
            calculateAndUpdateLeaf(level, currentIndex);
        }
        setupDepth(newDepth);
    }

    function decreaseDepth(uint depthDifference) internal {
        uint oldDepth = depth;
        uint newDepth = oldDepth - depthDifference;
        assert(depthDifference > 0);
        assert(newDepth > 0);

        uint checkIndex = 1;
        for (uint level = newDepth; level < oldDepth; level++) {
            assert(tree[level][checkIndex] == EMPTY_LEAF);
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

    function calculateEmptyLeafHash(uint level) internal {
        if (cacheEmptyValues[0] == EMPTY_LEAF) {
            cacheEmptyValues[0] = sha256("");
        }

        for (uint index = 1; index <= level; index += 1) {
            if (cacheEmptyValues[index] == EMPTY_LEAF) {
                bytes32 prev = cacheEmptyValues[index-1];
                cacheEmptyValues[index] = sha256(abi.encodePacked(prev, prev));
            }
        }
    }

    function calculateAndUpdateLeaf(uint level, uint i) internal {

        uint i0 = 2*i;
        uint i1 = 2*i+1;

        bytes32 v0 = tree[level][i0];
        bytes32 v1 = tree[level][i1];

        if ((v0 == EMPTY_LEAF) && (v1 == EMPTY_LEAF)) {
            delete tree[level+1][i];
            return;
        }

        if (v0 == EMPTY_LEAF) {
            v0 = cacheEmptyValues[level];
        }

        if (v1 == EMPTY_LEAF) {
            v1 = cacheEmptyValues[level];
        }

        tree[level+1][i] = sha256(abi.encodePacked(v0, v1));
    }

    function modifyHashedElement(uint index, bytes32 hashedElement) internal {
        require(index < maxElements, "Index out of bounds");
        tree[0][index] = hashedElement;
        for (uint level = 0; level < depth; level++) {
            uint currentIndex = index / (2**(level+1));
            calculateAndUpdateLeaf(level, currentIndex);
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
        require(elementData[index].length != 0, "Can't remove already empty element");
        delete elementData[index];
        modifyHashedElement(index, EMPTY_LEAF);
    }
}

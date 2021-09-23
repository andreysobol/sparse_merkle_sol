// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

contract Spt {
    bytes32 public emptyElement = 0x0000000000000000000000000000000000000000000000000000000000000000;
    mapping(uint256 => bytes32) public cacheEmptyValues;

    uint public depth;
    uint public maxElements;

    mapping(uint256 => mapping(uint256 => bytes32)) public lists;
    mapping(uint256 => bytes) public elementData; 

    constructor(uint _depth) {
        assert(_depth > 0);
        setupDepth(_depth);
        calculateEmptyLeafHash(_depth);
    }

    function setupDepth(uint _depth) internal {
        depth = _depth;
        maxElements = 2**depth;
    }

    function increaseDepth(uint amountOfLevel) internal {
        assert(amountOfLevel > 0);
        uint oldDepth = depth;
        uint newDepth = depth + amountOfLevel;

        calculateEmptyLeafHash(newDepth);

        uint currentIndex = 0;
        for (uint level = oldDepth; level < newDepth - 1; level++) {
            calculateAndUpdateLeaf(level, currentIndex);
        }
        setupDepth(newDepth);
    }

    function decreaseDepth(uint amountOfLevel) internal {
        uint oldDepth = depth;
        uint newDepth = depth - amountOfLevel;
        assert(amountOfLevel > 0);
        assert(newDepth > 0);

        uint checkIndex = 1;
        for (uint level = newDepth; level < oldDepth - 1; level++) {
            assert(lists[level][checkIndex] == 0x00);
        }
        setupDepth(newDepth);
    }

    function getRoot() public view returns (bytes32) {
        return lists[depth][0];
    }

    function calculateEmptyLeafHash(uint level) internal returns (bytes32) {
        if (cacheEmptyValues[level] != 0x00) {
            return cacheEmptyValues[level];
        }

        if (level == 0) {
            cacheEmptyValues[level] = sha256(abi.encodePacked(emptyElement));
        } else {
            bytes32 prev = calculateEmptyLeafHash(level - 1);
            cacheEmptyValues[level] = sha256(abi.encodePacked(prev, prev));
        }

        return cacheEmptyValues[level];
    }

    function calculateLeaf(uint level, uint i) internal returns (bytes32) {
        uint i0 = 2*i;
        uint i1 = 2*i+1;

        bytes32 v0 = lists[level][i0];
        bytes32 v1 = lists[level][i1];

        if ((v0 == 0) && (v1 == 0)) {
            return 0x00;
        }

        if (v0 == 0) {
            v0 = calculateEmptyLeafHash(level);
        }

        if (v1 == 0) {
            v1 = calculateEmptyLeafHash(level);
        }

        return sha256(abi.encodePacked(v0, v1));
    }

    function calculateAndUpdateLeaf(uint level, uint i) internal {
        lists[level+1][i] = calculateLeaf(level, i);
    }

    function modifyHashedElement(uint index, bytes32 hashedElement) internal {
        lists[0][index] = hashedElement;
        for (uint level = 0; level < depth - 1; level++) {
            uint currentIndex = index / (2**(level+1));
            calculateAndUpdateLeaf(level, currentIndex);
        }
    }

    function modifyElement(uint index, bytes calldata data) internal {
        elementData[index] = data;
        bytes32 hashedElement = sha256(data);
        modifyHashedElement(index, hashedElement);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

library SMT {
    // because maxElements = 2**depth, so 256 will overflow
    uint8 constant MAX_DEPTH = 255;
    bytes32 constant internal EMPTY_SUBTREE = 0x00;

    struct MerkleTree {
        uint8 depth;
        mapping(uint256 => bytes32) cacheEmptyValues;
        // tree level => index inside level => element hash
        mapping(uint256 => mapping(uint256 => bytes32)) tree;
        mapping(uint256 => bytes) elementData;
    }

    using SMT for MerkleTree;

    function initialize(MerkleTree storage tree, uint8 _depth) internal {
        require(_depth > 0, "Depth must be non-zero");
        tree.cacheEmptyValues[0] = hash("");
        // current depth == 0
        tree._calculateEmptyLeafHash(_depth);
        tree.depth = _depth;
    }

    function totalElements(MerkleTree storage tree) public view returns (uint256) {
        // 1<<depth == 2**depth
        return 1<<tree.depth;
    }

    function increaseDepth(MerkleTree storage tree, uint8 depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint8 oldDepth = tree.depth;
        require(depthDifference <= MAX_DEPTH - oldDepth, "Overflow protection");
        uint8 newDepth = oldDepth + depthDifference;

        tree._calculateEmptyLeafHash(newDepth);

        for (uint8 level = oldDepth+1; level <= newDepth; level += 1) {
            tree._updateNode(level, 0);
        }
        tree.depth = newDepth;
    }

    function decreaseDepth(MerkleTree storage tree, uint8 depthDifference) internal {
        require(depthDifference > 0, "depthDifference must be non-zero");
        uint8 oldDepth = tree.depth;
        require(depthDifference < oldDepth, "Underflow protection");
        uint8 newDepth = oldDepth - depthDifference;

        for (uint8 level = newDepth; level < oldDepth; level += 1) {
            require(tree.tree[level][1] == EMPTY_SUBTREE, "Subtree must be empty");
            // If we will delete this:
            // delete tree[level+1][0];
            // delete cacheEmptyValues[level+1];
            // refund will be smaller than gas spent :(
        }
        tree.depth = newDepth;
    }

    function getRoot(MerkleTree storage tree) public view returns (bytes32) {
        if (tree.tree[tree.depth][0] == EMPTY_SUBTREE) {
            return tree.cacheEmptyValues[tree.depth];
        }
        return tree.tree[tree.depth][0];
    }

    function _calculateEmptyLeafHash(MerkleTree storage tree, uint8 toLevel) internal {
        uint8 currentDepth = tree.depth;
        bytes32 prev = tree.cacheEmptyValues[currentDepth];

        for (uint8 level = currentDepth+1; level <= toLevel; level += 1) {
            // We write the hash to both memory and storage at the same time
            // in order to use it in the next iteration. It is cheaper to read
            // from memory instead of storage, so we save it here.
            tree.cacheEmptyValues[level] = prev = hash(abi.encodePacked(prev, prev));
        }
    }

    function _updateNode(MerkleTree storage tree, uint8 level, uint i) internal {
        // level MUST be > 0

        uint i0 = 2*i;
        uint i1 = 2*i+1;

        bytes32 v0 = tree.tree[level-1][i0];
        bytes32 v1 = tree.tree[level-1][i1];

        if ((v0 == EMPTY_SUBTREE) && (v1 == EMPTY_SUBTREE)) {
            delete tree.tree[level][i];
            // If we will use:
            // tree[level][i] = EMPTY_SUBTREE;
            // We will spend much more gas
            return;
        }

        if (v0 == EMPTY_SUBTREE) {
            v0 = tree.cacheEmptyValues[level-1];
        }

        if (v1 == EMPTY_SUBTREE) {
            v1 = tree.cacheEmptyValues[level-1];
        }

        tree.tree[level][i] = hash(abi.encodePacked(v0, v1));
    }

    function _modifyTree(MerkleTree storage tree, uint index, bytes32 hashedElement) internal {
        require(index < totalElements(tree), "Index out of bounds");
        tree.tree[0][index] = hashedElement;
        for (uint8 level = 1; level <= tree.depth; level += 1) {
            // index >> level == index / 2**level
            uint currentIndex = index >> level;
            tree._updateNode(level, currentIndex);
        }
    }

    function modifyElement(MerkleTree storage tree, uint index, bytes calldata data) internal {
        tree.elementData[index] = data;
        bytes32 hashedElement = hash(data);
        tree._modifyTree(index, hashedElement);
    }

    function addElement(MerkleTree storage tree, uint index, bytes calldata data) internal {
        require(tree.elementData[index].length == 0, "Element already exists");
        tree.modifyElement(index, data);
    }

    function removeElement(MerkleTree storage tree, uint index) internal {
        require(tree.elementData[index].length != 0, "Can't remove empty element");
        delete tree.elementData[index];
        // If we will use:
        // elementData[index] = "";
        // We will spend much more gas
        tree._modifyTree(index, EMPTY_SUBTREE);
    }

    function hash(bytes memory data) internal pure returns (bytes32) {
        return keccak256(data);
    }
}

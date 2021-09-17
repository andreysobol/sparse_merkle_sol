pragma solidity ^0.7.0;

contract Spt {

    bytes32 internal emptyElement = 0x0000000000000000000000000000000000000000000000000000000000000000;
    mapping(uint256 => bytes32) internal cacheEmptyValues;

    uint internal depth;
    uint internal maxElements;

    mapping(uint256 => mapping(uint256 => bytes32)) internal lists;

    mapping(uint256 => bytes[]) internal elements;

    function setupDepth(uint _depth) public {
        depth = _depth;
        maxElements = 2**depth;
    }

    function getRoot() public view returns (bytes32) {
        if (lists[depth][0] == 0x00) {
            return getEmptyLeafHash(depth);
        } else {
            return lists[depth][0];
        }
    }

    function getEmptyLeafHash(uint level) public view returns (bytes32) {
        if (level == 0) {
            return sha256(abi.encodePacked(emptyElement));
        } else {
            bytes32 prev = getEmptyLeafHash(level - 1);
            return sha256(abi.encodePacked(prev, prev));
        }
    }

    function calculateEmptyLeafHash(uint level) public returns (bytes32) {

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

}
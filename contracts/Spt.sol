pragma solidity ^0.7.0;

contract Spt {

    bytes32 internal emptyElement = 0x0000000000000000000000000000000000000000000000000000000000000000;
    mapping(uint256 => bytes32) internal cacheEmptyValues;

    uint internal depth;
    uint internal maxElements;

    function setupDepth(uint _depth) public {
        depth = _depth;
        maxElements = 2**depth;
    }

}
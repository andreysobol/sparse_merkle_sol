pragma solidity ^0.7.0;

contract Spt {

    bytes32 internal emptyElement = 0x0000000000000000000000000000000000000000000000000000000000000000;
    mapping(uint256 => bytes32) internal cacheEmptyValues;

    uint internal depth;
    uint internal maxElements;

    mapping(uint256 => mapping(uint256 => bytes32)) internal lists;

    function setupDepth(uint _depth) public {
        depth = _depth;
        maxElements = 2**depth;
    }

    function getRoot() public view returns (uint) {
        if (lists[depth][0] == 0x00) {
            return 0;
            //calculate_empty_leaf_hash will be here
        } else {
            return lists[depth][0];
        }
    }
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    // this will be initialized to the null value - 0!
    uint256 favoriteNumber;
    bool favoriteBool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    // external, internal, public, private
    function store(uint256 _favoriteNumber) public returns(uint256){
        // updating variables
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    // view - non-state changing - no transactions needed, it just reads the state, pure - doesn't store the value(mathematical) anywhere like in a variable, it just does the math and that's it
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    // memory - only stored during the execution, storage - stored after execution
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
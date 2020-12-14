// SPDX-License-Identifier: MIT
pragma solidity >=0.4.26 <0.7.0;

contract DNSContract {
    struct Entry
    {
    	string ip;
    	string url;
    	uint dateOfCreation;
    	uint expireTimeAmount;
    	address creator;
    }

    Entry public entry;

  function setAddress(string memory newAddress) public {
     entry.ip = newAddress;
  }

  function getAddress() public view returns (string memory) {
    return entry.ip;
  }

  function setURL(string memory newURL) public {
     entry.url = newURL;
  }

  function getURL() public view returns (string memory) {
    return entry.url;
  }

  function setDateOfCreation(uint newDateOfCreation) public {
     entry.dateOfCreation = newDateOfCreation;
  }

  function getDateOfCreation() public view returns (uint) {
    return entry.dateOfCreation;
  }

  function setExpireTimeAmount(uint newExpireTimeAmount) public {
     entry.expireTimeAmount = newExpireTimeAmount;
  }

  function getExpireTimeAmount() public view returns (uint) {
    return entry.expireTimeAmount;
  }

  function setCreator(address newCreator) public {
     entry.creator = newCreator;
  }

  function getCreator() public view returns (address) {
    return entry.creator;
  }

   constructor() public {
      setCreator(msg.sender);
      setDateOfCreation(now);
      // One year to expire
      setExpireTimeAmount(1);
   }
}

// SPDX-License-Identifier: MIT
//pragma solidity >=0.4.22 <0.8.0;
pragma solidity >=0.4.0 <0.7.0;

contract DNS {
    struct Entry
    {
	string ip;
	string url;
	uint dateOfCreation;
	uint expireTimeAmount;
	address creator;
    }

    Entry entry;

  function setAddress(string memory newAddress) private {
     entry.ip = newAddress;
  }

  function getAddress() public view returns (string memory) {
    return entry.ip;
  }

  function setURL(string memory newURL) private {
     entry.url = newURL;
  }

  function getURL() public view returns (string memory) {
    return entry.url;
  }

  function setDateOfCreation(uint newDateOfCreation) private {
     entry.dateOfCreation = newDateOfCreation;
  }

  function getDateOfCreation() public view returns (uint) {
    return entry.dateOfCreation;
  }

  function setExpireTimeAmount(uint newExpireTimeAmount) private {
     entry.expireTimeAmount = newExpireTimeAmount;
  }

  function getExpireTimeAmount() public view returns (uint) {
    return entry.expireTimeAmount;
  }

  function setCreator(address newCreator) private {
     entry.creator = newCreator;
  }

  function getCreator() public view returns (address) {
    return entry.creator;
  }

   constructor() public {
      setCreator(msg.sender);
      setDateOfCreation(now);
   }
}

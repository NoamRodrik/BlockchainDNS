// SPDX-License-Identifier: MIT
//pragma solidity >=0.4.22 <0.8.0;
pragma solidity >=0.4.0 <0.7.0;

contract DNSRegistry {
  string url;

  function set(string memory new_url) public {
     url = new_url;
  }

  function get() public view returns (string memory) {
    return url;
  }
}

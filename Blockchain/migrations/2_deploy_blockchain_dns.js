const DNSContract = artifacts.require("DNSContract");

module.exports = function (deployer) {
  deployer.deploy(DNSContract);
};

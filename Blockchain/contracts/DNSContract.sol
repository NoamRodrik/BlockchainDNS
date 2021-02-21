// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

interface DNSCustomAddress {
    function getDomainAddress(string calldata domainName) external view returns (string memory);
}

contract DNSContract {
    uint256 constant priceForOneByteForOneSecond = 0.016 ether; // ~1B dollar a year
    uint256 constant priceFactor = 5; // divide by this for every additional byte
    uint256 constant minimumNumberOfSeconds = 10 days;
    uint256 constant maximumNumberOfSeconds = 365 days;

    enum AddressType {Simple, Custom}

    struct DNSEntry {
        string domainName;
        uint256 reservationEndTime;
        address payable owner;
        uint256 deposit;
        AddressType addressType;
        string domainAddress;
        DNSCustomAddress customDomainAddress;
    }

    mapping(string => DNSEntry) public entries;
    mapping(address => uint256) public pendingDepositReturns;

    function calculateReservationTime(string memory domainName, uint256 paymentAmount) public pure returns (uint256) {
        uint256 priceForSecond = priceForOneByteForOneSecond / (priceFactor ** bytes(domainName).length);
        uint256 reservationTime = paymentAmount / priceForSecond;
        return reservationTime;
    }

    function isDomainNameReserved(string memory domainName) public view returns (bool) {
        return block.timestamp < entries[domainName].reservationEndTime;
    }

    function isDomainNameReservedBySender(string memory domainName) public view returns (bool) {
        return isDomainNameReserved(domainName) && entries[domainName].owner == msg.sender;
    }

    function reserveDomainName(string calldata domainName) external payable {
        require(!isDomainNameReserved(domainName), "Domain name is already reserved.");
        releaseDomainName(domainName);

        uint256 reservationTime = calculateReservationTime(domainName, msg.value);
        require(reservationTime >= minimumNumberOfSeconds, "The payment is lower than expected");
        require(reservationTime <= maximumNumberOfSeconds, "The payment is higher than expected");

        entries[domainName].domainName = domainName;
        entries[domainName].reservationEndTime = block.timestamp + reservationTime;
        entries[domainName].owner = msg.sender;
        entries[domainName].deposit += msg.value;
    }

    function extendDomainNameReservation(string calldata domainName) external payable {
        require(isDomainNameReservedBySender(domainName), "Domain name has to be reserved by the sender");

        uint256 remainingReservationTime = entries[domainName].reservationEndTime - block.timestamp;
        uint256 addedReservationTime = calculateReservationTime(domainName, msg.value);
        uint256 totalReservationTime = remainingReservationTime + addedReservationTime;
        require(totalReservationTime >= minimumNumberOfSeconds, "The payment is lower than expected");
        require(totalReservationTime <= maximumNumberOfSeconds, "The payment is higher than expected");

        entries[domainName].reservationEndTime = totalReservationTime;
        entries[domainName].deposit += msg.value;
    }

    function releaseDomainName(string memory domainName) public {
        require(entries[domainName].owner == msg.sender || !isDomainNameReserved(domainName), "Domain name has to be reserved by the sender or expaired");

        pendingDepositReturns[entries[domainName].owner] += entries[domainName].deposit;
        delete entries[domainName];
    }

    function pullDeposit() external returns (bool) {
        uint256 amount = pendingDepositReturns[msg.sender];
        if (amount > 0) {
            // It is important to set this to zero because the recipient
            // can call this function again as part of the receiving call
            // before `send` returns.
            pendingDepositReturns[msg.sender] = 0;

            if (!msg.sender.send(amount)) {
                // No need to call throw here, just reset the amount owing
                pendingDepositReturns[msg.sender] = amount;
                return false;
            }
        }
        return true;
    }

    function setDomainAddress(string calldata domainName, string calldata domainAddress) external {
        require(isDomainNameReservedBySender(domainName), "Domain name has to be reserved by the sender");

        entries[domainName].addressType = AddressType.Simple;
        entries[domainName].domainAddress = domainAddress;
        entries[domainName].customDomainAddress = DNSCustomAddress(address(0));
    }

    function setCustomDomainAddress(string calldata domainName, DNSCustomAddress customDomainAddress) external {
        require(isDomainNameReservedBySender(domainName), "Domain name has to be reserved by the sender");

        entries[domainName].addressType = AddressType.Custom;
        entries[domainName].domainAddress = "";
        entries[domainName].customDomainAddress = customDomainAddress;
    }

    function getDomainAddress(string calldata domainName) external view returns (string memory) {
        require(isDomainNameReserved(domainName), "Domain name is not reserved");

        if (entries[domainName].addressType == AddressType.Simple) {
            return entries[domainName].domainAddress;
        }
        else {
            return entries[domainName].customDomainAddress.getDomainAddress(domainName);
        }
    }
}

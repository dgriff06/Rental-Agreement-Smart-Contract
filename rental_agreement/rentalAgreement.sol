//SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.5.0;

// Import ERCX Token so that we can use it's functions.

import "https://github.com/kohshiba/ERC-X/blob/master/contracts/ERCX/Contract/ERCX.sol";

// Create Contract

contract rentalAgreement is  ERCX {

// Create state variables 

    address payable public tenant;
    address payable public owner;
    uint256 public expiration;

    string lessee;
    string landlord;
    string mailingAddress;
    string city;
    string state;
    string month;
    string year;
   
   
    bool renterInsurance = false;
    bool criminalCheck = false;
    bool creditCheck = false;
    bool approved = false;
    bool paidDeposit = false;

// Create constructor that declares the owner

    constructor() public {
        owner = msg.sender;
    }

// Create modifiers for restrictions 

    modifier onlyOwner(){
        require(msg.sender == owner, "Only owner requirement");
        _;
    }
    modifier approval(){
        require(approved == true , "Tenant not approved");
        _;

// Create the functions that we need

    }
    function extend(uint256 newExpiration) external onlyOwner{
        require(block.timestamp <= expiration, "This agreement has expired and cannot be extended. Please sign a new contract.");
        uint _newExpiration = SafeMath.add(newExpiration, expiration);
        expiration = _newExpiration;
    }

 // create contract lengths
    // duration[1] is for 6 months
    // duration[2] is for 12 months
    // duration[3] is for 15 months

    uint[] internal duration = [0, 15768000 ,31536000, 38880000];  

    function leaseApt(address payable _tenant, uint _duration, uint itemID) public onlyOwner approval returns(string memory) {
        expiration = SafeMath.add(duration[_duration], block.timestamp);
        tenant = _tenant;

        safeTransferUser(owner, tenant, itemID);

    }
     function terminateAgreement(address payable _tenant, uint itemID) external onlyOwner {
        require(block.timestamp >= expiration, "Lessee has still time left in the contract");
        tenant = _tenant;
        safeTransferUser(tenant,owner,itemID);
    }
    function mint(address person, uint ID) public onlyOwner {
        _mint(person, ID);
    }

    function finalApproval(address payable _tenant, uint itemID, bool _renterInsurance, bool _criminalCheck, bool _creditCheck, bool _paidDeposit) public onlyOwner returns (bool)  {
        
        tenant = _tenant;
        renterInsurance = _renterInsurance;
        criminalCheck = _criminalCheck;
        creditCheck = _creditCheck;
        paidDeposit = _paidDeposit;
       
        approveForUser(tenant, itemID);

        if (renterInsurance == true && criminalCheck == true && creditCheck == true && paidDeposit == true ){return approved = true;}
        else {approved = false;}
        return approved;

    }
}
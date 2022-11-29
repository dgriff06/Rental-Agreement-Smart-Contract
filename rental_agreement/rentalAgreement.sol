//SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.5.0;

// Import ERCX Token so that we can use it's functions.

import "https://github.com/kohshiba/ERC-X/blob/master/contracts/ERCX/Contract/ERCX.sol";

contract rentalAgreement is  ERCX {
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
   
    constructor() public {
        owner = msg.sender;
    }
    modifier onlyOwner(){
        require(msg.sender == owner, "Only owner requirement");
        _;
    }
    function extend(uint256 newExpiration) external onlyOwner{
        require(block.timestamp <= expiration, "This agreement has expired and cannot be extended. Please sign a new contract.");
        uint _newExpiration = SafeMath.add(newExpiration, expiration);
        expiration = _newExpiration;
    }

    // create contract lengths 
    uint[] internal duration = [0, 15768000 ,31536000, 38880000]; // duration[1] is for 6 months

    function leaseApt(address payable _tenant, uint _duration, uint itemID) public onlyOwner returns(string memory) {
        expiration = SafeMath.add(duration[_duration], block.timestamp);
        tenant = _tenant;

        if(approved == true){safeTransferUser(owner, tenant, itemID);}
        else {return "Tenant not approved";}

         require(approved == true , "Tenant not approved");
    }
     function terminateAgreement(address payable _tenant, uint itemID) external onlyOwner {
        require(block.timestamp >= expiration, "Leasee has still time left in the contract");
        tenant = _tenant;
        safeTransferUser(tenant,owner,itemID);
    }
    function mint(address person, uint ID) public onlyOwner {
        _mint(person, ID);
    }

    bool renterInsurance = false;
    bool criminalCheck = false;
    bool creditCheck = false;
    bool approved = false;
    bool paidDeposit = false;

    function finalApproval(address payable _tenant, uint itemID, bool _renterInsurance, bool _criminalCheck, bool _creditCheck, bool _paidDeposit) public onlyOwner returns (bool)  {
        
        tenant = _tenant;
        renterInsurance = _renterInsurance;
        criminalCheck = _criminalCheck;
        creditCheck = _creditCheck;
        paidDeposit = _paidDeposit;
       
        approveForUser(tenant, itemID);

        if (renterInsurance == true && criminalCheck == true && creditCheck == true && paidDeposit == true ){return approved = true;}
        else {return approved = false;}

    }

    //  function getExpiration(uint itemID) view public returns(uint) {

    //     return (expiration);
    // }
}
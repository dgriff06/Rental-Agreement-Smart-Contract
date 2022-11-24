# Rental-Agreement-Smart-Contract

## Project overview

It is a smart contract for property managers which allows both landlords and tenants to take advantage of the capabilities of blockchain technology. Landlords create a smart contract with the key requirements of the tenancy such as rent amount, payment frequency, property and insurance details. Once all the terms and conditions are reviewed, the contract is electronically signed by both parties and published on the Blockchain. Once published, it is activated and executes transactions using a payments bridge to control the flow of funds between accounts, as specified in the terms of the contract.

We minted a token (like an NFT token), that represents the apartment that is being leased. The token has all unique features such as interoperability, scarcity and transparency. Only the owner is allowed to mint this token. We imported this contract because it had basic rental agreement functions.We just had to add our own requirements and functionalities on top of it to make it more efficient. 

There are a few requirements for a potential tenant to complete in order to be approved by the landlord:
 * Having purchased renters insurance and indicating 
the owner as an additional insured 
* Passing a criminal background check 
* Having a good credit score
* Paying the deposit

Once all the requirements are fulfilled, then the NFT is passed over to the tenant. But if the applicant fails to complete at least one of the listed requirements, a message “Tenant not approved” will pop up. The duration of the lease contract can be chosen to be either short-term representing 6 months, mid term - 12 months, or long term - 15 months. The landlord cannot terminate the agreement if the lease is


## Package requirements and imports
We imported the following contract because it had basic rental agreement functions: <br>
"https://github.com/kohshiba/ERC-X/blob/master/contracts/ERCX/Contract/ERCX.sol"

We just had to add our own requirements and functionalities on top of it to make it more efficient. The import was a bare bones simple rental lease agreement in which a tenant is approved, a token representing an apartment is transacted, and the balance of both landlord and tenant can be checked. We added more features which we believe are common in real life rental lease agreements, such as duration of lease, and approving a tenant based on a number of specific criteria as specified above<br>

### PInata imports:
* pinFiletoIPFS
* pinSONtoIPFS
* convertDatatoJSON



## User instructions
* Download all the files from the repository
* Once download is complete, open the folder on VSCode
* Make sure to install Ethereum Remix plugin on your extensions
* Click on the Ethereum icon on the left and deploy the contract on the .sol file.
* Look to the right and copy and paste the deployed address and put it on the .env file for
* “SMART_CONTRACT_DEPLOYED_ADDRESS” = “” between the quotations.
* On the .env file also the WEB_PROVIDER_URI = should be either HTTP://127.0.0.1:8545 or HTTP://127.0.0.1:7545
* Copy and paste the ABI from the right to the abi.json file
* Open a New Git Bash terminal.
* On the terminal, type Streamlit run app.py

## Results/Examples:
Once up and running, the initial address is the landlord and only the initial address can execute the contract. Make sure it is set to that for any transactions. <br>
The first thing to do is to mint an apartment, which is a token representing a specific apartment.
After choosing lease duration and checking all the boxes, approve the tenant and then lease the apartment to another address. You can then check who owns it with   some of the other buttons.

## Limitations and future development
If we had more time, we could potentially connect the token to a smart lock device connected to the internet that could lock or unlock the apartment based on the contract regulations. If for instance someone leases the apartment, the entrance code to that lock would be given to the user by the contract. Once the contract expires, the lock combination would change.

This potentially could become a business model so that this web site becomes a platform where apartments are advertised by landlords and potential tenants browse apartments. And a lease could take place on the site itself almost automatically, much like Airbnb.


## References
https://docs.soliditylang.org/en/v0.8.17/solidity-by-example.html <br>
https://github.com/kohshiba/ERC-X/blob/master/contracts/ERCX/Contract/ERCX.sol <br>
https://docs.soliditylang.org/en/v0.8.17/solidity-by-example.html <br>
https://github.com/RollaProject/solidity-datetime#timestamptodatetime <br>




## Team Members
Darius Griffin <br>
Yohan Hwang <br>
Bek Davronov <br>

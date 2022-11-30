import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB_PROVIDER_URI")))

## loading the contract
@st.cache(allow_output_mutation=True)
def load_contract():
    
    with open(Path("abi.json")) as abi:
        rental_agreement_abi = json.load(abi)
        
    rental_agreemnt_address = os.getenv("SMART_CONTRACT_DEPLOYED_ADDRESS")
    
    contract = w3.eth.contract(
        address=rental_agreemnt_address,
        abi = rental_agreement_abi
    )
    
    return contract

contract = load_contract()

# front end 

accounts = w3.eth.accounts

st.markdown("# Mint & Rent Residential Lease")

landlord = st.text_input("Landlord Name")
owner = st.selectbox("Landlord's Address", options=accounts, key =1)

lessee = st.text_input("Tenant Name")
user = st.selectbox("Tenant's Address", options=accounts, key =2)

mailingAddress = st.text_input("Mailing Address")

city = st.text_input("City")

state = st.text_input("State")

zipCode = st.text_input("Zip Code")

date = st.date_input("Lease Start Date")

rent = st.text_input("Rent Amount")

deposit = st.text_input("Deposit Amount")

suffix= "th"

m_suffix= "th"

if date.day == 1:
    suffix = "st"
elif date.day == 2:
    suffix = "nd"
elif date.day == 3:
    suffix = "rd"
    
    
if date.month == 1:
    m_suffix = "st"
elif date.month == 2:
    m_suffix = "nd"
elif date.month == 3:
    m_suffix = "rd"
    

leaseAgreement = f"This Residential Lease Agreement ('Agreement') made this {date.month}{m_suffix} month of {date.year} is between {landlord} ('Landlord') with a mailing address of {mailingAddress} , City of {city} , State of {state} AND {lessee} ('Tenant(s)')."

securityDeposit = f"The Landlord requires a payment in the amount of ${deposit} ('Security Deposit') for the faithful performance of the Tenant under the terms and conditions of this Agreement. The Security Deposit is required by the Tenant upon the execution of this Agreement. The Security Deposit shall be returned to the Tenant after the end of the Lease Term less any any itemized deductions. This Security Deposit shall not be credited towards any Rent unless the Landlord gives their written consent. Check the box below if the Tenant has paid their security deposit."

rent = f"The Tenant shall pay the Landlord, in equal monthly installments, ${rent} ('Rent'). The rent shall be due on the {date.day}{suffix} of every month ('Due Date') and paid under the Landlord's instructions. The Landlord requires that the Tenant purchases renter's insurance prior to the approval of this agreement. Check the box below if the Tenanat has purchased renter's insurance."

backgroundCheck = "The Landlord requires that the Tenant(s) submit to a credit check and criminal background check before the lease is approved. If the Tenant(s) fail to sumbit to, or fails to pass the credit and criminal checks, the Landlord reserves the right to deny the Tenant's application. Check the boxes below if the Tenant has consented to and a credit check and criminal background check. "

_duration = st.number_input("Lease Length: Enter '1' for a 6 Month Lease, '2' for a 12 Month Lease, or '3' for a 15 Month Lease",
                            min_value = 1,
                            max_value = 3,
                            step = 1)

apt_no = st.text_input("Enter Apartment Number")

st.write(f"Select 'Mint and Register' below, to mint a token for apartment number: {apt_no} at {mailingAddress}.")

if st.button("Mint and Register"):
    try:
        tx_hash = contract.functions.mint(owner, int(apt_no)).transact({"from":owner})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write(f"The token for Aparment number:{apt_no} has been minted, and is now registered to {landlord}")
        st.write(dict(receipt))
    except Exception as e:
         st.warning(f"RunTimeError: {e}")

# Create the Lease Agreement 

st.markdown("### Lease Agreement")
st.markdown(leaseAgreement)

st.write("Landlord and Tenant are each referred to herin as a 'Party' and, collectively, as the 'Parties'.")
st.write("NOW, THEREFORE, FOR AND IN CONSIDERATION of the mutual promises and agreemnts contained herein, the Tenant agrees to lease the Premises from the Landlord under the following terms and conditions:")
st.markdown("#### 1. Rent")

# st.markdown(rent)
# form = st.form("Insurance", clear_on_submit = True)
# with form:
#     renterInsurance = st.checkbox("Renter's Insurace")
# submitInsurance = form.form_submit_button("Insurance")
# st.write(f"{renterInsurance}")

st.markdown(rent)
renterInsurance = st.checkbox("Renter's Insurace")
st.write(f"{renterInsurance}")


st.markdown("#### 2. Security Deposit")
st.markdown(securityDeposit)      
paidDeposit = st.checkbox("Deposit Paid")

st.markdown("#### 3. Background Check")
st.markdown(backgroundCheck)
creditCheck = st.checkbox("Credit Check")
criminalCheck = st.checkbox("Criminal Check")

        
# Approve & Lease an apartment

st.markdown("#### Submit for Approval")

st.write(f"By selecting 'Approve', the Landlord agrees to submitting this application for approval and verifies that the Tenant agrees to the terms and conditions as stated above. If the Tenant's application is approved Apartment number: {apt_no} at {mailingAddress} will be available to the Tenant for lease.")

# if renterInsurance:
#     if paidDeposit:
#         if creditCheck:
#             if criminalCheck:
# approved = False
if renterInsurance and paidDeposit and creditCheck and criminalCheck:
    if st.button("Approve"):
        try:
            tx_hash = contract.functions.finalApproval(user, int(apt_no), renterInsurance,criminalCheck,creditCheck, paidDeposit)
            st.write(f"The Tenant's application has been submitted for approval.")
            # global approved
            approved = True
        except Exception as e:
            st.warning(f"RunTimeError: {e}")
else:
    st.warning("### Please complete the above fields before approving the apt.")
        
st.markdown("#### Lease Apartment")
st.write(f"By selecting 'Lease', the Landlord verifies that the Tenant has been approved to lease Apartment number: {apt_no} at {mailingAddress} beginning on {date}.")
try:
    if renterInsurance and paidDeposit and creditCheck and criminalCheck:
        if st.button("Lease"):
            try:
                tx_hash = contract.functions.leaseApt(user, int(_duration), int(apt_no)).transact({"from":owner})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                st.write("The apartment has been leased.")
                st.write(dict(receipt))
                # renterInsurance = paidDeposit = creditCheck = criminalCheck =  False
            except Exception as e:
                st.warning(f"RunTimeError: {e}")
    else:
        st.warning("### Please complete the above fields before leasing the apt.")
except Exception as e:
    st.warning(f"RunTimeError: {e}")   
# Verify the Landlord and Tenant
    
st.markdown("#### Verify Lease")
    
st.write(f"Select 'Lessee' below to verify the address of the Tenant who is currently renting apartment number: {apt_no} at {mailingAddress}. ") 

if st.button("Lessee", key = "userof"):
    userOf = contract.functions.userOf(int(apt_no)).call()
    st.write(f"apartment number {apt_no} is used by {userOf} at the moment")

st.write("Select 'Balance' to verify the number of apartments that the Tenant is currently leasing.")
  
if st.button("Balance", key = "balanceuserof"):
    balanceOfUser = contract.functions.balanceOfUser(owner).call()
    st.write(f"{owner} uses {balanceOfUser}")
    
st.write(f"Select 'Landlord' below to verify the address of the Landlord who is currently leasing apartment number: {apt_no} at {mailingAddress}. ")
if st.button("Landlord", key = "ownerof"):
    ownerOf = contract.functions.ownerOf(int(apt_no)).call()
    st.write(f"apartment number {apt_no} is used by {ownerOf} at the moment")
    
# Extend the Lease    
 
st.markdown("#### Extend Lease")

st.write("Before the completion of the above lease agreement, the Parties listed may decide to extend the agreement. If the Parties wish to do so, select 'Extend' below after choosing the agreed upon legth of the extension (in months).")  
newExpiration = st.number_input("Length of Extension",step = 1, format = "%i")
monthExpiration = int(newExpiration) * 2628288

if st.button("Extend"):
    try:
        tx_hash = contract.functions.extend(monthExpiration).transact({"from":owner})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write(f"The lease has been extended by {newExpiration} months")
        st.write(dict(receipt))
    except Exception as e:
        st.write(f"Error: {e}")
        
# ts = int(monthExpiration)
# ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# if st.button("Expiration Date", key = "expirationDate"):
#     expirationDate = contract.functions.getExpiration(int(apt_no)).call()
#     st.write(f"Expiration Date is {expirationDate}")

st.markdown("#### Terminate Lease")
st.write(f"Upon completion of the above lease agreement, the contract shall be terminated, and the token representing apartment number: {apt_no} at {mailingAddress} shall be returned to the Landlord. If the agreement has been completed, select 'Terminate' below.")
    
if st.button("Terminate"):
    try:
        tx_hash = contract.functions.terminateAgreement(user, int(apt_no)).transact({"from":owner})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("The agreement has been terminated")
        st.write(dict(receipt))
    except Exception as e:
        st.warning(f"Error: {e}")


    
    
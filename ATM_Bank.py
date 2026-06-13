accounts={
    "current":500.00,
    "savings":1500.00
}

def check_balance():

    account_type=input("Please enter the account type savings/current: ")

    if account_type in accounts:
        print(f"Your balance in your {account_type} is: {accounts[account_type]}")
        
    else:
        print(f"❌ Error: '{account_type}' account not found.")
        

    

def deposit_money():
    
    account_type=input("Please enter the account type savings/current: ")

    if account_type in accounts:
        try:
            Amount=float(input("Please enter the amount to be added: "))

            if Amount>0:
                accounts[account_type]+=Amount
            else:
                print(f"❌ Error: Deposit amount must be greater than zero.")



        except ValueError:
            print(("❌ Error: Please enter a valid number.")) 


    else:
        print(f"❌ Error: '{account_type}' account not found.")


def withdraw_money():
    
    account_type=input("Please enter the account type savings/current: ")

    if account_type in accounts:
        
        try:
            Amount=float(input("Please enter the amount to be withdrawn: "))
            if Amount>accounts[account_type]:
                print(f"❌ Error: You do not have sufficent funds for this transaction.!")
            else:
                accounts[account_type]-=Amount
                print(f"Withdrawal of {Amount} from your {account_type} account was successfull!")
                print(f"Your new balance in {account_type} is {accounts[account_type]}")

        except ValueError:  
            print(("❌ Error: Please enter a valid number."))

    else:
        print(f"❌ Error: '{account_type}' account not found.")


# ----- Main program ------

import sys

print(f"Welcome to Python Bank !")

PIN_attempts=3

while PIN_attempts>0:

    PIN=input("Please enter the 4 digit pin: ")


    if PIN=="1234":
        print(f"Access granted successfully !")
        break
    else:
        PIN_attempts-=1
        
        if PIN_attempts > 0:
            print(f"The entered PIN is wrong ! , pls try again & you have {PIN_attempts} attempts remaining.")
        else:
            print("Card blocked due to consicutive 3 wrong attempts !")
            sys.exit()

# ---- Inside Program ----

while True:
    print(f"Please choose from the below options: ")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Return Card")

    option=input("please enter the option to choose 1-4: ")

    if option=='1':
        check_balance()
    elif option=='2':
        deposit_money()
    elif option=='3':
        withdraw_money()
    elif option=='4':
        print("card returned successfully!")
        break
    else:
        print("Please enter a valid option to choose !")


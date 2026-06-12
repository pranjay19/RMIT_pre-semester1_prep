# ----- Main program ------

import sys

print(f"Welcome to Python Bank !")

PIN_attempts=3

while PIN_attempts>0:

    PIN=input("Please enter the 4 digit pin: ")

    if PIN=="1234":
        print(f"Access granted successfully !")
    else:
        PIN_attempts-=1
        
        if PIN_attempts > 0:
            print(f"The entered PIN is wrong ! , pls try again & you have {PIN_attempts} attempts remaining.")
        else:
            print("Card blocked due to consicutive 3 wrong attempts !")
            sys.exit()



""" ============================================ 
Title: Assignment 2.1 
Author: David Jorgensen 
Date: 21 September 2025  
Description: Purchase fiber optic cable via python console.
;=========================================== """

# Importing libraries
import math
import random

# Welcome message
print("Behold, the Cable-inator!")

# Collecting user input
while True:
    company = input("Please enter your company name: ").strip()
    # If the input is empty, prompt again
    if company:
        break
    print("Company name cannot be empty. Please try again.")
while True:
    feet_input = input("Please enter the number of feet of cable you wish to purchase: ").strip()
    # If the input is empty, prompt again
    if not feet_input:
        print("Input cannot be empty. Please try again.")
        continue
    # Validate that the input is a float
    try:
        feet = float(feet_input)
        break
    # If input is not a float, prompt again
    except ValueError:
        print("Please enter a valid integer for the number of feet.")

# Calculating total price
price_per_foot = 0.95
total_price = feet * price_per_foot
# Rounding to two decimal places for US currency, always rounding up to the nearest cent
rounded_price = math.ceil(total_price * 100) / 100

# Ensuring two decimal places in the output, even if it's a whole number
rounded_price = f"{rounded_price:.2f}"

# Generating order number
order_number = random.randint(100000, 999999)

# Displaying order summary
print(f"""Thank you, {company}, for your order of {feet} feet of fiber optic cable. 
      The total cost is ${rounded_price}. 
      Your order number is {order_number}.""")
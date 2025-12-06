""" ============================================ 
Title: Assignment 4.1
Author: David Jorgensen
Date: 21 September 2025
Description: Purchase fiber optic cable via python console.
=========================================== """

""" ===========================================
CHANGELOG

25 September 2025 - David Jorgensen
    Updated pricing structure to include bulk discounts.
    Changed rounding method to use round() for standard rounding.
    Removed math library.

30 September 2025 - David Jorgensen
    Wrapped code in main() function.
    Wrapped cost calculation code in orderProcessor() function.
=========================================== """

def orderProcessor(length, price_per_foot):
    # Function to calculate order price and generate order number.
    
    # Importing libraries
    import random
    
    # Calculating total price
    total_price = length * price_per_foot
    # Rounding to two decimal places for US currency
    # Adding a small epsilon to avoid floating point precision issues
    rounded_price = round(total_price + 1e-8, 2)

    # Ensuring two decimal places in the output, even if it's a whole number
    rounded_price = f"{rounded_price:.2f}"

    # Generating order number
    order_number = random.randint(100000, 999999)

    return rounded_price, order_number

def main():
    # Welcome message
    print("Behold, the Cable-inator!")

    # Informing user of pricing structure
    print("""This program will help you order fiber optic cable.
        Cable costs start at $0.95/ft.
        Discounts are available for bulk orders:
        Orders of at least 100 feet will be priced at $0.85/ft.
        Orders of at least 250 feet will be priced at $0.75/ft.
        Orders of at least 500 feet will be priced at $0.55/ft.""")

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

    # Calculate price per foot based on bulk discounts
    if feet >= 500:
        price_per_foot = 0.55
    elif feet >= 250:
        price_per_foot = 0.75
    elif feet >= 100:
        price_per_foot = 0.85
    else: price_per_foot = 0.95

    # Processing the order
    rounded_price, order_number = orderProcessor(feet, price_per_foot)

    # Displaying order summary
    print(f"""Thank you, {company}, for your order of {feet} feet of fiber optic cable. 
        The total cost is ${rounded_price}. 
        Your order number is {order_number}.""")

# Running the main function
main()
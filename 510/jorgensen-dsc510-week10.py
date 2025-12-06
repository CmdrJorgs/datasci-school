""" ============================================
Title: Assignment 10.1
Author: David Jorgensen
Course: DSC 510
Date: 16 November 2025
Description: Basic cash register application.
=========================================== """

# Import libraries
import os
import locale

# Define CashRegister class
class CashRegister:
    """Track total price and item count."""
    def __init__(self):
        # Initialize total_price and item_count constructor
        self.total_price = 0.0
        self.item_count = 0
        self.item_list = []
    
    def add_item(self, price, name, quantity):
        item = CartItem(price, name, quantity)
        # Append item to item_list
        self.item_list.append(item)
    
    @property
    def get_total(self):
        # Returns the total price of items in cart.
        total = self.total_price
        for item in self.item_list:
            total += item.price * item.quantity
        return total
    
    @property
    def get_count(self):
        # Returns the number of items in cart.
        count = self.item_count
        for item in self.item_list:
            count += item.quantity
        return count

class CartItem:
    """Item in the cart."""
    def __init__(self, price, name, quantity):
        self.price = price
        self.name = name
        self.quantity = quantity

def cart_add_item(cart):
    # Prompts user for item details and adds item to cart
    print("\nPlease enter the item details (or type 'exit' to quit):")
    # Get item name
    while True:
        name = input("Product Name: ")
        if name.strip().lower() == 'exit':
            exit()
            break
        elif name == '' or name.isspace():
            print("Name cannot be blank.")
            continue
        else:
            break
    # Get item price
    while True:
        try:
            price_input = input("Product Price: ").strip().lower()
            if price_input == 'exit':
                exit()
                break
            price = float(price_input)
            if price < 0:
                print("Price cannot be negative.")
                continue
            else:
                break
        except ValueError:
            print("Price must be a numeric value.")
            continue
    # Get item quantity
    while True:
        try:
            quantity_input = input("Quantity: ").strip().lower()
            if quantity_input == 'exit':
                exit()
                break
            quantity = int(quantity_input)
            if quantity < 1:
                print("Quantity cannot be less than 1.")
                continue
            else:
                break
        except ValueError:
            print("Quantity must be a whole number.")
    
    # Add item to cart
    cart.add_item(price, name, quantity)
    return cart

def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Main function to run the cash register application.
    print("Welcome to the Cash Register Application!")
    # Initialize a new cash register
    cart = CashRegister()
    while True:
        # Add item to cart
        cart = cart_add_item(cart)
        # Ask user if they want to add another item
        continue_input = input("Add another item? (y/n): ").strip().lower()
        if continue_input == 'y':
            # Clear the console
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        elif continue_input == 'n':
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue
    
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Print cart items in a formatted table
    print("\nItems in your cart:")
    print(f"\n\033[7m{'PRODUCT':<20}{'QUANTITY':<10}{'INDIVIDUAL PRICE':<20}{'TOTAL PRICE':<20}\033[0m")
    for item in cart.item_list:
        # Calculate cumulative price for each item
        total_price = item.price * item.quantity
        # Format prices as USD currency
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        formatted_price = locale.currency(item.price, grouping=True)
        formatted_total = locale.currency(total_price, grouping=True)
        # Print each item in the cart
        print(f"{item.name:<20}{item.quantity:<10}{formatted_price:<20}{formatted_total:<20}")
    print("-" * 70)
    # Print totals
    print(f"\033[1m{'TOTALS':<20}{cart.get_count:<10}{'':<20}{locale.currency(cart.get_total, grouping=True):<20}\033[0m\n")
    exit()

# Run the main function
if __name__ == "__main__":
    main()
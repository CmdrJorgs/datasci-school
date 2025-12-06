""" ============================================ 
Title: Assignment 5.1
Author: David Jorgensen
Date: 12 October 2025
Description: Calculator utility.
=========================================== """

def perform_calculation(operator):
    # Prompt user for two numbers
    while True:
        try:
            num1 = float(input("Enter the first number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    while True:
        try:
            num2 = float(input("Enter the second number: "))
            # If input is zero and operator is division, prompt again
            if operator == '/' and num2 == 0:
                print("Cannot divide by zero. Please enter a non-zero number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    # Perform the calculation based on the operator
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2

def calculate_average():
    # Ask user how many numbers they want to average
    total_numbers = int(input("How many numbers do you want to average? "))
    numbers = []

    # Collect the numbers
    for i in range(total_numbers):
        while True:
            try:
                number = float(input(f"Enter number {i + 1}: "))
                numbers.append(number)
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    # Calculate the average
    average = sum(numbers) / total_numbers
    return average
    

def main():
    print("Welcome to the Calculator Utility!")
    while True:
        # Prompt user for action
        print("\nSelect an option:")
        print("1. Perform a calculation")
        print("2. Calculate an average")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            # Get the operator from the user and ensure it's valid
            while True:
                operator = input("Enter an operator (+, -, *, /): ").strip()
                if operator in ['+', '-', '*', '/']:
                    break
                print("Invalid operator. Please enter one of +, -, *, /.")
            response = perform_calculation(operator)
            print(f"The result of the calculation is: {response}")
        elif choice == '2':
            # Calculate average
            response = calculate_average()
            print(f"The average of the entered numbers is: {response:.2f}")
        elif choice == '3':
            # Exit the program
            print("Exiting the program. Goodbye!")
            break
        else:
            # Invalid choice, prompt again
            print("Invalid choice. Please select 1, 2, or 3.")

# Run the main function
main()
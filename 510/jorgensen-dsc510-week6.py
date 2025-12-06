""" ============================================ 
Title: Assignment 6.1
Author: David Jorgensen
Date: 19 October 2025
Description: Temperature high/low finder utility.
=========================================== """

def main():
    print("Welcome to the Temperature High/Low Finder Utility!")
    while True:
        # Prompt user for temperatures
        print("Enter temperatures in Fahrenheit (or type '=' to calculate): ")
        temperatures = []
        while True:
            user_input = input("Enter temperature (or '=' to finish): ")
            if user_input == '=':
                break
            try:
                temp_f = float(user_input)
                temperatures.append(temp_f)
            except ValueError:
                print("Invalid input. Please enter a numeric value or '=' to finish.")
        # Find high and low temperatures
        if not temperatures:
            print("No temperatures were entered.")
            continue
        # Get high and low from list
        high_temp, low_temp = temperatureListEvaluator(temperatures)

        # Print high and low temperatures
        print(f"High Temperature: {high_temp}°")
        print(f"Low Temperature: {low_temp}°")

        # Print total number of temperatures entered
        print(f"Total number of temperatures entered: {len(temperatures)}")

        # Ask user if they want to perform another calculation
        again = input("Would you like to enter another set of temperatures? (y/n): ")
        if again.lower() != 'y':
            print("Thank you for using the Temperature High/Low Finder Utility. Goodbye!")
            break

def temperatureListEvaluator(tempList):
    # Evaluate the list to find high and low temperatures
    if not tempList:
        return None, None
    high_temp = max(tempList)
    low_temp = min(tempList)
    return high_temp, low_temp

# Run the main function
main()
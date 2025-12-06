""" ============================================
Title: Assignment 9.1
Author: David Jorgensen
Course: DSC 510
Date: 9 November 2025
Description: Chuck Norris joke API retriever.
=========================================== """

# Import libraries
import os
import requests

def category_fetcher():
    # Fetches joke categories from the Chuck Norris API.
    categories_url = "https://api.chucknorris.io/jokes/categories"
    print("Fetching joke categories from API...")
    try:
        response = requests.get(categories_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching category data from API: {e}")
        return []
    return response.json()

def joke_fetcher(category):
    # Fetches a random joke from the specified category.
    joke_url = f"https://api.chucknorris.io/jokes/random?category={category}"
    print(f"Fetching joke from category '{category}'...")
    try:
        response = requests.get(joke_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke data from API: {e}")
        print("No categories available. Exiting program.")
        exit()
    return response.json()

def joke_prompter(categories):
    # Prompts the user to select a category and returns it.
    print("Available Chuck Norris Joke Categories:")
    for category in categories:
        print(f"- {category}")
    while True:
        selected_category = input("Please enter a category from the list above (or type 'exit' to close the program): ").strip().lower()
        if selected_category in categories:
            return selected_category
        elif selected_category == "exit": 
            print("Exiting program. Goodbye!")
            exit()
        else:
            print(f"'{selected_category}' is not a valid category. Please try again.")

def joke_printer(joke):
    # Formats the joke text to highlight "Chuck Norris".
    joke_text = joke.replace("Chuck Norris", "\033[1;35mChuck Norris\033[0m")
    print(joke_text)

def joke_looper(categories):
    # Prompt and Fetch a random joke from the selected category
    joke_data = joke_fetcher(joke_prompter(categories))
    if not joke_data:
        print("Could not retrieve a joke. Exiting program.")
        return
    
    # Print the joke with formatting
    joke_printer(joke_data['value'])
    
    # Ask user if they want another joke
    while True:
        another = input("\nWould you like another joke? (y/n): ").strip().lower()
        if another == 'y':
            # Clear the console
            os.system('cls' if os.name == 'nt' else 'clear')
            # Prompt for another joke
            return joke_looper(categories)
        elif another == 'n':
            print("Thanks for using the Chuck Norris Joke Retriever! Goodbye!")
            exit()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Main function to run the Chuck Norris joke retriever program.
    print("\033[1mWelcome to the Chuck Norris Joke Retriever!\033[0m")

    # Fetch joke categories
    categories = category_fetcher()
    
    # Start the joke looper
    joke_looper(categories)

# Run the main function
if __name__ == "__main__":
    main()
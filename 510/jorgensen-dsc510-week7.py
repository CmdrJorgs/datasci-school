""" ============================================ 
Title: Assignment 7.1
Author: David Jorgensen
Date: 19 October 2025
Description: Generates a word count dictionary from the Gettysburg Address.
=========================================== """

# Import libraries
import re

def main():
    print("Word Count from the Gettysburg Address")
    word_count_dict = {}
    # Open and read the Gettysburg Address file
    try:
        with open('gettysburg.txt', 'r') as fileHandle:
            for line in fileHandle:
                process_line(line, word_count_dict)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    # Print the word count dictionary to console
    pretty_print(word_count_dict)

def process_line(line, word_count_dict):
    # Remove punctuation and whitespace using regex and convert to lowercase
    line = re.sub(r'[^A-Za-z0-9\s]', '', line)
    words = line.lower().split()
    # Tally word counts
    add_word(words, word_count_dict)

def add_word(words, word_count_dict):
    # Add words to the dictionary and tally counts
    for word in words:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1

def pretty_print(word_count_dict):
    # Sort by count descending, then alphabetically
    sorted_words = sorted(word_count_dict.items(), key=lambda item: (-item[1], item[0]))
    # Print in a formatted table
    print("\nCurrent Word Counts:")
    print(f"{'Word':<15}{'Count':<10}")
    print("-" * 25)
    for word, count in sorted_words:
        print(f"{word:<15}{count:<10}")
    # Print total unique words
    print(f"\nTotal unique words: {len(word_count_dict)}")

# Run the main function
main()
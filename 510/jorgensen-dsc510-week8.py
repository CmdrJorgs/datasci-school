""" ============================================
Title: Assignment 8.1
Author: David Jorgensen
Course: DSC 510
Date: 23 October 2025
Description: Generates a word count dictionary from the Gettysburg Address.
=========================================== """

# CHANGE LOG
# 19 October 2025: Initial release 
# 23 October 2025: Added process_file()
# 27 October 2025: Added file overwrite confirmation

# Import libraries
import re
import os

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
    # Ask user for output filename
    print("\nProcessing complete, saving to text file. What do you want to name it?")
    output_filename = input("Enter output filename: ")
    # Ensure output filename has .txt extension
    if not output_filename.endswith('.txt'):
        output_filename += '.txt'
    # Check if output file already exists
    if os.path.isfile(output_filename):
        print(f"Warning: The file '{output_filename}' already exists and will be overwritten.")
        # ask for user confirmation
        confirmation = input("Do you want to continue? (y/n): ")
        if confirmation.lower() == 'y':
            process_file(output_filename, word_count_dict)
        else:
            print("Operation cancelled. No changes were made.")
    else:
        # Write the word count dictionary to the specified file
        process_file(output_filename, word_count_dict)
        return

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

def process_file(output_filename, word_count_dict):
    try:
        with open(output_filename, 'w') as fileHandle:
            # Sort by count descending, then alphabetically
            sorted_words = sorted(word_count_dict.items(), key=lambda item: (-item[1], item[0]))
            # Write header
            fileHandle.write(f"{'Word':<15}{'Count':<10}\n")
            fileHandle.write("-" * 25 + "\n")
            # Write each word and its count
            for word, count in sorted_words:
                fileHandle.write(f"{word:<15}{count:<10}\n")
            # Write total unique words
            fileHandle.write(f"\nTotal unique words: {len(word_count_dict)}\n")
            fileHandle.close()
        # Get file path
        full_path = os.path.abspath(output_filename)
        # Verify file creation and print clickable file link to console
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File {full_path} was not created successfully.")
        else:
            print(f"Word count data successfully saved to {full_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# Run the main function
main()
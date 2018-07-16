"""

Author: Cole Helbling
Description: Parse a given file for digits same as input and output
             matching word (most likely through a dict(key, value)
             system).

             For an explanation of Diceware, see:
                http://world.std.com/~reinhold/diceware.html


TODO: Make modular (eg support weird formats of 6 die rolled instead of only 5)
      -- requires file to support 6 digits

"""
import re
import argparse


def main():
    """
    Ask user for name of file containing entries in format of
        `#####{WHITESPACE}str`, warn that any not in that format are dropped
        from the list. make_list(filename) and then match_word(list, value),
        where value is the result of the die rolls.
    """
    print("Contents of file must be in the format of '#####{WHITESPACE}str'!\n")
    parser = argparse.ArgumentParser()
    parser.add_argument("wordlist", nargs='?')
    args = parser.parse_args()

    if not args.wordlist:
        inputs = input("What is the full filename of the word list you are using? ")
    else:
        inputs = args.wordlist

    try:
        open(inputs)
    except FileNotFoundError:
        print("File not found! Make sure the name matches exactly!")
        exit(1)

    # die_length = int(input("How many die are you going to roll per segment? "))
    words = []
    numbers = []
    die_length = 5  # see TODO
    num_rolls = int(input("How many times did you roll the "
                          + str(die_length) + " die? "))

    wordlist = make_list(inputs)
    for x in range(1, num_rolls+1):
        try:
            number = int(input("Input dice roll #" + str(x) + ": "))
            numbers.append(number)
            words.append(match_word(wordlist, number))
        except ValueError:
            print("Must be a number " + str(die_length) + " digits in length!")

    print("\n{}\n{}".format(' '.join(map(str, numbers)), ' '.join(words)))


def match_word(wordlist, search):
    """
    If validate_input(),

    :param wordlist: list of dicts to search keys for value
    :param search: list[element][key] (key input should be str()'d to search for
    :return: matched word
    """
    match = ''

    for elements in wordlist:
        for key in elements:
            if key == str(search):
                match = elements[key]

    return match


def make_list(file):
    """
    Make a list containing {'#': 'str'} for each entry in file

    :param file: file with entries in format `######{WHITESPACE}str`
    :return: list of dicts
    """
    pattern = re.compile("^[\d]+.*", re.M)
    final = []

    with open(file) as f:
        for line in f:
            found = pattern.findall(line)
            data = [item.split() for item in found]
            final.append(dict(data))
    final = [i for i in final if i]

    return final


if __name__ == "__main__":
    main()

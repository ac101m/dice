#!/usr/bin/env python3

'''
DND dice thing.

Usage:
    dice roll <rolltype>
    dice check <rolltype> <samples>

options:
    -h --help  Show this help message.
'''

import docopt
import random

DICE_VALUES = {
    "4": 4,
    "6": 6,
    "8": 8,
    "10": 10,
    "12": 12,
    "20": 20,
    "%": 100
}

def error(message):
    print(message)
    exit(1)

def random_number(max):
    return random.randint(1, max)

def parse_roll_type(command):
    error_message = "Invalid roll command '{}'.".format(command)
    tokens = command.split("d")
    if len(tokens) != 2:
        error(error_message)
    count = None
    try:
        count = int(tokens[0])
    except:
        error(error_message)
    dice_type = tokens[1]
    if dice_type not in DICE_VALUES:
        error(error_message)
    return (DICE_VALUES[dice_type], count)

def calculate_rolls(roll_type):
    (value, count) = parse_roll_type(roll_type)
    return [random_number(value) for r in range(0, count)]

def roll(args):
    roll_type = args["<rolltype>"]
    rolls = calculate_rolls(roll_type)
    print("Rolls: {}".format(rolls))
    print("Total: {}".format(sum(rolls)))
    if roll_type == "2d20":
        print("Advantage: {}".format(max(rolls)))
        print("Disadvantage: {}".format(min(rolls)))

def check(args):
    error("TODO")

def main(args):
    if args["roll"]:
        roll(args)
    elif args["check"]:
        check(args)
    else:
        print("Unrecognized command.")

if __name__ == "__main__":
    main(docopt.docopt(__doc__))

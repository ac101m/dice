#!/usr/bin/env python3

'''
DND dice thing.

Usage:
    dice (-h | --help)
    dice roll <roll-type>
    dice check <dice-type> <roll-count>

options:
    -h --help   Display this help message.
'''

import docopt
import random

# All the dice types and their side counts
DICE_TYPES = {
    "d4": 4,
    "d6": 6,
    "d8": 8,
    "d10": 10,
    "d12": 12,
    "d20": 20,
    "d%": 100
}

# Print a message and exit
def error(message):
    print(message)
    exit(1)

# Random number generator
# Simple implementation for now
def random_number(max):
    return random.randint(0, max)

# Roll a single dice
def roll_dice(side_count):
    return random_number(side_count - 1) + 1

# Calculate serveral rolls
def roll_n_dice(side_count, roll_count):
    return [roll_dice(side_count) for r in range(0, roll_count)]

# Verify dice type string
def get_side_count(dice_type):
    if dice_type not in DICE_TYPES:
        print("{} is not a valid dice type.".format(dice_type))
        dice_type_list = list(DICE_TYPES.keys())
        list_text = ", ".join(dice_type_list[:-1]) + " or {}".format(dice_type_list[-1])
        print("Valid dice types are; {}".format(list_text))
        exit(1)
    
    return DICE_TYPES[dice_type]

# Parse a roll command
def parse_roll_command(command):
    format_error_message = "Invalid command format '{}'. Expecting <count>d<dice-type>".format(command)
    tokens = command.split("d")
    if len(tokens) != 2:
        error(format_error_message)
    try:
        roll_count = int(tokens[0])
    except:
        error(format_error_message)
    side_count = get_side_count("d{}".format(tokens[1]))
    return (side_count, roll_count)

# Perform a roll
def roll(args):
    roll_command = args["<roll-type>"]
    side_count, roll_count = parse_roll_command(roll_command)
    rolls = roll_n_dice(side_count, roll_count)
    print("Rolls: {}".format(rolls))
    print("Total: {}".format(sum(rolls)))
    if roll_command == "2d20":
        print("Advantage: {}".format(max(rolls)))
        print("Disadvantage: {}".format(min(rolls)))

# Check the distribution of the dice rolls
def check(args):
    dice_type = args["<dice-type>"]
    roll_count = int(args["<roll-count>"])
    side_count = get_side_count(dice_type)
    print("Randomness summary for {} {} rolls:".format(roll_count, dice_type))
    frequency_map = {k: 0 for k in range(1, side_count + 1)}
    for i in range(0, roll_count):
        roll = roll_dice(side_count)
        frequency_map[roll] = frequency_map[roll] + 1
    print("VALUE\tCOUNT\tPERCENTAGE")
    for value, count in frequency_map.items():
        percentage = (count / roll_count) * 100
        print("{}:\t{}\t{}%".format(value, count, percentage))

# Main function just checks the top level arguments
def main(args):
    if args["roll"]:
        roll(args)
    elif args["check"]:
        check(args)
    else:
        print("Unrecognized command.")

if __name__ == "__main__":
    main(docopt.docopt(__doc__))

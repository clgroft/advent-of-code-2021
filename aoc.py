#!/usr/bin/env python3

import click
from collections import defaultdict
import sys


def day01(day, lines):
    depths = [ int(l) for l in lines ]

    num_increased_depths = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            num_increased_depths += 1
    print(f"There are {num_increased_depths} increased depths")

    num_increased_windows = 0
    for i in range(3, len(depths)):
        if depths[i] > depths[i-3]:
            num_increased_windows += 1
    print(f"There are {num_increased_windows} inrceased windows")


solutions = defaultdict(lambda : lambda day, lines : print(f"Day {day} not yet implemented"))
solutions[1] = day01


@click.command()
@click.option('--day', default=1, help='Run the solution for this day.')
@click.option('--input_type', default='real', help="Specify input ('real' or 'test')")
def aoc(day, input_type):
    """Run the AOC 2021 solution for the given day, on the real or test input."""

    if input_type != 'real' and input_type != 'test':
        print("Unrecognized input type (must be 'real' or 'test')")
        sys.exit(1)

    if day < 1 or day > 25:
        print("Unrecognized day (must be between 1 and 25 inclusive)")
        sys.exit(1)

    path = f'{input_type}/day{day:0>2d}.txt'
    with open(path) as f:
        lines = f.readlines()
        solutions[day](day, lines)


if __name__ == "__main__":
    aoc()

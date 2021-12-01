#!/usr/bin/env python3

import click
from collections import defaultdict
import sys


solutions = defaultdict(
    lambda : lambda day, part, lines : print(f"Day {day} not yet implemented"))


@click.command()
@click.option('--day', default=1, help='Run the solution for this day.')
@click.option('--part', default=1, help='Specify part of day (1 or 2)')
@click.option('--input_type', default='real', help="Specify input ('real' or 'test')")
def aoc(day, part, input_type):
    """Run the AOC 2021 solution for the given day, on the real or test input."""
    if input_type != 'real' and input_type != 'test':
        print("Unrecognized input type (must be 'real' or 'test')")
        sys.exit(1)

    if day < 1 or day > 25:
        print("Unrecognized day (must be between 1 and 25 inclusive)")
        sys.exit(1)

    if part < 1 or part > 2:
        print("Unrecognized part (must be 1 or 2)")
        sys.exit(1)

    path = f'{input_type}/day{day:0>2d}.txt'
    with open(path) as f:
        lines = f.readlines()
        solutions[day](day, part, lines)


if __name__ == "__main__":
    aoc()

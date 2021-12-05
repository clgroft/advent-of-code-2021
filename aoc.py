#!/usr/bin/env python3

import click
from collections import defaultdict
import sys

from solutions import day01, day02, day03, day04, day05


solutions = defaultdict(lambda : lambda day, lines : print(f"Day {day} not yet implemented"))
solutions[1] = day01.solution
solutions[2] = day02.solution
solutions[3] = day03.solution
solutions[4] = day04.solution
solutions[5] = day05.solution


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

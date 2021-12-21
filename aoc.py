#!/usr/bin/env python3

import click
from collections import defaultdict
import sys

from solutions import (day01, day02, day03, day04, day05, day06, day07, day08,
                       day09, day10, day11, day12, day13, day14, day15, day16,
                       day17, day18, day19, day20, day21)


solutions = defaultdict(lambda : lambda day, lines : print(f"Day {day} not yet implemented"))
solutions[1] = day01.solution
solutions[2] = day02.solution
solutions[3] = day03.solution
solutions[4] = day04.solution
solutions[5] = day05.solution
solutions[6] = day06.solution
solutions[7] = day07.solution
solutions[8] = day08.solution
solutions[9] = day09.solution
solutions[10] = day10.solution
solutions[11] = day11.solution
solutions[12] = day12.solution
solutions[13] = day13.solution
solutions[14] = day14.solution
solutions[15] = day15.solution
solutions[16] = day16.solution
solutions[17] = day17.solution
solutions[18] = day18.solution
solutions[19] = day19.solution
solutions[20] = day20.solution
solutions[21] = day21.solution


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

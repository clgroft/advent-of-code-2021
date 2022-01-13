from collections import Counter
from dataclasses import dataclass
from functools import reduce
from itertools import takewhile, dropwhile
import numpy as np
import re


def solution(day, lines):
    full_solution = Solution(scans(lines))
    full_solution.compute()
    print(f'Found {full_solution.num_beacons()} beacons')
    print('Max Manhattan distance:',
          full_solution.max_manhattan_distance())


def scans(lines):
    def paragraphs():
        buffer = lines
        while buffer:
            yield list(takewhile(str.strip, buffer))
            buffer = list(dropwhile(lambda l: not l.strip(),
                                    dropwhile(str.strip, buffer)))

    beacon_line = re.compile('^(-?\d+),(-?\d+),(-?\d+)$')
    def scan(paragraph):
        return set(
            (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            for m in (beacon_line.match(l) for l in paragraph[1:]))

    return [scan(p) for p in paragraphs()]


class Solution:
    def __init__(self, original_scans):
        self._placed_scans = {
            0: PlacedScan(np.array((0,0,0)), original_scans[0])
        }
        self._unplaced_scan_indices = set(range(1, len(original_scans)))
        self._failed_matches = set()
        self._all_rotated_scans = [[rotate(r, os) for r in ROTATIONS]
                                   for os in original_scans]

    def compute(self):
        while self._unplaced_scan_indices:
            self._find_single_match()

    def num_beacons(self):
        return len(reduce(set.union,
                          map(lambda ps: ps.beacons,
                              self._placed_scans.values())))

    def max_manhattan_distance(self):
        return max(sum(abs(ps1.position - ps2.position))
                   for ps1 in self._placed_scans.values()
                   for ps2 in self._placed_scans.values())

    def _find_single_match(self):
        for i in self._unplaced_scan_indices:
            for j, placed_scan in self._placed_scans.items():
                if (i,j) in self._failed_matches:
                    continue
                beacon_set_rotations = self._all_rotated_scans[i]
                result = next(try_to_fit(beacon_set_rotations, placed_scan),
                              None)
                if result:
                    self._placed_scans[i] = result
                    self._unplaced_scan_indices.remove(i)
                    print(f'Placed scan {i}: location is {result.position}')
                    return
                else:
                    self._failed_matches.add((i,j))
        raise MatchNotFoundException()


class MatchNotFoundException(Exception):
    ...


@dataclass
class PlacedScan:
    position: np.array
    beacons: set(tuple([int, int, int]))


def try_to_fit(rotated_beacon_sets, placed_scan):
    return (result
            for beacon_set in rotated_beacon_sets
            for result in try_to_fit_rotated(beacon_set, placed_scan))


def try_to_fit_rotated(beacon_set, ps):
    s, cnt = Counter(tuple(b2-b1)
                     for b1 in beacon_set
                     for b2 in ps.beacons).most_common(1)[0]
    if cnt >= 12:
        s = np.array(s)
        yield PlacedScan(s, shift(beacon_set, s))


def rotate(r, beacon_set):
    return list(np.matmul(r, b) for b in beacon_set)


def shift(beacon_set, vec):
    return set(tuple(b + vec) for b in beacon_set)


ROTATIONS = list(map(np.array,
                [
                    [[1,0,0],[0,1,0],[0,0,1]], [[1,0,0],[0,-1,0],[0,0,-1]],
                    [[-1,0,0],[0,1,0],[0,0,-1]], [[-1,0,0],[0,-1,0],[0,0,1]],

                    [[1,0,0],[0,0,1],[0,-1,0]], [[1,0,0],[0,0,-1],[0,1,0]],
                    [[-1,0,0],[0,0,1],[0,1,0]], [[-1,0,0],[0,0,-1],[0,-1,0]],

                    [[0,1,0],[1,0,0],[0,0,-1]], [[0,1,0],[-1,0,0],[0,0,1]],
                    [[0,-1,0],[1,0,0],[0,0,1]], [[0,-1,0],[-1,0,0],[0,0,-1]],

                    [[0,1,0],[0,0,1],[1,0,0]], [[0,1,0],[0,0,-1],[-1,0,0]],
                    [[0,-1,0],[0,0,1],[-1,0,0]], [[0,-1,0],[0,0,-1],[1,0,0]],

                    [[0,0,1],[1,0,0],[0,1,0]], [[0,0,1],[-1,0,0],[0,-1,0]],
                    [[0,0,-1],[1,0,0],[0,-1,0]], [[0,0,-1],[-1,0,0],[0,1,0]],

                    [[0,0,1],[0,1,0],[-1,0,0]], [[0,0,1],[0,-1,0],[1,0,0]],
                    [[0,0,-1],[0,1,0],[1,0,0]], [[0,0,-1],[0,-1,0],[-1,0,0]]
                ]))

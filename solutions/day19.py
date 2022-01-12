from collections import Counter
from dataclasses import dataclass
from functools import reduce
import numpy as np
import re


def solution(day, lines):
    interim_solution = InterimSolution(scans(lines))
    if not interim_solution.find_matches():
        return
    print(f'Found {interim_solution.num_beacons()} beacons')
    print(f'Max Manhattan distance: {interim_solution.max_manhattan_distance()}')


def scans(lines):
    original_scans = []
    latest_scan = None
    header_line = re.compile('^--- scanner (\d+) ---$')
    beacon_line = re.compile('^(-?\d+),(-?\d+),(-?\d+)$')

    for l in lines:
        m = header_line.match(l)
        if m:
            latest_scan = set()
            continue

        m = beacon_line.match(l)
        if m:
            latest_scan.add((int(m.group(1)), int(m.group(2)), int(m.group(3))))
            continue

        # presumably blank line
        original_scans.append(latest_scan)
        latest_scan = None

    if latest_scan is not None:
        original_scans.append(latest_scan)
    return original_scans


class InterimSolution:
    def __init__(self, original_scans):
        self._original_scans = original_scans
        self._placed_scans = {0: PlacedScan(np.array((0,0,0)), original_scans[0])}
        self._unplaced_scan_indices = set(range(1, len(original_scans)))
        self._failed_matches = set()

    def find_matches(self):
        while self._unplaced_scan_indices:
            if not self._find_single_match():
                return False
        return True

    def num_beacons(self):
        return len(reduce(set.union,
                          map(lambda ps: ps.beacons, self._placed_scans.values())))

    def max_manhattan_distance(self):
        return max(sum(abs(ps1.position - ps2.position))
                   for ps1 in self._placed_scans.values()
                   for ps2 in self._placed_scans.values())

    def _find_single_match(self):
        for i in sorted(self._unplaced_scan_indices):
            original_scan = self._original_scans[i]
            for j, placed_scan in self._placed_scans.items():
                if (i,j) in self._failed_matches:
                    continue
                result = try_to_fit(original_scan, placed_scan)
                if result:
                    self._placed_scans[i] = result
                    self._unplaced_scan_indices.remove(i)
                    print(f'Placed scan {i}: location is {result.position}')
                    return True
                else:
                    self._failed_matches.add((i,j))
        print('Failed to find match')
        return False


@dataclass
class PlacedScan:
    position: np.array
    beacons: set(tuple([int, int, int]))


def try_to_fit(unrotated_beacon_set, ps):
    for r in ROTATIONS:
        rotated_beacon_set = rotate(r, unrotated_beacon_set)
        result = try_to_fit_rotated(rotated_beacon_set, ps)
        if result:
            return result
    return None


def try_to_fit_rotated(rotated_beacon_set, ps):
    potential_shifts = Counter()
    for b1 in rotated_beacon_set:
        for b2 in ps.beacons:
            potential_shifts[tuple(b2-b1)] += 1
    s, cnt = potential_shifts.most_common(1)[0]
    if cnt >= 12:
        s = np.array(s)
        return PlacedScan(s, shift(rotated_beacon_set, s))
    else:
        return None


def rotate(r, unrotated_beacon_set):
    return list(np.matmul(r, b) for b in unrotated_beacon_set)


def shift(rotated_beacon_set, vec):
    return set(tuple(b + vec) for b in rotated_beacon_set)


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

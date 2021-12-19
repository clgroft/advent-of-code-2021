from collections import Counter
from functools import reduce
import numpy as np
import re


HEADER_LINE = re.compile('^--- scanner (\d+) ---$')
BEACON_LINE = re.compile('^(-?\d+),(-?\d+),(-?\d+)$')

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


class PlacedScan:
    def __init__(self, position, beacons):
        self.position = position
        self.beacons = beacons


def solution(day, lines):
    original_scans = scans(lines)
    placed_scans = {0: PlacedScan(np.array((0,0,0)), original_scans[0])}
    unplaced_scan_indices = set(range(1,len(original_scans)))
    failed_matches = set()
    while unplaced_scan_indices:
        found_match = False
        for i in sorted(unplaced_scan_indices):
            if found_match:
                break
            for j, ps in placed_scans.items():
                if (i,j) in failed_matches:
                    continue
                result = try_to_fit(original_scans[i], ps)
                if result:
                    found_match = True
                    placed_scans[i] = result
                    unplaced_scan_indices.remove(i)
                    print(f'Placed scan {i}: location is {result.position}')
                    break
                else:
                    failed_matches.add((i,j))
        if not found_match:
            print(f'Failed to find match')
            return
    print(f'Placed all scans!')

    all_beacons = reduce(set.union, map(lambda ps: ps.beacons, placed_scans.values()))
    print(f'Found {len(all_beacons)} beacons')

    max_manhattan_distance = 0
    for ps1 in placed_scans.values():
        for ps2 in placed_scans.values():
            distance = sum(abs(ps1.position - ps2.position))
            if distance > max_manhattan_distance:
                max_manhattan_distance = distance
    print(f'Max Manhattan distance: {max_manhattan_distance}')


def scans(lines):
    original_scans = []
    latest_scan = None
    for l in lines:
        m = HEADER_LINE.match(l)
        if m:
            latest_scan = set()
            continue
        m = BEACON_LINE.match(l)
        if m:
            latest_scan.add((int(m.group(1)), int(m.group(2)), int(m.group(3))))
            continue
        # presumably blank line
        original_scans.append(latest_scan)
        latest_scan = None
    if latest_scan is not None:
        original_scans.append(latest_scan)
    return original_scans


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
    for s, cnt in potential_shifts.items():
        if cnt >= 12:
            s = np.array(s)
            return PlacedScan(s, shift(rotated_beacon_set, s))
    return None


def rotate(r, unrotated_beacon_set):
    return list(np.matmul(r, b) for b in unrotated_beacon_set)


def shift(rotated_beacon_set, vec):
    return set(tuple(b + vec) for b in rotated_beacon_set)

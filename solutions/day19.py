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


def scans(lines):
    original_scans = []
    latest_scan = None
    for l in lines:
        m = HEADER_LINE.match(l)
        if m:
            latest_scan = []
            continue
        m = BEACON_LINE.match(l)
        if m:
            latest_scan.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
            continue
        # presumably blank line
        original_scans.append(latest_scan)
        latest_scan = None
    if latest_scan is not None:
        original_scans.append(latest_scan)
    return list(map(np.array, original_scans))


def solution(day, lines):
    original_scans = scans(lines)
    placed_scans = {0: original_scans[0]}
    unplaced_scans = list(range(1,len(original_scans)))

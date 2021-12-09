from collections import Counter
from functools import reduce
from operator import mul


HEIGHT_MAP = []


class Point:
    # Compass directions: N = previous row, E = next column, etc.
    N = 0
    E = 1
    S = 2
    W = 3

    def __init__(self, i, j, height):
        self.down = [False] * 4
        self._color = 'white'  # for DFS
        self._basin_center = None
        self._i, self._j = i, j
        self.height = height

    def is_low_point(self):
        return all(not d for d in self.down)

    def basin_center(self):
        if self._color == 'black':
            return self._basin_center
        elif self._color == 'gray':
            return 'gray'
        else:  # self._color == 'white'
            self._color = 'gray'
            self._basin_center = self._find_basin_center()
            self._color = 'black'
            return self._basin_center

    def _find_basin_center(self):
        if self.is_low_point():
            return (self._i, self._j)
        if self.height == 9:
            return None

        if self.down[Point.N]:
            maybe_center = HEIGHT_MAP[self._i-1][self._j].basin_center()
            if maybe_center != 'gray':
                return maybe_center
        if self.down[Point.E]:
            maybe_center = HEIGHT_MAP[self._i][self._j+1].basin_center()
            if maybe_center != 'gray':
                return maybe_center
        if self.down[Point.S]:
            maybe_center = HEIGHT_MAP[self._i+1][self._j].basin_center()
            if maybe_center != 'gray':
                return maybe_center
        if self.down[Point.W]:
            maybe_center = HEIGHT_MAP[self._i][self._j-1].basin_center()
            if maybe_center != 'gray':
                return maybe_center

        # shouldn't reach this point
        return None


def solution(day, lines):
    global HEIGHT_MAP
    HEIGHT_MAP = [[Point(i, j, int(c)) for j, c in enumerate(line.strip())]
                  for i, line in enumerate(lines)]

    for i in range(len(HEIGHT_MAP) - 1):
        row_i, row_ip1 = HEIGHT_MAP[i], HEIGHT_MAP[i+1]
        for j in range(len(row_i)):
            if row_i[j].height >= row_ip1[j].height:
                row_i[j].down[Point.S] = True
            if row_i[j].height <= row_ip1[j].height:
                row_ip1[j].down[Point.N] = True
    for i in range(len(HEIGHT_MAP)):
        row_i = HEIGHT_MAP[i]
        for j in range(len(row_i) - 1):
            if row_i[j].height >= row_i[j+1].height:
                row_i[j].down[Point.E] = True
            if row_i[j].height <= row_i[j+1].height:
                row_i[j+1].down[Point.W] = True

    total_risk_level = sum(pt.height + 1
                           for row in HEIGHT_MAP
                           for pt in row
                           if pt.is_low_point())
    print(f'Total risk level: {total_risk_level}')

    basin_sizes = Counter()
    for row in HEIGHT_MAP:
        for point in row:
            basin_center = point.basin_center()
            if basin_center is not None:
                basin_sizes[basin_center] += 1

    three_biggest = [j for pt, j in basin_sizes.most_common(3)]
    prod = reduce(mul, three_biggest)
    print(f'Product of three biggest basins: {prod}')

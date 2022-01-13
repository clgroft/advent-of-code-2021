from collections import Counter


class VentLine:
    def __init__(self, line):
        words = line.split()
        start_pt = words[0].split(',')
        end_pt = words[2].split(',')
        self.start_x = int(start_pt[0])
        self.start_y = int(start_pt[1])
        self.end_x = int(end_pt[0])
        self.end_y = int(end_pt[1])

    def covered_points_1(self):
        """Return list of (x,y) points covered by line.

        For now, only consider horizontal and vertical lines; ignore
        diagonals.
        """
        if self.start_x == self.end_x:
            return self._vertical_line()
        if self.start_y == self.end_y:
            return self._horizontal_line()
        else:
            return []

    def covered_points_2(self):
        """Return list of (x,y) points covered by line.

        Now allow diagonals; we assume all diagonals are at 45 degrees
        from horizontal/vertical.
        """
        if self.start_x == self.end_x:
            return self._vertical_line()
        if self.start_y == self.end_y:
            return self._horizontal_line()
        else:
            return self._diagonal_line()

    def _vertical_line(self):
        start_y, end_y = self.start_y, self.end_y
        if start_y > end_y:
            start_y, end_y = end_y, start_y
        for y in range(start_y, end_y + 1):
            yield (self.start_x, y)

    def _horizontal_line(self):
        start_x, end_x = self.start_x, self.end_x
        if start_x > end_x:
            start_x, end_x = end_x, start_x
        for x in range(start_x, end_x + 1):
            yield (x, self.start_y)

    def _diagonal_line(self):
        start_x, end_x = self.start_x, self.end_x
        start_y, end_y, inc_y = self.start_y, self.end_y, 1
        if start_x > end_x:
            start_x, end_x = end_x, start_x
            start_y, end_y = end_y, start_y
        if start_y > end_y:
            inc_y = -1

        x, y = start_x, start_y
        while x <= end_x:
            yield (x, y)
            x += 1
            y += inc_y


def solution(day, lines):
    vent_lines = [VentLine(line) for line in lines]

    covered_points = Counter(
        p for v in vent_lines for p in v.covered_points_1())
    num_crossings = sum(1 for v in covered_points.values() if v > 1)
    print(f'Part 1: There are {num_crossings} crossings')

    covered_points = Counter(
        p for v in vent_lines for p in v.covered_points_2())
    num_crossings = sum(1 for v in covered_points.values() if v > 1)
    print(f'Part 2: There are {num_crossings} crossings')

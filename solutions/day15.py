from heapq import heappush, heappop


class Cavern:
    """Finds the least risky path to any point in the given cavern.

    At present, only the path to the lower right corner matters.
    """
    def __init__(self, lines, replicate=False):
        simple_risk_levels = [[int(c) for c in l.strip()] for l in lines]
        if replicate:
            self._max_row = len(simple_risk_levels) * 5 - 1
            self._max_col = len(simple_risk_levels[0]) * 5 - 1
            self._risk_levels = [[None for _ in range(self._max_col + 1)]
                                for _ in range(self._max_row + 1)]
            for y in range(5):
                for i in range(len(simple_risk_levels)):
                    ip = len(simple_risk_levels) * y + i
                    for x in range(5):
                        for j in range(len(simple_risk_levels[0])):
                            jp = len(simple_risk_levels[0]) * x + j
                            risk = (simple_risk_levels[i][j] + y + x) % 9
                            self._risk_levels[ip][jp] = 9 if risk == 0 else risk
        else:
            self._risk_levels = simple_risk_levels
            self._max_row = len(self._risk_levels) - 1
            self._max_col = len(self._risk_levels[0]) - 1

    def find_all_shortest_paths(self):
        self._shortest_paths = [[None for j in range(self._max_col + 1)]
                               for i in range(self._max_row + 1)]
        heap = [(0,0,0)]  # cost, row, col
        while heap:
            distance, i, j = heappop(heap)
            if self._shortest_paths[i][j] is None:
                self._shortest_paths[i][j] = distance
                for ip, jp in self._neighbors(i, j):
                    heappush(heap, (distance + self._risk_levels[ip][jp], ip, jp))

    def shortest_path_to_bottom_right(self):
        return self._shortest_paths[self._max_row][self._max_col]

    def _neighbors(self, i, j):
        if i > 0:
            yield (i-1, j)
        if i < self._max_row:
            yield (i+1, j)
        if j > 0:
            yield (i, j-1)
        if j < self._max_col:
            yield (i, j+1)


class NaiveCavern(Cavern):
    """Only considers paths that only go right and down.

    I wanted to see whether the puzzle creator played a nasty trick and made
    test input that would work with the naive algorithm and real input that
    wouldn't.  Spoiler alert: they did!"""
    def __init__(self, lines, replicate=False):
        super().__init__(lines, replicate)

    def find_all_shortest_paths(self):
        self._shortest_paths = [[None for j in range(self._max_col + 1)]
                                for i in range(self._max_row + 1)]
        self._shortest_paths[0][0] = 0
        for j in range(self._max_col):
            self._shortest_paths[0][j+1] = (self._shortest_paths[0][j] +
                                            self._risk_levels[0][j+1])
        for i in range(self._max_row):
            self._shortest_paths[i+1][0] = (self._shortest_paths[i][0] +
                                            self._risk_levels[i+1][0])
            for j in range(self._max_col):
                base = min(self._shortest_paths[i+1][j],
                           self._shortest_paths[i][j+1])
                self._shortest_paths[i+1][j+1] = base + self._risk_levels[i+1][j+1]


def solution(day, lines):
    print()
    print('Correct solution:')
    cavern = Cavern(lines)
    cavern.find_all_shortest_paths()
    distance = cavern.shortest_path_to_bottom_right()
    print(f'Part 1: Shortest distance to bottom right: {distance}')

    cavern = Cavern(lines, replicate=True)
    cavern.find_all_shortest_paths()
    distance = cavern.shortest_path_to_bottom_right()
    print(f'Part 2: Shortest distance to bottom right: {distance}')
    print()

    print('Naive solution:')
    cavern = NaiveCavern(lines)
    cavern.find_all_shortest_paths()
    distance = cavern.shortest_path_to_bottom_right()
    print(f'Part 1: Shortest distance to bottom right: {distance}')

    cavern = NaiveCavern(lines, replicate=True)
    cavern.find_all_shortest_paths()
    distance = cavern.shortest_path_to_bottom_right()
    print(f'Part 2: Shortest distance to bottom right: {distance}')
    print()

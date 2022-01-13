from heapq import heappush, heappop


class Cavern:
    """Finds the least risky path to any point in the given cavern.

    At present, only the path to the lower right corner matters.
    """
    def __init__(self, lines, replicate=False):
        simple_risk_levels = [[int(c) for c in l.strip()] for l in lines]
        if replicate:
            self.max_row = len(simple_risk_levels) * 5 - 1
            self.max_col = len(simple_risk_levels[0]) * 5 - 1
            self.risk_levels = [[None for _ in range(self.max_col + 1)]
                                for _ in range(self.max_row + 1)]
            for y in range(5):
                for i in range(len(simple_risk_levels)):
                    ip = len(simple_risk_levels) * y + i
                    for x in range(5):
                        for j in range(len(simple_risk_levels[0])):
                            jp = len(simple_risk_levels[0]) * x + j
                            risk = (simple_risk_levels[i][j] + y + x) % 9
                            self.risk_levels[ip][jp] = 9 if risk == 0 else risk
        else:
            self.risk_levels = simple_risk_levels
            self.max_row = len(self.risk_levels) - 1
            self.max_col = len(self.risk_levels[0]) - 1

    def find_all_shortest_paths(self):
        self.shortest_paths = [[None for j in range(self.max_col + 1)]
                               for i in range(self.max_row + 1)]
        heap = [(0,0,0)]  # cost, row, col
        while heap:
            distance, i, j = heappop(heap)
            if self.shortest_paths[i][j] is None:
                self.shortest_paths[i][j] = distance
                for ip, jp in self._neighbors(i, j):
                    heappush(heap, (distance + self.risk_levels[ip][jp], ip, jp))

    def shortest_path_to_bottom_right(self):
        return self.shortest_paths[self.max_row][self.max_col]

    def _neighbors(self, i, j):
        neighbors = []
        if i > 0:
            neighbors.append((i-1,j))
        if i < self.max_row:
            neighbors.append((i+1,j))
        if j > 0:
            neighbors.append((i,j-1))
        if j < self.max_col:
            neighbors.append((i,j+1))
        return neighbors


class NaiveCavern(Cavern):
    """Only considers paths that only go right and down.

    I wanted to see whether the puzzle creator played a nasty trick and made
    test input that would work with the naive algorithm and real input that
    wouldn't.  Spoiler alert: they did!"""
    def __init__(self, lines, replicate=False):
        super().__init__(lines, replicate)

    def find_all_shortest_paths(self):
        self.shortest_paths = [[None for j in range(self.max_col + 1)]
                               for i in range(self.max_row + 1)]
        self.shortest_paths[0][0] = 0
        for j in range(self.max_col):
            self.shortest_paths[0][j+1] = (self.shortest_paths[0][j] +
                                           self.risk_levels[0][j+1])
        for i in range(self.max_row):
            self.shortest_paths[i+1][0] = (self.shortest_paths[i][0] +
                                           self.risk_levels[i+1][0])
            for j in range(self.max_col):
                base = min(self.shortest_paths[i+1][j],
                           self.shortest_paths[i][j+1])
                self.shortest_paths[i+1][j+1] = base + self.risk_levels[i+1][j+1]


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

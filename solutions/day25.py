class SeaFloor:
    def __init__(self, lines):
        self._state = [list(line.strip()) for line in lines]
        self._nrows = len(self._state)
        self._ncols = len(self._state[0])

    def step(self):
        """Attempts one step for all sea cucumbers.

        Returns True if any moved, False otherwise."""
        any_moves = False

        # First move the east herd
        should_move = [[False for c in row] for row in self._state]
        for i, row in enumerate(self._state):
            for j, cell in enumerate(row):
                if cell == '>':
                    should_move[i][j] = (row[(j+1) % self._ncols] == '.')
        for i, row in enumerate(self._state):
            for j in range(self._ncols):
                if should_move[i][j]:
                    any_moves = True
                    row[(j+1) % self._ncols] = '>'
                    row[j] = '.'

        # Then move the south herd
        should_move = [[False for c in row] for row in self._state]
        for i, row in enumerate(self._state):
            for j, cell in enumerate(row):
                if cell == 'v':
                    should_move[i][j] = (
                        self._state[(i+1) % self._nrows][j] == '.')
        for i, row in enumerate(self._state):
            for j in range(self._ncols):
                if should_move[i][j]:
                    any_moves = True
                    self._state[(i+1) % self._nrows][j] = 'v'
                    row[j] = '.'

        return any_moves

    def print_state(self):
        for row in self._state:
            print(''.join(row))


def solution(day, lines):
    sea_floor = SeaFloor(lines)
    num_steps = 0

    while sea_floor.step():
        num_steps += 1

    num_steps += 1
    print(f'Stopped moving after {num_steps} steps')

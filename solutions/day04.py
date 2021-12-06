class Board:
    def __init__(self, lines):
        self._marks = [[False for j in range(5)] for i in range(5)]
        self._position_from_number = {}
        self._unmarked_numbers = set()
        for i, line in enumerate(lines):
            for j, entry in enumerate(line.split()):
                number = int(entry)
                self._position_from_number[number] = (i,j)
                self._unmarked_numbers.add(number)
        self._has_won = False

    def call_number(self, number):
        """Respond to number being called."""
        if self._has_won:
            return None

        pos = self._position_from_number.get(number)
        if pos is None:
            return None
        i, j = pos

        self._mark(i, j, number)
        if self._is_victory(i, j):
            self._has_won = True
            return self._score(number)
        else:
            return None

    def _mark(self, i, j, number):
        self._marks[i][j] = True
        self._unmarked_numbers.remove(number)

    def _is_victory(self, i, j):
        return all(self._marks[i]) or all(row[j] for row in self._marks)

    def _score(self, number):
        """Return score, i.e., sum of unmarked numbers times called number."""
        return number * sum(self._unmarked_numbers)

    def _is_marked(self, pos):
        i, j = pos
        return self._marks[i][j]


def solution(day, lines):
    call_sequence = [int(n) for n in lines[0].split(',')]
    lines = lines[2:]
    boards = []
    while lines:
        boards.append(Board(lines[:5]))
        lines = lines[6:]

    winning_scores = []
    for number in call_sequence:
        for board in boards:
            score = board.call_number(number)
            if score is not None:
                winning_scores.append(score)

    print(f'First winning score: {winning_scores[0]}')
    print(f'Last winning score:  {winning_scores[-1]}')

class Board:
    def __init__(self, lines):
        self.marks = [ [False for j in range(5)] for i in range(5)]
        self.position_from_number = {}
        for i, line in enumerate(lines):
            for j, entry in enumerate(line.split()):
                self.position_from_number[int(entry)] = [i,j]
        self.has_won = False


    def call_number(self, number):
        """Respond to number being called."""
        if self.has_won:
            return None

        pos = self.position_from_number.get(number)
        if pos is None:
            return None
        i, j = pos

        self.mark(i,j)
        if self.is_victory(i,j):
            self.has_won = True
            return self.score(number)
        else:
            return None


    def mark(self, i, j):
        """Mark number on this board."""
        self.marks[i][j] = True


    def is_victory(self, i, j):
        """Check victory condition along row and column of pos."""
        return all(self.marks[i]) or all(row[j] for row in self.marks)


    def score(self, number):
        """Return score, i.e., sum of unmarked numbers times called number."""
        return number * (
                sum(num for num, pos in self.position_from_number.items()
                    if not self.is_marked(pos)))


    def is_marked(self, pos):
        """Return True if position is marked."""
        i, j = pos
        return self.marks[i][j]


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
            if score:
                winning_scores.append(score)

    print(f'First winning score: {winning_scores[0]}')
    print(f'Last winning score:  {winning_scores[-1]}')

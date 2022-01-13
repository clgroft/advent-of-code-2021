from dataclasses import dataclass
from statistics import median


OPEN_CHARS = set(['(', '[', '{', '<'])
OPEN_FOR_CLOSE = {')': '(', ']': '[', '}': '{', '>': '<'}
SCORE_FOR_CLOSE = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORE_FOR_OPEN = {'(': 1, '[': 2, '{': 3, '<': 4}


@dataclass
class Result:
    error_type: str
    score: int


def error_type_and_score(line):
    stack = []
    for c in line:
        if c in OPEN_CHARS:
            stack.append(c)
        elif stack.pop() != OPEN_FOR_CLOSE[c]:
            return Result('corrupted', SCORE_FOR_CLOSE[c])

    if not stack:
        return Result('none', 0)  # this shouldn't actually happen

    score = 0
    while stack:
        score = score * 5 + SCORE_FOR_OPEN[stack.pop()]
    return Result('incomplete', score)


def solution(day, lines):
    results = [error_type_and_score(l.strip()) for l in lines]

    se_score = sum(
        r.score for r in results if r.error_type == 'corrupted')
    print(f'Total syntax error score: {se_score}')

    median_ac_score = median(
        r.score for r in results if r.error_type == 'incomplete')
    print(f'Median autocomplete score: {median_ac_score}')

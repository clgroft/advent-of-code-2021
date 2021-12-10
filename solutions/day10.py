from statistics import median


OPEN_CHARS = set(['(', '[', '{', '<'])
OPEN_FOR_CLOSE = {')': '(', ']': '[', '}': '{', '>': '<'}
SCORE_FOR_CLOSE = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORE_FOR_OPEN = {'(': 1, '[': 2, '{': 3, '<': 4}


def syntax_error_score(line):
    stack = []
    for c in line:
        if c in OPEN_CHARS:
            stack.append(c)
        elif stack.pop() != OPEN_FOR_CLOSE[c]:  # line is corrupted
            return SCORE_FOR_CLOSE[c]
    return 0  # line is incomplete


def autocomplete_score(line):
    stack = []
    for c in line:
        if c in OPEN_CHARS:
            stack.append(c)
        elif stack.pop() != OPEN_FOR_CLOSE[c]:  # line is corrupted
            return None

    # Line is incomplete
    score = 0
    while stack:
        score = score * 5 + SCORE_FOR_OPEN[stack.pop()]
    return score


def solution(day, lines):
    lines = [l.strip() for l in lines]

    se_score = sum(map(syntax_error_score, lines))
    print(f'Total syntax error score: {se_score}')

    ac_scores = [autocomplete_score(l) for l in lines]
    ac_scores = filter(lambda n : n is not None, ac_scores)
    median_ac_score = median(ac_scores)
    print(f'Median autocomplete score: {median_ac_score}')

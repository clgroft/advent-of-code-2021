import re


POINT_REGEX = re.compile('(\d+),(\d+)')
FOLD_REGEX = re.compile('fold along ([xy])=(\d+)')


def fold(axis, length, points):
    if axis == 'x':
        return fold_along_x(length, points)
    else:  # axis == 'y'
        return fold_along_y(length, points)


def fold_along_x(x, points):
    return set(map(lambda pt: (2*x - pt[0], pt[1]) if pt[0] > x else pt, points))


def fold_along_y(y, points):
    return set(map(lambda pt: (pt[0], 2*y - pt[1]) if pt[1] > y else pt, points))


def display(points):
    max_x, max_y = 0, 0
    for x, y in points:
        max_x = x if x > max_x else max_x
        max_y = y if y > max_y else max_y
    screen = [[' ' for i in range(max_x+1)] for j in range(max_y+1)]
    for x, y in points:
        screen[y][x] = '#'
    for row in screen:
        print(''.join(row))


def solution(day, lines):
    paper = set()
    folds = []
    for l in lines:
        result = POINT_REGEX.match(l)
        if result:
            paper.add((int(result.group(1)),int(result.group(2))))
            continue
        result = FOLD_REGEX.match(l)
        if result:
            folds.append((result.group(1),int(result.group(2))))

    axis, length = folds[0]
    paper = fold(axis, length, paper)
    print(f'After 1 fold, {len(paper)} points')
    print()

    for axis, length in folds[1:]:
        paper = fold(axis, length, paper)

    display(paper)
    print()

from functools import reduce
from operator import add
import re


class ParseException(Exception):
    pass


class SnailNumber:
    def __init__(self):
        pass

    NUMBER_PATTERN = re.compile('^(\d+)(.*)$')

    @classmethod
    def parse(cls, line):
        num, line = cls._parse(line)
        if line and line != '\n': raise ParseException()
        return num

    @classmethod
    def _parse(cls, line):
        m = cls.NUMBER_PATTERN.match(line)
        if m:
            return RegularNumber(int(m.group(1))), m.group(2)
        if line[0] != '[': raise ParseException()
        left, line = cls._parse(line[1:])
        if line[0] != ',': raise ParseException()
        right, line = cls._parse(line[1:])
        if line[0] != ']': raise ParseException()
        return PairNumber(left, right), line[1:]

    def __add__(self, o):
        num = PairNumber(self, o)
        reduced = True
        while reduced:
            _, num, _, reduced = num.explode(4)
            if not reduced:
                num, reduced = num.split()
        return num


class RegularNumber(SnailNumber):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def explode(self, depth):
        return None, self, None, False  # Can't explode a regular number

    def split(self):
        if self.value < 10:
            return self, False
        half = self.value // 2
        return (
            PairNumber(RegularNumber(half), RegularNumber(self.value - half)),
            True)

    def magnitude(self):
        return self.value

    def add_leftmost(self, value):
        return RegularNumber(self.value + value)

    def add_rightmost(self, value):
        return RegularNumber(self.value + value)


class PairNumber(SnailNumber):
    def __init__(self, left, right):
        super().__init__()
        self.left, self.right = left, right

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def explode(self, depth):
        if depth == 0:
            return self.left.value, RegularNumber(0), self.right.value, True

        left_add_left, new_left, left_add_right, exploded = (
            self.left.explode(depth-1))
        if left_add_right is not None:
            new_right = self.right.add_leftmost(left_add_right)
        else:
            new_right = self.right
        if exploded:
            return left_add_left, PairNumber(new_left, new_right), None, True

        right_add_left, new_right, right_add_right, exploded = (
            self.right.explode(depth-1))
        if right_add_left is not None:
            new_left = self.left.add_rightmost(right_add_left)
        else:
            new_left = self.left
        if exploded:
            return None, PairNumber(new_left, new_right), right_add_right, True

        return None, self, None, False

    def split(self):
        new_left, split_left = self.left.split()
        if split_left:
            return PairNumber(new_left, self.right), True
        new_right, split_right = self.right.split()
        if split_right:
            return PairNumber(self.left, new_right), True
        return self, False

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add_leftmost(self, value):
        return PairNumber(self.left.add_leftmost(value), self.right)

    def add_rightmost(self, value):
        return PairNumber(self.left, self.right.add_rightmost(value))


def solution(day, lines):
    numbers = [SnailNumber.parse(l) for l in lines]
    final_sum = reduce(add, numbers)
    print(f'Part 1:')
    print(f'Final sum: {final_sum}')
    print(f'Magnitude: {final_sum.magnitude()}')
    print()

    highest_magnitude = max((n+m).magnitude() for n in numbers for m in numbers)
    print(f'Part 2:')
    print(f'Highest magnitude: {highest_magnitude}')

from collections import defaultdict


class CaveSystem:
    def __init__(self, lines):
        super().__init__()
        self._edges = defaultdict(lambda: [])
        for l in lines:
            start, end = l.strip().split('-')
            self._edges[start].append(end)
            self._edges[end].append(start)

    def num_paths_part_1(self):
        return self._num_paths('start', [], False)

    def num_paths_part_2(self):
        return self._num_paths('start', [], True)

    def _num_paths(self, cave, small_caves, allow_repeat):
        num_paths = 0
        for c in self._edges[cave]:
            if c == 'start':
                pass
            elif c == 'end':
                num_paths += 1
            elif c.islower():
                if c not in small_caves:
                    num_paths += self._num_paths(
                        c, small_caves + [c], allow_repeat)
                elif allow_repeat:
                    num_paths += self._num_paths(c, small_caves, False)
            else:
                num_paths += self._num_paths(c, small_caves, allow_repeat)
        return num_paths


def solution(day, lines):
    cs = CaveSystem(lines)
    num_paths_1 = cs.num_paths_part_1()
    print(f'Part 1: paths from start to end: {num_paths_1}')
    num_paths_2 = cs.num_paths_part_2()
    print(f'Part 2: paths from start to end: {num_paths_2}')

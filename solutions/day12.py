from collections import defaultdict


class CaveSystem:
    def __init__(self, lines):
        super().__init__()
        self._edges = defaultdict(lambda: [])
        for l in lines:
            start, end = l.strip().split('-')
            self._edges[start].append(end)
            self._edges[end].append(start)

    def num_paths_start_to_end(self):
        return self._num_paths_to_end('start', ['start'])

    def _num_paths_to_end(self, cave, small_caves):
        num_paths = 0
        for c in self._edges[cave]:
            if c == 'end':
                num_paths += 1
            elif c.islower():
                num_paths += (0 if c in small_caves
                              else self._num_paths_to_end(c, small_caves + [c]))
            else:
                num_paths += self._num_paths_to_end(c, small_caves)
        return num_paths

    def num_paths_start_to_end_2(self):
        return self._num_paths_to_end_2('start', [], False)

    def _num_paths_to_end_2(self, cave, small_caves, extra_visit):
        num_paths = 0
        for c in self._edges[cave]:
            if c == 'start':
                pass
            elif c == 'end':
                num_paths += 1
            elif c.islower():
                if c not in small_caves:
                    num_paths += self._num_paths_to_end_2(c, small_caves + [c],
                                                          extra_visit)
                elif not extra_visit:
                    num_paths += self._num_paths_to_end_2(c, small_caves, True)
            else:
                num_paths += self._num_paths_to_end_2(c, small_caves,
                                                      extra_visit)
        return num_paths


def solution(day, lines):
    cs = CaveSystem(lines)
    num_paths = cs.num_paths_start_to_end()
    print(f'Part 1: paths from start to end: {num_paths}')
    num_paths_2 = cs.num_paths_start_to_end_2()
    print(f'Part 2: paths from start to end: {num_paths_2}')

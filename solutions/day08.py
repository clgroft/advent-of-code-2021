class Entry:
    SIMPLE_VALUE_LENGTHS = set([2, 3, 4, 7])

    def __init__(self, line):
        sp_line, ov_line = line.strip().split(' | ')
        self._signal_patterns = [tuple(sorted(sp))
                                 for sp in sp_line.split(' ')]
        self._signal_patterns.sort(key=len)
        self._output_values = [tuple(sorted(ov))
                               for ov in ov_line.split(' ')]

    def count_simple(self):
        return sum(1 for ov in self._output_values
                   if len(ov) in self.SIMPLE_VALUE_LENGTHS)

    def displayed_value(self):
        lookups = self._build_lookups()
        return (lookups[self._output_values[0]] * 1000 +
                lookups[self._output_values[1]] *  100 +
                lookups[self._output_values[2]] *   10 +
                lookups[self._output_values[3]])

    def _build_lookups(self):
        lookups = {}

        # _signal_patterns, having been sorted by length, have lengths
        # [2,3,4, 5,5,5, 6,6,6, 7].
        lookups[self._signal_patterns[0]] = 1
        lookups[self._signal_patterns[1]] = 7
        lookups[self._signal_patterns[2]] = 4
        lookups[self._signal_patterns[9]] = 8

        one_set  = set(self._signal_patterns[0])
        four_set = set(self._signal_patterns[2])

        for sp in self._signal_patterns[3:6]:  # length 5
            if one_set.issubset(set(sp)):
                lookups[sp] = 3
            elif len(set(sp) & four_set) == 2:
                lookups[sp] = 2
            else:
                lookups[sp] = 5

        for sp in self._signal_patterns[6:9]:
            if four_set.issubset(sp):
                lookups[sp] = 9
            elif one_set.issubset(sp):
                lookups[sp] = 0
            else:
                lookups[sp] = 6

        return lookups


def solution(day, lines):
    entries = [Entry(l) for l in lines]

    appearances = sum(e.count_simple() for e in entries)
    print(f'The given digits appear {appearances} times')

    sum_displays = sum(e.displayed_value() for e in entries)
    print(f'The displayed numbers sum to {sum_displays}')

from collections import Counter


class PolymerRules:
    def __init__(self, lines):
        polymer_template = lines[0].strip()
        self.elements = Counter(polymer_template)
        self.pairs = Counter(polymer_template[i:i+2]
                             for i in range(len(polymer_template) - 1))
        self.new_elements = {}
        self.rules = {}
        for l in lines[2:]:
            words = l.strip().split(' ')
            self.new_elements[words[0]] = words[2]
            self.rules[words[0]] = [words[0][0] + words[2],
                                    words[2] + words[0][1]]

    def one_step(self):
        new_pairs = Counter()
        for pair, cnt in self.pairs.items():
            self.elements[self.new_elements[pair]] += cnt
            for new_pair in self.rules[pair]:
                new_pairs[new_pair] += cnt
        self.pairs = new_pairs

    def difference(self):
        freq_counts = self.elements.most_common()
        return freq_counts[0][1] - freq_counts[-1][1]


def solution(day, lines):
    polymer_rules = PolymerRules(lines)

    for _ in range(10):
        polymer_rules.one_step()
    print(f'Difference after 10 steps: {polymer_rules.difference()}')

    for _ in range(30):
        polymer_rules.one_step()
    print(f'Difference after 40 steps: {polymer_rules.difference()}')

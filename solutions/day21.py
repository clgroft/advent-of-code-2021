from collections import Counter
import re


class DeterministicD100:
    def __init__(self):
        self._last_roll = 100
        self.times_rolled = 0

    def roll(self):
        self._last_roll = 1 if self._last_roll == 100 else self._last_roll + 1
        self.times_rolled += 1
        return self._last_roll


class QuantumGameStates:
    def __init__(self, position_1, position_2):
        self._possible_die_rolls = Counter()
        for i in range(1,4):
            for j in range(1,4):
                for k in range(1,4):
                    self._possible_die_rolls[i+j+k] += 1
        self._universes = Counter()
        self._universes[(position_1, position_2, 0, 0)] = 1

    def run_simulation(self):
        victories_1, victories_2 = 0, 0
        while True:
            new_universes = Counter()
            for old_state, cnt_state in self._universes.items():
                for roll, cnt_roll in self._possible_die_rolls.items():
                    position_1, position_2, score_1, score_2 = old_state
                    position_1 = (position_1 + roll) % 10
                    score_1 += 10 if position_1 == 0 else position_1
                    if score_1 >= 21:
                        victories_1 += cnt_state * cnt_roll
                    else:
                        new_state = (position_1, position_2, score_1, score_2)
                        new_universes[new_state] += cnt_state * cnt_roll
            self._universes = new_universes
            if not self._universes:
                return max(victories_1, victories_2)
            new_universes = Counter()
            for old_state, cnt_state in self._universes.items():
                for roll, cnt_roll in self._possible_die_rolls.items():
                    position_1, position_2, score_1, score_2 = old_state
                    position_2 = (position_2 + roll) % 10
                    score_2 += 10 if position_2 == 0 else position_2
                    if score_2 >= 21:
                        victories_2 += cnt_state * cnt_roll
                    else:
                        new_state = (position_1, position_2, score_1, score_2)
                        new_universes[new_state] += cnt_state * cnt_roll
            self._universes = new_universes
            if not self._universes:
                return max(victories_1, victories_2)


def solution(day, lines):
    m = re.match('Player 1 starting position: (\d+)', lines[0])
    position_1 = int(m.group(1))
    m = re.match('Player 2 starting position: (\d+)', lines[1])
    position_2 = int(m.group(1))
    die = DeterministicD100()

    losing_score = play_game(position_1, position_2, die)
    print(f'Losing score = {losing_score}, die rolls = {die.times_rolled}')
    print(f'Product: {losing_score * die.times_rolled}')

    qgs = QuantumGameStates(position_1, position_2)
    max_universes = qgs.run_simulation()
    print(f'Maximum universes: {max_universes}')


def play_game(position_1, position_2, die):
    score_1 = 0
    score_2 = 0

    while True:
        die_rolls = die.roll() + die.roll() + die.roll()
        position_1 = (position_1 + die_rolls) % 10
        score_1 += 10 if position_1 == 0 else position_1
        if score_1 >= 1000:
            return score_2
        die_rolls = die.roll() + die.roll() + die.roll()
        position_2 = (position_2 + die_rolls) % 10
        score_2 += 10 if position_2 == 0 else position_2
        if score_2 >= 1000:
            return score_1

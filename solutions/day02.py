class Instruction:
    def __init__(self, line):
        words = line.split()
        self.direction = words[0]
        self.param = int(words[1])


def solution(day, lines):
    instructions = [ Instruction(l) for l in lines ]

    print('Part 1:')

    position = 0
    depth = 0

    for i in instructions:
        if i.direction == 'forward':
            position += i.param
        elif i.direction == 'down':
            depth += i.param
        elif i.direction == 'up':
            depth -= i.param
        else:
            print(f'Unknown direction {i.direction}')

    print(f'Position {position}, depth {depth}, result {position * depth}')

    print('Part 2:')

    position = 0
    depth = 0
    aim = 0

    for i in instructions:
        if i.direction == 'forward':
            position += i.param
            depth += i.param * aim
        elif i.direction == 'down':
            aim += i.param
        elif i.direction == 'up':
            aim -= i.param
        else:
            print(f'Unknown direction {i.direction}')

    print(f'Position {position}, depth {depth}, result {position * depth}')

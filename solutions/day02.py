def solution(day, lines):
    instructions = [ l.split() for l in lines ]

    print('Part 1:')

    position = 0
    depth = 0

    for i in instructions:
        direction = i[0]
        distance = int(i[1])
        if direction == 'forward':
            position += distance
        elif direction == 'down':
            depth += distance
        elif direction == 'up':
            depth -= distance
        else:
            print(f'Unknown direction {direction}')

    print(f'Position {position}, depth {depth}, result {position * depth}')

    print('Part 2:')

    position = 0
    depth = 0
    aim = 0

    for i in instructions:
        direction = i[0]
        param = int(i[1])
        if direction == 'forward':
            position += param
            depth += param * aim
        elif direction == 'down':
            aim += param
        elif direction == 'up':
            aim -= param
        else:
            print(f'Unknown direction {direction}')

    print(f'Position {position}, depth {depth}, result {position * depth}')

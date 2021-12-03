def gamma_epsilon(inputs):
    counts = [ [0,0] for c in inputs[0]]
    for l in inputs:
        for i in range(len(l)):
            counts[i][l[i]] += 1

    gamma_binary = []
    epsilon_binary = []
    for c in counts:
        if c[0] > c[1]:
            gamma_binary.append('0')
            epsilon_binary.append('1')
        else:
            gamma_binary.append('1')
            epsilon_binary.append('0')

    gamma = int(''.join(gamma_binary), 2)
    epsilon = int(''.join(epsilon_binary), 2)
    return gamma, epsilon


def oxygen_generator_rating(inputs):
    for i in range(len(inputs[0])):
        counts = [0,0]
        for val in inputs:
            counts[val[i]] += 1

        if counts[0] > counts[1]:
            inputs = [ val for val in inputs if val[i] == 0 ]
        else:
            inputs = [ val for val in inputs if val[i] == 1 ]

        if len(inputs) == 1:
            return int(''.join([str(i) for i in inputs[0]]), 2)


def co2_scrubber_rating(inputs):
    for i in range(len(inputs[0])):
        counts = [0,0]
        for val in inputs:
            counts[val[i]] += 1

        if counts[0] > counts[1]:
            inputs = [ val for val in inputs if val[i] == 1 ]
        else:
            inputs = [ val for val in inputs if val[i] == 0 ]

        if len(inputs) == 1:
            return int(''.join([str(i) for i in inputs[0]]), 2)


def solution(day, lines):
    lines = [ [ int(c) for c in l.strip() ] for l in lines ]

    print('Part 1:')
    gamma, epsilon = gamma_epsilon(lines)
    print(f'gamma = {gamma}, epsilon = {epsilon}, answer = {gamma * epsilon}')

    print('Part 2:')
    og_rating = oxygen_generator_rating(lines)
    cs_rating = co2_scrubber_rating(lines)
    print(f'Oxygen generator rating = {og_rating}')
    print(f'CO2 scrubber rating = {cs_rating}')
    print(f'Solution = {og_rating * cs_rating}')

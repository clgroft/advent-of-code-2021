def solution(day, lines):
    fish_count = [0] * 9
    for word in lines[0].split(','):
        fish_count[int(word)] += 1

    for i in range(256):
        new_fish_count = [0] * 9
        new_fish_count[:8] = fish_count[1:]
        new_fish_count[6] += fish_count[0]
        new_fish_count[8] = fish_count[0]
        fish_count = new_fish_count
        if i == 79:  # after 80 days
            print(f'After 80 days, {sum(fish_count)} fish')

    print(f'After 256 days, {sum(fish_count)} fish')

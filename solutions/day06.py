def solution(day, lines):
    """Solution for day 6.

    Input is a single line of integers separated by commas, each
    representing a single lanternfish; the integer is the number of days
    to next spawn.  A mature lanternfish spawns every 7 days; a newly
    spawned lanternfish takes 9 days to spawn the first time.

    Output is the total number of lanternfish after 80 and 256 days.
    """

    # fish_count[i] == number of lanternfish which will spawn in i days.
    # E.g. fish_count[0] fish are about to spawn.
    fish_count = [0] * 9
    for word in lines[0].split(','):
        fish_count[int(word)] += 1

    for i in range(256):
        new_fish_count = [0] * 9
        new_fish_count[:8] = fish_count[1:] # counting down to next spawn
        new_fish_count[6] += fish_count[0]  # just spawned, resetting count
        new_fish_count[8] = fish_count[0]   # newly spawned
        fish_count = new_fish_count
        if i == 79 or i == 255:  # after 80 and 256 days
            print(f'After {i+1} days, {sum(fish_count)} fish')

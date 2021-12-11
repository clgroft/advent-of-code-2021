def solution(day, lines):
    energy_levels = [[int(c) for c in l.strip()] for l in lines]
    nrows = len(energy_levels)
    ncols = len(energy_levels[0])

    def neighbors(i,j):
        nbors = [(i-1,j), (i-1,j+1), (i,j+1), (i+1,j+1),
                 (i+1,j), (i+1,j-1), (i,j-1), (i-1,j-1)]
        return [(x,y) for (x,y) in nbors
                if x != -1 and x != nrows and y != -1 and y != ncols]

    num_steps = 0
    num_flashes = 0
    while True:
        if num_steps == 100:
            print(f'Number of flashes after 100 steps: {num_flashes}')

        # First each octopus increases its energy level by 1.
        for row in energy_levels:
            for j in range(ncols):
                row[j] += 1

        # Then any octopus with an energy level greater than 9 flashes. This
        # increases the energy level of all adjacent octupuses by 1.  If this
        # causes an octupus to have an energy level greater than 9, it also
        # flashes (but not more than once per step).  This process continues
        # as long as new octopuses keep having their energy levels increased
        # beyond 9.
        flashed_this_step = set()
        new_flashes_this_substep = True
        while new_flashes_this_substep:
            new_flashes_this_substep = False
            for i in range(nrows):
                for j in range(ncols):
                    if ((i,j) not in flashed_this_step
                            and energy_levels[i][j] > 9):
                        flashed_this_step.add((i,j))
                        new_flashes_this_substep = True
                        for (x,y) in neighbors(i,j):
                            energy_levels[x][y] += 1

        # Finally, any octopus that flashed during this step has its energy set
        # to 0, as it used all of its energy to flash.
        for (i,j) in flashed_this_step:
            energy_levels[i][j] = 0
        num_flashes += len(flashed_this_step)

        num_steps += 1
        if len(flashed_this_step) == nrows * ncols:
            print(f'Number of steps to synchronization: {num_steps}')
            return

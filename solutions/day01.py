def solution(day, lines):
    depths = [ int(l) for l in lines ]

    # Part 1: find the number of depths which are greater than the
    # previous depth.
    num_increased_depths = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            num_increased_depths += 1
    print(f"There are {num_increased_depths} increased depths")

    # Part 2: find the number of 3-depth sliding windows which have greater
    # total sum than the previous window.  Since each window shares two depths
    # with the previous window, it's enough to compare each depth with the
    # depth three measurements ago.
    num_increased_windows = 0
    for i in range(3, len(depths)):
        if depths[i] > depths[i-3]:
            num_increased_windows += 1
    print(f"There are {num_increased_windows} inrceased windows")

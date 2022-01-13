def solution(day, lines):
    depths = [ int(l) for l in lines ]

    # Part 1: find the number of depths which are greater than the
    # previous depth.
    num_increased_depths = sum(
        1 for d1, d2 in zip(depths, depths[1:]) if d1 < d2)
    print(f"There are {num_increased_depths} increased depths")

    # Part 2: find the number of 3-depth sliding windows which have greater
    # total sum than the previous window.  Since each window shares two depths
    # with the previous window, it's enough to compare each depth with the
    # depth three measurements ago.
    num_increased_windows = sum(
        1 for d1, d2 in zip(depths, depths[3:]) if d1 < d2)
    print(f"There are {num_increased_windows} inrceased windows")

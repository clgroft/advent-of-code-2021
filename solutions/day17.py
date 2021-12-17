import re


def solution(day, lines):
    match = re.match('target area: x=(\d+)\.\.(\d+), y=-(\d+)\.\.-(\d+)',
                     lines[0])
    xmin, xmax, ymin, ymax = (
        int(match.group(1)),  int(match.group(2)),
        -int(match.group(3)), -int(match.group(4)))

    # I tried to be clever and kept counting the wrong thing for part 2.
    # This naive solution works in less than a second, which is far less
    # time than I wasted trying to be clever.
    init_velocities = set()
    for init_vx in range(0, xmax+1):
        for init_vy in range(ymin, -ymin + 1):
            t, x, y, vx, vy = 0, 0, 0, init_vx, init_vy
            while y >= ymin:
                t += 1
                x += vx
                y += vy
                vx -= 1 if vx > 0 else 0
                vy -= 1
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    init_velocities.add((init_vx, init_vy))
                    break

    vy_max = max(vy for _, vy in init_velocities)
    print(f'Part 1: Highest point: {vy_max*(vy_max+1)//2}')
    print(f'Part 2: Number of initial velocities: {len(init_velocities)}')

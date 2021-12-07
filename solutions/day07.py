import statistics


def total_fuel_to_point_1(point, positions):
    return sum(abs(n - point) for n in positions)


def total_fuel_to_point_2(point, positions):
    def fuel_used(distance):
        return distance * (distance+1) // 2
    return sum(fuel_used(abs(n - point)) for n in positions)


def solution(day, lines):
    positions = [int(n) for n in lines[0].split(',')]

    # Part 1: assuming each submarine takes a linear amount of fuel to
    # reach a given position, the common position that minimizes the
    # amount of fuel used is the median.
    median = int(statistics.median(positions))
    total_fuel = total_fuel_to_point_1(median, positions)
    print(f'Part 1: Total fuel used: {total_fuel}')

    # Part 2: since the true amount of fuel is quadratic in the distance
    # travelled, the true minimizer should be close to the mean.
    # Moreover the total-fuel function is concave upward as a function
    # of the point reached, so a local minimum will be a true minimum.
    # Thus we manually search near the mean.
    value = round(statistics.mean(positions))
    total_fuel_2 = total_fuel_to_point_2(value, positions)
    while True:
        new_value = value - 1
        new_total_fuel = total_fuel_to_point_2(new_value, positions)
        if new_total_fuel >= total_fuel_2:
            break
        value = new_value
        total_fuel_2 = new_total_fuel
    while True:
        new_value = value + 1
        new_total_fuel = total_fuel_to_point_2(new_value, positions)
        if new_total_fuel >= total_fuel_2:
            break
        value = new_value
        total_fuel_2 = new_total_fuel
    print(f'Part 2: Total fuel used: {total_fuel_2}')

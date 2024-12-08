import os
import functools
import itertools


def parse(path):
    with open(path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]


def solve(grid):
    total = 0
    for count_function in [functools.partial(count_direction, d_y, d_x) for d_y, d_x in itertools.product(range(-1, 2), repeat=2) if d_y != 0 or d_x != 0]:
        total += count_function(grid, 'XMAS')
    return total


def count_direction(d_y, d_x, grid, word):
    height, width = len(grid), len(grid[0])
    def is_in_bounds(y, x): return y in range(height) and x in range(width)

    def at(y, x):
        return grid[y][x]
    found = 0
    for row in range(height):
        for col in range(width):
            positions = [(row + (i * d_y), col + (i * d_x))
                         for i in range(len(word))]
            if not all(is_in_bounds(*position) for position in positions):
                continue
            actuals = [at(*position) for position in positions]
            if all(actual == expected for actual, expected in zip(actuals, word)):
                found += 1
    return found


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

import os
from collections import defaultdict
import functools
import itertools


def parse(path):
    with open(path, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
        height = len(grid)
        width = len(grid[0])
        antenna_map = defaultdict(list)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                ch = grid[row][col]
                if ch not in ['.', '#']:
                    antenna_map[ch].append((row, col))
        return (height, width, antenna_map)


def solve(height, width, antenna_map):
    def is_in_bounds(y, x): return y in range(height) and x in range(width)
    return len(
        functools.reduce(lambda accum, antenna_positions: accum |
                         solve_for_one_frequency(is_in_bounds, antenna_positions), antenna_map.values(), set())
    )


def solve_for_one_frequency(is_in_bounds, antenna_positions):
    antinode_positions = set()
    for a, b in itertools.combinations(antenna_positions, 2):
        y_a, x_a = a
        y_b, x_b = b

        d_y, d_x = y_b - y_a, x_b - x_a

        y_p, x_p = y_a - d_y, x_a - d_x
        y_q, x_q = y_b + d_y, x_b + d_x

        for antinode_position in [(y_p, x_p), (y_q, x_q)]:
            y, x = antinode_position
            if is_in_bounds(y, x):
                antinode_positions.add(antinode_position)

    return antinode_positions


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(*parse(input_path))
print(solution)

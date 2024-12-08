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
        for row in range(height):
            for col in range(width):
                ch = grid[row][col]
                if ch not in ['.', '#']:
                    antenna_map[ch].append((row, col))
        return (height, width, antenna_map)


def solve(height, width, antenna_map):
    antinode_positions = functools.reduce(
        lambda accum, antenna_positions: accum | solve_for_one_frequency(
            height, width, antenna_positions),
        antenna_map.values(),
        set()
    )
    return len(antinode_positions)


def solve_for_one_frequency(height, width, antenna_positions):
    def is_in_bounds(y, x): return y in range(height) and x in range(width)
    antinode_positions = set()
    for a, b in itertools.combinations(antenna_positions, 2):
        y_a, x_a = a
        y_b, x_b = b

        d_y, d_x = y_b - y_a, x_b - x_a

        i = 0
        while True:
            y_p, x_p = y_a - (i * d_y), x_a - (i * d_x)
            if not is_in_bounds(y_p, x_p):
                break
            antinode_positions.add((y_p, x_p))
            i += 1
        i = 0
        while True:
            y_q, x_q = y_b + (i * d_y), x_b + (i * d_x)
            if not is_in_bounds(y_q, x_q):
                break
            antinode_positions.add((y_q, x_q))
            i += 1

    return antinode_positions


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(*parse(input_path))
print(solution)

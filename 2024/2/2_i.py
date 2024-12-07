import os
import itertools


def parse(path):
    with open(path, 'r') as f:
        return [[int(number) for number in line.strip().split()] for line in f]


def solve(data):
    return sum(solve_one(line) for line in data)


def solve_one(xs):
    return (is_increasing(xs) or is_decreasing(xs)) and has_good_differences(xs)


def is_increasing(xs):
    return all((a > b) for a, b in itertools.pairwise(xs))


def is_decreasing(xs):
    return all(a < b for a, b in itertools.pairwise(xs))


def has_good_differences(xs):
    return all(abs(a - b) in range(1, 4) for a, b in itertools.pairwise(xs))


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

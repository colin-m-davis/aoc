import os
import functools


def parse(path):
    with open(path, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def solve(numbers):
    return sum(map(solve_one, numbers))


def solve_one(number):
    return functools.reduce(lambda acc, _: evolve(acc), range(2000), number)


def evolve(number):
    a = prune(mix(number * 64, number))
    b = prune(mix(a // 32, a))
    c = prune(mix(b * 2048, b))
    return c


def mix(x, y):
    return x ^ y


def prune(x):
    return x % 16777216


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

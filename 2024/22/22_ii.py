import os
from functools import reduce
from collections import defaultdict


def parse(path):
    with open(path, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def solve(numbers):
    m = reduce(merge, numbers, defaultdict(int))
    return max(m.values())


def merge(acc, number):
    for k, v in get_map(number).items():
        acc[k] += v
    return acc


def get_map(number):
    m = defaultdict(int)
    last_digit = number % 10
    past_differences = [last_digit]
    for _ in range(2000):
        new_number = evolve(number)
        new_last_digit = new_number % 10
        past_differences.append(new_last_digit - last_digit)
        if len(past_differences) > 4:
            recent_differences = tuple(past_differences[-4:])
            if recent_differences not in m:
                m[recent_differences] = new_last_digit
        number = new_number
        last_digit = new_last_digit
    return m


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

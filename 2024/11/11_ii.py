import os
import functools
import itertools
import collections


def parse(path):
    with open(path, 'r') as f:
        return [int(x) for x in f.readline().strip().split(' ')]


def transform(stone):
    if stone == 0:
        return [1]
    if len(stone_str := str(stone)) % 2 == 0:
        return [int(stone_str[:len(stone_str) // 2]), int(stone_str[len(stone_str) // 2:])]
    return [stone * 2024]


def transform_counter(counter):
    new_counter = collections.defaultdict(int)
    for number, quantity in counter.items():
        for new_number in transform(number):
            new_counter[new_number] += quantity
    return new_counter


def solve(stones, blinks=25):
    counter = collections.Counter(stones)
    for _ in range(blinks):
        counter = transform_counter(counter)
    return sum(counter.values())


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path), 75)
print(solution)

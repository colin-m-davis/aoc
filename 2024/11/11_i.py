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


def solve(stones, blinks=25):
    for _ in range(blinks):
        stones = list(itertools.chain.from_iterable(
            transform(stone) for stone in stones))
    return len(stones)


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path), 25)
print(solution)

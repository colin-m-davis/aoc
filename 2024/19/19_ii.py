import os
from typing import List
from functools import cache


def parse(path: str):
    with open(path, 'r') as f:
        patterns = f.readline().strip().split(', ')
        f.readline()
        designs = [line.strip() for line in f.readlines()]
        return (patterns, designs)


def solve(input: tuple[List[str], List[str]]) -> int:
    patterns, designs = input
    return sum(solve_one(patterns, design) for design in designs)


def solve_one(patterns: List[str], design: str) -> int:
    @cache
    def recurse(index: int):
        if index == len(design):
            return 1
        if index > len(design):
            return 0
        return sum(recurse(index + len(pattern)) for pattern in patterns if index + len(pattern) <= len(design) and pattern == design[index:index + len(pattern)])
    return recurse(0)


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

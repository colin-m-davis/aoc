import os
from typing import List


def parse(path: str):
    with open(path, 'r') as f:
        patterns = f.readline().strip().split(', ')
        f.readline()
        designs = [line.strip() for line in f.readlines()]
        return (patterns, designs)


def solve(input: tuple[List[str], List[str]]) -> int:
    patterns, designs = input
    return sum(1 for design in designs if solve_one(patterns, design))


def solve_one(patterns: List[str], design: str, index=0) -> bool:
    if index == len(design):
        return True
    for pattern in patterns:
        if index + len(pattern) <= len(design) and pattern == design[index:index + len(pattern)] and solve_one(patterns, design, index + len(pattern)):
            return True
    return False


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

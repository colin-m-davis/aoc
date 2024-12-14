import os
import re

regex = r"mul\((\d{1,3}),(\d{1,3})\)"


def parse(path: str) -> str:
    with open(path, 'r') as f:
        return ''.join(line.strip() for line in f)


def solve(s: str) -> int:
    return sum(int(x) * int(y) for x, y in re.findall(regex, s))


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

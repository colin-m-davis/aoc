import os
import re
import functools

regex = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))"


def parse(path: str) -> str:
    with open(path, 'r') as f:
        return ''.join(line.strip() for line in f)


def solve(s: str) -> int:
    matches = re.findall(regex, s)

    def accumulate(acc, match):
        are_instructions_enabled, running_total = acc
        if match[2]:
            return (True, running_total)
        elif match[3]:
            return (False, running_total)
        elif are_instructions_enabled:
            return (are_instructions_enabled, running_total + (int(match[0]) * int(match[1])))
        else:
            return acc
    return functools.reduce(accumulate, matches, (True, 0))[1]


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

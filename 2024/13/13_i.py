import os
from dataclasses import dataclass
import re
import math


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other: 'Point'):
        return self.x == other.x and self.y == other.y

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, a: int):
        return Point(a * self.x, a * self.y)


@dataclass
class ClawMachine:
    button_a: Point
    button_b: Point
    prize: Point


def parse(path: str):
    with open(path, 'r') as f:
        lines = f.readlines()
        chunks = [lines[i:i+3] for i in range(0, len(lines) - 2, 4)]

        def parse_chunk(chunk):
            points = (Point(*(int(x) for x in re.findall(r'\d+', line)))
                      for line in chunk)
            return ClawMachine(*points)
        return [parse_chunk(chunk) for chunk in chunks]


def solve(claw_machines: ClawMachine):
    return sum(solve_one(claw_machine) for claw_machine in claw_machines)


def solve_one(claw_machine: ClawMachine):
    def did_go_too_far(point: Point):
        return point.x > claw_machine.prize.x or point.y > claw_machine.prize.y
    best = float('inf')
    presses_a = 0
    while True:
        cur = presses_a * claw_machine.button_a
        if did_go_too_far(cur):
            break
        remaining = claw_machine.prize - cur
        if remaining.x % claw_machine.button_b.x == 0 and remaining.y % claw_machine.button_b.y == 0:
            presses_b = remaining.x // claw_machine.button_b.x
            if remaining - (presses_b * claw_machine.button_b) == Point(0, 0):
                cost = 3 * presses_a + presses_b
                best = min(best, cost)
        presses_a += 1
    return 0 if best == float('inf') else best


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

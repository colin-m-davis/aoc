import os
from dataclasses import dataclass
from functools import reduce
from operator import mul
from re import findall
from typing import List


HEIGHT = 103
WIDTH = 101
SECONDS = 100


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Robot:
    position: Point
    velocity: Point


def parse(path: str) -> List[Robot]:
    with open(path, 'r') as f:
        def parse_robot(line: str):
            numbers = [int(x) for x in findall(r'-?\d+', line)]
            position = Point(*numbers[:2])
            velocity = Point(*numbers[2:])
            return Robot(position, velocity)
        return [parse_robot(line) for line in f]


def solve(robots: List[Robot], width=WIDTH, height=HEIGHT, seconds=SECONDS) -> int:
    final_positions = [final_position(
        robot, width, height, seconds) for robot in robots]

    def accumulate(quadrant_counts: tuple[int, int, int, int], position: Point) -> tuple[int, int, int, int]:
        if position.x == width // 2 or position.y == height // 2:
            # Robot is not in any quadrant
            return quadrant_counts
        # Assign arbitrary indices to each quadrant, consistent across the program
        quadrant_index = (
            (0 if position.x < width // 2 else 2)
            + (0 if position.y < height // 2 else 1)
        )
        return (*quadrant_counts[:quadrant_index], quadrant_counts[quadrant_index] + 1, *quadrant_counts[quadrant_index + 1:])

    quadrant_counts = reduce(accumulate, final_positions, (0, 0, 0, 0))
    return reduce(mul, quadrant_counts)


def final_position(robot: Robot, width: int, height: int, seconds: int) -> Point:
    final_x = (((seconds * robot.velocity.x) + robot.position.x) %
               width + width) % width
    final_y = (((seconds * robot.velocity.y) + robot.position.y) %
               height + height) % height
    return Point(final_x, final_y)


input_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

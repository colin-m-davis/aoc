import os
from dataclasses import dataclass
from functools import reduce
from operator import mul
from re import findall
from time import sleep
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


def solve(robots: List[Robot], width=WIDTH, height=HEIGHT) -> None:
    i = 0
    while True:
        positions = [robot.position for robot in robots]
        if len(set((position.y, position.x) for position in positions)) == len(positions):
            print(i)
            print_grid(robots, width, height)
            print('\n\n')
            sleep(0.500)
        robots = [move_robot(robot, width, height) for robot in robots]
        i += 1


def move_robot(robot: Robot, width: int, height: int) -> Robot:
    new_x = ((robot.velocity.x + robot.position.x) %
             width + width) % width
    new_y = ((robot.velocity.y + robot.position.y) %
             height + height) % height
    return Robot(Point(new_x, new_y), robot.velocity)


def print_grid(robots: List[Robot], width, height) -> None:
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot.position.y][robot.position.x] = '#'
    for row in grid:
        print(' '.join(row))


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solve(parse(input_path), 101, 103)

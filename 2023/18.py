# AoC 2023, day 18

from functools import reduce
from itertools import pairwise

right = 0
down = 1
left = 2
up = 3
steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dm = {'R': right, 'D': down, 'L': left, 'U': up}

def move(y, x, d, n):
    movement = (n * steps[d][0], n * steps[d][1])
    return (y + movement[0], x + movement[1])

def parse1(line):
    s = line.strip().split()[:2]
    return (dm[s[0]], int(s[1]))

def parse2(line):
    s = line.strip().split()[2]
    return (int(s[-2]), int('0x' + s[2:-2], 16))

part_map = {1: parse1, 2: parse2}

def parse_instructions(part, path):
    return map(part_map[part], open(path).readlines())

def get_vertices(instructions):
    return reduce(lambda acc, ins: (p := acc[-1]) and (acc + [move(p[0], p[1], ins[0], ins[1])]), instructions, [(0, 0)])

def lines(vertices):
    return pairwise(vertices + [vertices[0]])

def shoelace(vertices):
    det = lambda v1, v2: v1[0] * v2[1] - v1[1] * v2[0]
    return abs(sum(map(lambda pair: det(pair[0], pair[1]), lines(vertices)))) // 2

def perimeter(vertices):
    dist = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return sum(map(lambda ps: dist(ps[0], ps[1]), lines(vertices)))

def picks_area(vertices):
    return shoelace(vertices) + perimeter(vertices) // 2 + 1

def solve(part, path):
    return picks_area(get_vertices(parse_instructions(part, path)))

parts = [1, 2]
print([str(part) + ": " + str(solve(part, 'input')) for part in parts])
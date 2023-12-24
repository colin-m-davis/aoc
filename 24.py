from itertools import product
import numpy as np

def parse(path):
    f = open(path)
    def parse_one(line):
        halves = line.split(' @ ')
        x, y, z = [int(a) for a in halves[0].split(', ')]
        dx, dy, dz = [int(a) for a in halves[1].split(', ')]
        return (np.array([x, y, 0]), np.array([dx, dy, 0]))
    return [parse_one(line.strip()) for line in f]    

def does_intersect(stone1, stone2):
    lo, hi = 200000000000000, 400000000000000
    point1, dir_vector1 = stone1
    point2, dir_vector2 = stone2
    if np.all(dir_vector1 == dir_vector2): return False
    A = np.array([dir_vector1, -dir_vector2]).T
    b = point2 - point1
    params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    if np.allclose(A @ params, b):
        t, s = params
        intersection = (point1 + t * dir_vector1)[:2]
        return min(t, s) >= 0 and all((intersection >= lo) & (intersection <= hi))
    else: return False

def solve1(stones):
    return sum(does_intersect(a, b) for a, b in product(stones, stones)) // 2

print(solve1(parse('input')))
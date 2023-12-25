from itertools import product
import numpy as np
from functools import cache
from z3 import Solver, Int
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parse(path):
    f = open(path)
    def parse_one(line):
        halves = line.split(' @ ')
        x, y, z = [int(a) for a in halves[0].split(', ')]
        dx, dy, dz = [int(a) for a in halves[1].split(', ')]
        return (np.array([x, y, z]) / 1e13, np.array([dx, dy, dz]) / 1e13)
    return [parse_one(line.strip()) for line in f]    

def does_intersect(stone1, stone2, i, j):
    lo, hi = 7, 27
    point1, dir_vector1 = stone1
    point2, dir_vector2 = stone2
    if np.all(dir_vector1 == dir_vector2) or np.all(dir_vector1 == -dir_vector2):
        print(f'{i} and {j} are parallel!')
        return False
    A = np.array([dir_vector1, -dir_vector2]).T
    b = point2 - point1
    params, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    if np.allclose(A @ params, b):
        t, s = params
        intersection = (point1 + t * dir_vector1)[:2]
        return min(t, s) >= 0 and all((intersection >= lo) & (intersection <= hi))
    else: return False

def solve1(stones):
    n = len(stones)
    total = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            total += does_intersect(stones[i], stones[j], i, j)
    return total

def at(t, x, d):
    return x + t * d

def solve2(stones):
    @cache
    def getV(name):
        now = Int(name)
        return now

    o = Solver()
    o.set("timeout", 3000)
    for i, row in enumerate(stones):
        (x, y, z), (dx, dy, dz) = row
        o.add(getV(f"t{i}") >= 0)
        o.add(x + dx * getV(f"t{i}") == getV("sx") + getV("dx") * getV(f"t{i}"))
        o.add(y + dy * getV(f"t{i}") == getV("sy") + getV("dy") * getV(f"t{i}"))
        o.add(z + dz * getV(f"t{i}") == getV("sz") + getV("dz") * getV(f"t{i}"))

    o.check()
    m = o.model()
    total = 0
    return sum(m[getV(d)].as_long() for d in ['sx', 'sy', 'sz'])

def vis(stones):
    x_i = np.array([stone[0][0] for stone in stones])
    y_i = np.array([stone[0][1] for stone in stones])
    z_i = np.array([stone[0][2] for stone in stones])
    dx_i = np.array([stone[1][0] for stone in stones])
    dy_i = np.array([stone[1][1] for stone in stones])
    dz_i = np.array([stone[1][2] for stone in stones])
    points = np.column_stack((x_i, y_i, z_i))
    directions = np.column_stack((dx_i, dy_i, dz_i))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Normalize line lengths for visualization
    line_length = 100  # Adjust as needed
    for point, direction in zip(points, directions):
        line = point + line_length * direction / np.linalg.norm(direction)
        ax.plot([point[0], line[0]], [point[1], line[1]], [point[2], line[2]])

    # Setting the axes properties to encompass all points
    max_range = np.array([points[:,0].max()-points[:,0].min(), 
                        points[:,1].max()-points[:,1].min(), 
                        points[:,2].max()-points[:,2].min()]).max() / 2.0

    mid_x = (points[:,0].max()+points[:,0].min()) * 0.5
    mid_y = (points[:,1].max()+points[:,1].min()) * 0.5
    mid_z = (points[:,2].max()+points[:,2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()

stones = parse('input')
vis(stones)
# solve1(stones)
from collections import defaultdict
from sys import setrecursionlimit

setrecursionlimit(100000)

def parse(path):
    f = open('input')
    g = [list(map(lambda x: x if x in [ground, forest] else ground, line.strip())) for line in f]
    return g

up, right, down, left = range(4)
movements = {up: (-1, 0), right: (0, 1), down: (1, 0), left: (0, -1)}
ground = '.'
forest = '#'
arrows = {'v': down, '>': right}
def move(y, x, d):
    dy, dx = movements[d]
    return (y + dy, x + dx)

def solve(g):
    inf = 100000000000
    m, n = len(g), len(g[0])
    start = (1, 1)
    end = (m - 2, n - 2)

    def adjacents(y, x):
        in_bounds = lambda y, x: y in range(m) and x in range(n)
        assert(in_bounds(y, x) and g[y][x] != forest)
        adjacent = [(d, move(y, x, d)) for d in range(4)]
        goods = [(d, p) for d, p in adjacent if in_bounds(p[0], p[1]) and g[p[0]][p[1]] != forest]
        return goods

    graph = defaultdict(set)
    for y in range(1, m - 1):
        for x in range(1, n - 1):
            if g[y][x] == forest: continue
            goods = adjacents(y, x)
            if len(goods) <= 2 and (y, x) != start and (y, x) != end: continue
            opposite = lambda dir: (dir + 2) % 4
            def extend(pdir, pos):
                dist = 0
                while True:
                    dist += 1
                    y, x = pos
                    goods = adjacents(y, x)
                    if len(goods) != 2 or (y, x) == start or (y, x) == end: break
                    pdir, pos = [(d, p) for d, p in goods if d != opposite(pdir)][0]
                return (pdir, pos, dist)
            data = [extend(d, p) for d, p in goods]
            for _, pos, dist in data: graph[(y, x)].add((pos, dist))

    def walk(y, x, seen):
        if (y, x) == end: return 0
        adjacents = graph[(y, x)]
        results = [-inf]
        for p2, d in adjacents:
            if p2 not in seen:
                y2, x2 = p2
                at = graph[(y2, x2)]
                if at != forest:
                    seen2 = set.union(seen, {p2})
                    results.append(d + walk(y2, x2, seen2))
        return max(results)
    
    print(graph[start])
    print(graph[end])

    length = walk(1, 1, {(0, 1), (1, 1)})
    return length + 2

print(solve(parse('input')))

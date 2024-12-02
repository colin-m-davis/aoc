from functools import reduce
from timeit import default_timer as timer

N = 1000000000
empty = '.'
round = 'O'
cube = '#'

def pipeline(fs, init):
    return reduce(lambda accum, f: f(accum), fs, init)

def repeat(f, n, init):
    return pipeline([f] * n, init)

def transpose(g):
    return list(map(list, zip(*g)))

def rotate_left(g):
    return transpose(g)[::-1]

def rotate_right(g):
    return pipeline([rotate_left] * 3, g)

def dims(g):
    return len(g), len(g[0])

def tilt(g):
    g_t = transpose(g)
    for index, col in enumerate(g_t):
        for r in range(len(col)):
            if col[r] != round: continue
            r_past = r - 1
            while r_past >= 0 and col[r_past] == empty: r_past -= 1
            r_past += 1
            col[r] = empty
            col[r_past] = round
        g_t[index] = col
    return transpose(g_t)

def tilt4(g):
    return reduce(
        lambda accum, m: repeat(rotate_left, m, tilt(repeat(rotate_right, m, accum))),
        range(4),
        g)

def load(g):
    n_rows, n_cols = dims(g)
    return reduce(
        lambda acc, r: acc + reduce(
            lambda acc, c: acc + (n_rows - r if g[r][c] == round else 0),
            range(n_cols),
            0),
        range(n_rows),
        0)

def solve(g):
    slow = tilt4(g)
    fast = tilt4(tilt4(g))
    while slow != fast:
        slow = tilt4(slow)
        fast = repeat(tilt4, 2, fast)
    before_cycle = 0
    slow = g
    while slow != fast:
        before_cycle += 1
        slow = tilt4(slow)
        fast = tilt4(fast)
    cycle_length = 1
    slow = tilt4(slow)
    while slow != fast:
        cycle_length += 1
        slow = tilt4(slow)
    remaining = N - before_cycle
    leftover = remaining % cycle_length
    final = repeat(tilt4, leftover, slow)
    return load(final)

f = open('input')
g = [[c for c in line.strip()] for line in f]
start = timer()
print(solve(g))
end = timer()
print("took", end - start, "seconds")
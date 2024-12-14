import os


def parse(path):
    with open(path, 'r') as f:
        return [[int(x) for x in row.strip()] for row in f.readlines()]


def recurse(grid, r, c):
    cur_value = grid[r][c]
    if cur_value == 9:
        return 1
    next_attempts = (recurse(grid, r + offset_r, c + offset_c) for offset_r, offset_c in [
                     (0, -1), (0, 1), (-1, 0), (1, 0)] if r + offset_r in range(len(grid)) and c + offset_c in range(len(grid[0])) and grid[r + offset_r][c + offset_c] == cur_value + 1)
    return sum(next_attempts)


def get_score(grid, r, c):
    if grid[r][c] != 0:
        return 0
    return recurse(grid, r, c)


def solve(grid):
    return sum(get_score(grid, y, x) for x in range(len(grid[0])) for y in range(len(grid[1])))


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(parse(input_path))
print(solution)

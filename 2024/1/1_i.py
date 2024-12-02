def parse(path):
    with open(path, 'r') as f:
        return tuple(list(tup) for tup in zip(*((int(word) for word in line.strip().split()) for line in f)))

def solve(xs, ys):
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))

solution = solve(*parse('2024/1/input'))
print(solution)

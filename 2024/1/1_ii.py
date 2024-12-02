from collections import Counter

def parse(path):
    with open(path, 'r') as f:
        return tuple(list(tup) for tup in zip(*((int(word) for word in line.strip().split()) for line in f)))

def solve(xs, ys):
    ys_counter = Counter(ys)
    return sum(x * ys_counter[x] for x in xs)

solution = solve(*parse('2024/1/input'))
print(solution)

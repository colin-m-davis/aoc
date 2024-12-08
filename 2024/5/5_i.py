import os
from collections import defaultdict, deque


def parse(path):
    with open(path, 'r') as f:
        ordering_rules = []
        while len(line := f.readline()) > 1:
            a, b = [int(word) for word in line.strip().split('|')]
            ordering_rules.append((a, b))
        updates = [[int(word) for word in line.strip().split(',')]
                   for line in f.readlines()]
        return (ordering_rules, updates)


def solve(ordering_rules, updates):
    graph = construct_graph(ordering_rules)
    return sum(middle_value(update) if is_good(update, graph) else 0 for update in updates)


def construct_graph(ordering_rules):
    graph = defaultdict(set)
    for a, b in ordering_rules:
        graph[a].add(b)
    return graph


def is_good(update, graph):
    seen = set()
    for page in update:
        if set.intersection(seen, graph[page]):
            return False
        seen.add(page)
    return True


def middle_value(update):
    return update[len(update) // 2]


input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
solution = solve(*parse(input_path))
print(solution)

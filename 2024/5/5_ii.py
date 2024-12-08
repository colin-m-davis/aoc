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
    return sum(middle_value(order_correctly(update, graph)) if not is_good(update, graph) else 0 for update in updates)


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


def topologically_sort(graph):
    indegrees = defaultdict(int)
    for parent, children in graph.items():
        indegrees[parent] += 0
        for child in children:
            indegrees[child] += 1
    queue = deque(
        [node for node, indegree in indegrees.items() if indegree == 0])
    reverse_order = []
    while len(queue) > 0:
        current_node = queue.popleft()
        reverse_order.append(current_node)
        for child in graph[current_node]:
            indegrees[child] -= 1
            if indegrees[child] == 0:
                queue.append(child)
    return reverse_order[::-1]


def order_correctly(update, graph):
    graph_slice = {parent: [child for child in children if child in update]
                   for parent, children in graph.items() if parent in update}
    return topologically_sort(graph_slice)


def middle_value(update):
    return update[len(update) // 2]


input_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'input')
solution = solve(*parse(input_path))
print(solution)

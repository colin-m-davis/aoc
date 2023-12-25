from timeit import default_timer as timer
import networkx as nx
from functools import reduce

def parse(path):
    f = open(path)
    G = nx.Graph()
    for line in f:
        line = line.strip()
        node, adjs = line.split(': ')
        adjs = adjs.split(' ')
        G.add_node(node)
        G.add_nodes_from(adjs)
        for adj in adjs:
            G.add_edge(node, adj)
            G.add_edge(adj, node)
    return G

def solve(G):
    cut_set = nx.minimum_edge_cut(G)
    assert(len(cut_set) == 3)
    G_p = nx.Graph(G)
    G_p.remove_edges_from(cut_set)
    components = list(nx.connected_components(G_p))
    assert(len(components) == 2)
    sizes = (len(c) for c in components)
    product = lambda xs: reduce(lambda acc, x: acc * x, xs, 1)
    return product(sizes)

start = timer()
result = solve(parse('input'))
end = timer()

print(f'result: {result}')
print(f'took: {(end - start) * 1000} ms')

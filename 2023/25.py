import networkx as nx
from functools import reduce
from timeit import default_timer

def parse(path):
    f = open(path)
    G = nx.Graph()
    for line in f:
        line = line.strip()
        node, adjs = line.split(': ')
        adjs = adjs.split(' ')
        G.add_node(node)
        G.add_nodes_from(adjs)
        G.add_edges_from((node, adj) for adj in adjs)
        G.add_edges_from((adj, node) for adj in adjs)
    return G

def solve(G):
    cutset = nx.minimum_edge_cut(G)
    assert(len(cutset) == 3)
    G_p = nx.Graph(G)
    G_p.remove_edges_from(cutset)
    components = list(nx.connected_components(G_p))
    assert(len(components) == 2)
    sizes = [len(c) for c in components]
    product = lambda xs: reduce(lambda acc, x: acc * x, xs, 1)
    return product(sizes)

path = 'input'
start = default_timer()
result = solve(parse(path))
end = default_timer()
elapsed_ms = (end - start) * 1000

print(f'result: {result}')
print(f'took: {elapsed_ms} ms')

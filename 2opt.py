import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import random

problem = tsplib95.load_problem('bays29.tsp')
G = problem.get_graph()

n = len(G.nodes)

s = 1
v = s
nodes = [v]
path = []
cost = 0

for i in range(n - 1):
    candidates = []
    for to in range(1, n + 1):
        if to not in nodes:
            candidates.append((G.edges[v, to]['weight'], to))
    candidates.sort()
    next_node = candidates[0][1]
    cost += candidates[0][0]
    nodes.append(next_node)
    path.append((v, next_node))
    v = next_node
path.append((v, s))
cost += G.edges[v, s]['weight']

plt.figure()
_, ax = plt.subplots()
pos = problem.display_data or problem.node_coords
nx.draw_networkx_nodes(G, pos=pos, ax=ax)
nx.draw_networkx_labels(G, pos=pos, labels={i: str(i) for i in range(1, len(G.nodes) + 1)}, font_size=8, font_color='white')
nx.draw_networkx_edges(G, pos=pos, edgelist=path, arrows=True)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()

# 2-swap
for _ in range(10000):
    while True:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if i != j:
            break
    if i > j:
        i, j = j, i

    distA = G.edges[nodes[i], nodes[i + 1]]['weight']
    distB = G.edges[nodes[j], nodes[(j + 1) % n]]['weight']
    distC = G.edges[nodes[i], nodes[j]]['weight']
    distD = G.edges[nodes[i + 1], nodes[(j + 1) % n]]['weight']

    if distA + distB > distC + distD:
        print(cost, i, j, nodes[i], nodes[j])
        nodes[i + 1:j + 1] = reversed(nodes[i + 1: j + 1])
        cost += (distC + distD - distA - distB)
        path = []
        for i in range(n):
            path.append((nodes[i], nodes[(i + 1) % n]))
        plt.figure()
        _, ax = plt.subplots()
        pos = problem.display_data or problem.node_coords
        nx.draw_networkx_nodes(G, pos=pos, ax=ax)
        nx.draw_networkx_labels(G, pos=pos, labels={i: str(i) for i in range(1, len(G.nodes) + 1)}, font_size=8, font_color='white')
        nx.draw_networkx_edges(G, pos=pos, edgelist=path, arrows=True)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.show()

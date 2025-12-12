import random
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import networkx as nx

n = int(input("количество вершин: "))
h = float(input("связность от 0 до 1, 0 - не связный, 1 - сильносвязный: "))
graph_ver = [i for i in range(1, n + 1)]

#генерация рандомного графа с n вершинами
def generate_random_graph(n_ver, edge_probability):
    graph = {i: [] for i in range(1, n_ver + 1)}
    for i in range(1, n_ver + 1):
        for j in range(i + 1, n_ver + 1):
            if random.random() < edge_probability:
                graph[i].append(j)
                graph[j].append(i)
    return graph
graph_neighbors = generate_random_graph(n,h)

# поиск максимального независимого множества точным алгоритмом
def find_max_set_a1_py(graph,neighbors,cur_set):
    if len(graph) == 0:
        return cur_set
    var = graph[0]
    # включить вершину var
    new_graph = graph.copy()
    new_graph = [item for item in new_graph if item != var and item not in neighbors[var]]
    result1 = find_max_set_a1_py(new_graph,neighbors, cur_set + [var])
    #не включать вершину var
    new_graph = graph.copy()
    new_graph.remove(var)
    result2 = find_max_set_a1_py(new_graph,neighbors,cur_set)
    return max([result1, result2], key=len)

# поиск максимально независимого множество жадным алгоритмомом
def find_max_set_a2_py(neighbors):
    neighbors_copy = neighbors.copy()
    max_set = []
    while neighbors_copy:
        var = min(neighbors_copy.keys(), key=lambda x: len(neighbors_copy[x]))
        neighbors_list = neighbors_copy[var].copy()
        max_set.append(var)
        for i in neighbors_list:
            if i in neighbors_copy:
                neighbors_copy.pop(i, None)
        neighbors_copy.pop(var,None)
    return max_set

result_a1 = find_max_set_a1_py(graph_ver, graph_neighbors,[])
result_a2 = find_max_set_a2_py(graph_neighbors)

#визуализация
def visual(graph_dict, set1, set2):
    g = nx.Graph()
    for i, j in graph_dict.items():
        g.add_node(i)
        for k in j:
            g.add_edge(i, k)
    node_colors = []
    for node in g.nodes():
        if (node in set1) and (node in set2):
            node_colors.append("purple")
        elif node in set1:
            node_colors.append("red")
        elif node in set2:
            node_colors.append("blue")
        else:
            node_colors.append("gray")
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color=node_colors,node_size=500)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)
    plt.legend(handles=[
        Patch(facecolor='purple', label='В обоих алгоритмах'),
        Patch(facecolor='red', label='точный рекурсивный алгоритм'),
        Patch(facecolor='blue', label='жадный алгоритм'),
        Patch(facecolor='lightgray', label='нигде')
    ], loc='best')
    plt.title("граф", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

print(graph_neighbors)
print(result_a1)
print(result_a2)
visual(graph_neighbors,result_a1,result_a2)

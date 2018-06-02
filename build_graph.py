import json
import os

from metalearn.metafeatures.metafeatures import Metafeatures
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(str(node))

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()



with open("metalearn/metafeatures/metafeatures.json", "r") as fh:
	complete_dict = json.load(fh)

top = complete_dict.keys()
graph_dict = {}

for item in complete_dict.values():
	for node in item.keys():
		graph_dict[node] = {"forward":set(), "backward":set()}

for node, dependencies_dict in complete_dict["resources"].items():
	if dependencies_dict["function"] != "":
		graph_dict[node]["backward"].add(dependencies_dict["function"])
		graph_dict[dependencies_dict["function"]]["forward"].add(node)

for node, dependencies_dict in complete_dict["functions"].items():
	for param in dependencies_dict["parameters"]:
		graph_dict[node]["backward"].add(param)
		graph_dict[param]["forward"].add(node)
	for value in dependencies_dict["returns"]:
		graph_dict[node]["forward"].add(value)
		graph_dict[value]["backward"].add(node)

for node, dependencies_dict in complete_dict["metafeatures"].items():
	if dependencies_dict["function"] != "":
		graph_dict[node]["backward"].add(dependencies_dict["function"])
		graph_dict[dependencies_dict["function"]]["forward"].add(node)
	if "parameters" in dependencies_dict.keys():
		for param in dependencies_dict["parameters"]:
			if type(param) is not int:
				graph_dict[dependencies_dict["function"]]["backward"].add(param)
				graph_dict[param]["forward"].add(dependencies_dict["function"])
		for value in dependencies_dict["returns"]:
			graph_dict[dependencies_dict["function"]]["forward"].add(value)
			graph_dict[value]["backward"].add(dependencies_dict["function"])

# for item, value in graph_dict.items():
# 	print(item)
# 	print(value)
# 	print("")

mf_list = Metafeatures().list_metafeatures()
graph = []
for node in graph_dict.keys():
	forward = graph_dict[node]["forward"]
	backward = graph_dict[node]["backward"]
	if len(forward) > 0:
		for item in forward:
			graph.append((node, item))
	if len(backward) > 0:
		for item in backward:
			graph.append((node, item))

print(graph)
# draw example
draw_graph(graph)

# lvl1_set = [dependency for dependency in [dependencies for dependencies in [graph_dict[mf]["backward"] for mf in mf_list]]]
# lvl1_list = []
# for group in lvl1_set:
# 	lvl1_list.append(group)
# print(lvl1_list)
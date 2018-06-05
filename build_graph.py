import json
import os

from metalearn.metafeatures.metafeatures import Metafeatures
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'
):
    # create networkx graph
    G=graph

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    elif graph_layout == "kamada" :
        graph_pos=nx.kamada_kawai_layout(G)
    else:
    	graph_pos=nx.circular_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    # Show graph
    plt.show()

def make_graph(graph_dict):
	G=nx.DiGraph()
	for node in graph_dict.keys():
		child = graph_dict[node]["child"]
		parent = graph_dict[node]["parent"]
		if len(child) > 0:
			for item in child:
				G.add_edge(node, item)
		if len(parent) > 0:
			for item in parent:
				G.add_edge(item, node)
	return G

def make_simplified_graph_dict(original, subset):
	lvl1_dict = {}

	for node, children in subset.items():
		temp_set = set()
		for member in node:
			temp_set.update(original[member])
		if len(temp_set) == 0:
			lvl1_dict[node] = children
		else:
			if tuple(temp_set) not in lvl1_dict:
				lvl1_dict[tuple(temp_set)] = set()
			lvl1_dict[tuple(temp_set)].update(node)
	
	return lvl1_dict

def reverse(graph):
	reverse_graph = {}
	for node in graph:
		reverse_graph[node] = set()
	for node, children in graph.items():
		for child in children:
			reverse_graph[child].add(node)
	return reverse_graph

def make_graph_dict(complete_dict):
	graph_dict = {}

	for item in complete_dict.values():
		for node in item.keys():
			graph_dict[node] = set()

	for node, dependencies_dict in complete_dict["resources"].items():
		if dependencies_dict["function"] != "":
			graph_dict[dependencies_dict["function"]].add(node)

	for node, dependencies_dict in complete_dict["functions"].items():
		for param in dependencies_dict["parameters"]:
			graph_dict[param].add(node)
		for value in dependencies_dict["returns"]:
			graph_dict[node].add(value)

	for node, dependencies_dict in complete_dict["metafeatures"].items():
		if dependencies_dict["function"] != "":
			graph_dict[dependencies_dict["function"]].add(node)
		if "parameters" in dependencies_dict.keys():
			for param in dependencies_dict["parameters"]:
				if type(param) is not int:
					graph_dict[param].add(dependencies_dict["function"])
			for value in dependencies_dict["returns"]:
				graph_dict[dependencies_dict["function"]].add(value)

	return graph_dict


with open("metalearn/metafeatures/metafeatures.json", "r") as fh:
	complete_dict = json.load(fh)

graph_dict = make_graph_dict(complete_dict)
reverse_graph_dict = reverse(graph_dict)

mf_list = Metafeatures().list_metafeatures()

lvl0_dict = {tuple([k]): (v if len(v) > 0 else set()) for k,v in graph_dict.items() if k in mf_list}
lvl1_dict = make_simplified_graph_dict(reverse_graph_dict, lvl0_dict)
# lvl1_dict = make_simplified_graph_dict(reverse_graph_dict, lvl1_dict)

# for k,v in lvl1_dict.items():
# 	print(k)
# 	print(v)
# 	print()
# print(len(lvl1_dict))

for i,k in enumerate(lvl1_dict.items()):
	print(i)
	print(k[0])
	print(k[1])
	print()

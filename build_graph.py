import json
import os

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
		graph_dict[node]["backward"].add(value)
		graph_dict[value]["forward"].add(node)

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
			graph_dict[dependencies_dict["function"]]["backward"].add(value)
			graph_dict[value]["forward"].add(dependencies_dict["function"])

for item, value in graph_dict.items():
	print(item)
	print(value)
	print("")

# node_dict = {node:[] for node in complete_dict.values()}


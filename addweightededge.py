#
# Add weighted edges by also increasing the weight at each edge
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite: 
# install NetworkX with pip install networkx
#

def addweightededge(graph, node1, node2):
    if graph.has_edge(node1,node2) and "weight" in graph[node1][node2]:
        graph[node1][node2]['weight'] += 1
    else:
        graph.add_edge(node1, node2, weight=1)
    return


if __name__ == "__main__":
    pass
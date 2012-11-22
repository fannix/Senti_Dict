"""
convert an edge list to the graph VNA format.
"""

import sys

def edge_list_to_vna(edge_list):
    """edge_list is a list of 3-tuples: [from, to, weight]
    """
    node_set = set()

    for from_node, to_node, weight in edge_list:
        node_set.add(from_node)
        node_set.add(to_node)

    return node_set, edge_list

def output_vna(vna_node, vna_edge):
    """Output the node and edge to the appropriate vna format
    """
    print "*node data"
    print "ID"

    for node in vna_node_set:
        print node

    print "*tie data\nfrom to strength"

    for from_node, to_node, weight in edge_list:
        print from_node, to_node, weight


if __name__ == "__main__":

    edge_list = []

    for line in sys.stdin:
        li = line.strip().split()

        from_node = li[0]
        to_node = li[1]
        weight = li[2]

        edge_list.append((from_node, to_node, weight))

    vna_node_set, vna_edge = edge_list_to_vna(edge_list)

    output_vna(vna_node_set, vna_edge)

import sys
sys.path.append('..')
sys.path.append('../..')
import os
from utils import *
from student_utils_sp18 import *
from networkx.algorithms.traversal import *
from networkx.algorithms.approximation import *


# Util functions

#utils
# calculate the heuristic for all nodes on the graph
def conquer_gain(G, node):
    """Given a Graph and a node it calculates the value of the heuristic for the node"""
    """conquering_cost_neighbors/conquering_cost_current_node larger is better"""
    
    if G.node[node]['color'] =="black": # do not calculate the heuristic for black nodes
        return 0
    else:
        neighbors = nx.neighbors(G, node)
        
        neighbors_conquering_cost = 0
        for n in neighbors:
            neighbors_conquering_cost += G.node[n]['conquering_cost']
        
        return neighbors_conquering_cost/G.node[node]['conquering_cost']
    
# update the colors in the graph

def update_graph(G, node):
    G.node[node]['color'] = "black"
    neighbors = nx.neighbors(G, node)
    
    for n in neighbors:
        if G.node[n]['color'] == "white":
            G.node[n]['color'] = "grey"
    return

# find the the nodes that we need to visit based on heuristic

def choose_node(G):
    # calculate heuristic for everyone
    heuristic_value = []

    for node in G.nodes():
        heuristic_value.append(conquer_gain(G, node))

    chosen_node = np.argmax(heuristic_value)
    return chosen_node

def all_conquered(G):
    lst = [l[1] for l in nx.get_node_attributes(G, "color").items()]
    
    return not "white" in lst

# recover the order of traversal of the tree

def find_traversal(tree, start_index):
    """Recovers the traversal of the Steiner tree using DFS (the full walk tho)"""
    
    vertex_order = list(dfs_preorder_nodes(tree, start_index))+[start_index]
    current_node = start_index
    full_walk = [start_index]

    for next_node in vertex_order[1:]:
        path = list(nx.all_simple_paths(tree, current_node, next_node))[0]
        full_walk.extend(path[1:])
        current_node = next_node
    return full_walk


def vasilis_solver(G, start_index):
    # find nodes to visit
    
    nodes_to_visit = []

    while not all_conquered(G):
        next_node = choose_node(G)
        nodes_to_visit.append(next_node)
        update_graph(G, next_node)

    
    # Handle the edge case from below
    if nodes_to_visit[0]==start_index and len(nodes_to_visit)==1:
        print("pipes")
        return [start_index], [start_index]
    
    # get Steiner tree
    # CURRENTLY HAS THE BUG THAT THE STEINER TREE DOES NOT WORK WHEN YOU ONLY HAVE 1 TARGET VERTEX
    ST = steinertree.steiner_tree(G, set(nodes_to_visit+[start_index]))
    
    
    # Find the traversal based on the Steiner tree
    traversal = find_traversal(ST, start_index)
    conquered = dict(zip(nodes_to_visit, [False]*len(nodes_to_visit)))
    to_conquer = []

    for n in traversal:
        if n in nodes_to_visit and conquered[n] == False:
            to_conquer.append(n)
            conquered[n]=True
            
    return traversal, to_conquer
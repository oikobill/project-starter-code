import sys
sys.path.append('..')
sys.path.append('../..')
import os
from utils import *
from student_utils_sp18 import *
from networkx.algorithms.traversal import *
from networkx.algorithms.approximation import *
from output_validator import *
from vasilis_solver import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import re



# find an MST. If it is a leaf, add the weight of its edge to it

def is_leaf(G, v):
    return len(list(nx.neighbors(G, v)))==1

def new_method(G, start_index):
    
    T = nx.minimum_spanning_tree(G)
    
    for v in T.nodes():
        if is_leaf(T, v):
            parent = list(nx.neighbors(T, v))[0]
            edge_weight = T.get_edge_data(v, parent)['weight']
            G.node[v]['conquering_cost'] += edge_weight
    
    nodes_to_visit = list(min_weighted_dominating_set(T, weight='conquering_cost'))
    
    if nodes_to_visit[0]==start_index and len(nodes_to_visit)==1:
        print("pipes")
        return [start_index], [start_index]
    
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
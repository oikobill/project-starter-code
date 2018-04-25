import sys
sys.path.append('..')
sys.path.append('../..')
import os
from utils import *
from networkx.algorithms import *
from student_utils_sp18 import *
from networkx.algorithms.traversal import *
from networkx.algorithms.approximation import *
from vasilis_solver import *
from tqdm import tqdm
import matplotlib.pyplot as plt
from anneal import *


def vasilis_greedy_anneal_solver(G, start_index):
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


    ###### OLD CODE TO USE AS A STARTING POINT ######

    ST = steinertree.steiner_tree(G, set(nodes_to_visit+[start_index]))
    
    
    # Find the traversal based on the Steiner tree
    traversal = find_traversal(ST, start_index)
    conquered = dict(zip(nodes_to_visit, [False]*len(nodes_to_visit)))
    to_conquer = []

    for n in traversal:
        if n in nodes_to_visit and conquered[n] == False:
            to_conquer.append(n)
            conquered[n]=True

    ###### OLD CODE TO USE AS A INITIALIZATION FOR ANNEALING ######
    
    bcandidate, bcost = anneal(G, to_conquer, start_index)
    
    # generate the correct traversal based on simulated annealing
    shortest_traversal = nx.shortest_path(G, start_index, bcandidate[1])
    
    for v in bcandidate[2:]:
        shortest_traversal.extend(nx.shortest_path(G, shortest_traversal[-1], v)[1:])
        
    c = []
    
    for n in shortest_traversal:
        if n in nodes_to_visit and not n in c:
            c.append(n)

    # old_t, old_c = vasilis_solver(G.copy(), start_index)

    # old_sln = cost_of_solution(G, old_t, old_c)
    new_sln = cost_of_solution(G, shortest_traversal, c)

    #print(new_sln[1])
    
    return shortest_traversal, c



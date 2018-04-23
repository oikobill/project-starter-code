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


def simple(G, start_index):
    # find an MST. Move all the 
    # find best to conquer on tree
    nodes_to_visit = list(min_weighted_dominating_set(G, weight=None))
    
    ST = steinertree.steiner_tree(G, set(list(nodes_to_visit)+[start_index]))
    
    if nodes_to_visit[0]==start_index and len(nodes_to_visit)==1:
        print("pipes")
        return [start_index], [start_index]
    
    # get Steiner tree
    # CURRENTLY HAS THE BUG THAT THE STEINER TREE DOES NOT WORK WHEN YOU ONLY HAVE 1 TARGET VERTEX
    ST = steinertree.steiner_tree(G, set(list(nodes_to_visit+[start_index])))
    
    
    # Find the traversal based on the Steiner tree
    traversal = find_traversal(ST, start_index)
    conquered = dict(zip(nodes_to_visit, [False]*len(nodes_to_visit)))
    to_conquer = []

    for n in traversal:
        if n in nodes_to_visit and conquered[n] == False:
            to_conquer.append(n)
            conquered[n]=True
            
    return traversal, to_conquer

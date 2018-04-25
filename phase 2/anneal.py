# Given a set of nodes to conquer, use simulated annealing to find the best way to traverse them
import sys
sys.path.append('..')
sys.path.append('../..')
import os
from utils import *
from networkx.algorithms import *
from student_utils_sp18 import *
from networkx.algorithms.traversal import *
from networkx.algorithms.approximation import *


def make_candidate(current, start_index):
    """Assume current is a list of nodes in order of visit."""
    candidate = current.copy()
    
    while start_index in candidate:
        candidate.remove(start_index)
    
    a = random.randint(0, len(candidate))
    b = random.randint(0, len(candidate))
    
    start = min(a, b)
    end = max(a, b)
    candidate[start:end] = reversed(candidate[start:end])
    
    candidate = [start_index] + candidate +[start_index]
    return candidate

def evaluate_candidate(candidate, G):
    """Returns the cost of the tour"""
    dist = 0
    for ix in range(len(candidate)-1):
        # find shortest distance between the two
        dist += shortest_path_length(G, candidate[ix], candidate[ix+1], "weight")
    return dist

def accept_probability(current, candidate, G, T):
    """If proposed solution is better, accept immediately, else accept with some probability,
        depending on temperature."""
    current_cost = evaluate_candidate(current, G)
    candidate_cost = evaluate_candidate(candidate, G)
    
    if candidate_cost<current_cost:
        return 1
    else:
        return np.e**(-abs(candidate_cost - current_cost) / T)

def anneal(G, curr_state, start_index):
    
    current_state = curr_state.copy()
    while start_index in current_state:
        current_state.remove(start_index)
        
    current_state = [start_index] + current_state + [start_index]
    
    T = np.sqrt(len(curr_state))
    alpha = 0.995
    stopping_temperature = 0.00001
    max_iters = 5000
    num_iters = 1
    
    
   
    
    best_candidate = current_state.copy()
    best_cost = [evaluate_candidate(current_state, G)]
    current_candidate = current_state.copy()
    
    num_transitions = 0
    iter_found = 0
    
    while T >= stopping_temperature and num_iters < max_iters:
        
        candidate = make_candidate(current_candidate, start_index)
        
        p  = accept_probability(current_candidate, candidate, G, T)
        
        
        if np.random.uniform()<p:
            num_transitions += 1
            current_candidate = candidate.copy()
            
        cost_current = evaluate_candidate(current_candidate, G)
        
        if cost_current < best_cost[-1]:
            best_candidate = current_candidate.copy()
            best_cost.append(cost_current)
            iter_found = num_iters
        
        T *= alpha
        num_iters += 1

    #print("Optimal Solution found at iter: {}".format(iter_found))

    
    return best_candidate, best_cost
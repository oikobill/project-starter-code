import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils_sp18 import *

"""
======================================================================
  Complete the following function.
======================================================================
"""
def get_neighbors(adjacency_matrix, node_index):
  """Func to return indices of the neighbors.. parameters are adjacency matrix and node index."""
  row_dictionary = adjacency_matrix[node_index]
  neighbor_indices = []
  for i in range(len(row_dictionary) - 1):
    if (row_dictionary[i] > 0) & (i!=node_index): #check i != node_index because there will be a nonzero element representing the conquering cost.
      neighbor_indices = neighbor_indices + [i]
  return neighbor_indices

def get_travel_cost(adjacency_matrix, path_indices):
  """Get the cost to take a given path, ignore the conquer costs... just count the edge costs."""
  total_cost = 0
  #pairwise iteration through path
  for i in range(len(path_indices) - 1):
    pair_cost = adjacency_matrix[i][i+1]
    total_cost = total_cost + pair_cost
  return total_cost

import numpy as np
def get_shortest_path(G, source, dest):
  source = str(source)
  dest = str(dest)
  nodes = np.arange(0, len(G))
  nodes = ''.join([str(x) for x in nodes])
  p=[[source]]
  flag=0

  while p:                          # evaluates to true if p not empty
      x = p.pop(0)
      j = nodes.index(x[-1])        # use [-1] to get last element
      if nodes[j] == dest:             # by moving this check out of the loop...
          break                     # ...you can use break and don't need flag
      for i, e in enumerate(nodes): # enumerate gives (index, element)
          if graph[j][i] and e not in x: # a bit more concise
              p.append(x + [e])
  return [int(elem) for elem in x]

graph=  [#a,b,c,d,e,f,g,h,i,j
     [0,1,1,1,1,0,0,0,0,0],  #a
     [1,0,0,1,0,0,1,0,0,0],  #b
     [1,0,0,1,0,0,0,0,0,0],  #c
     [1,1,1,0,0,0,0,1,0,0],  #d
     [1,0,0,0,0,1,0,1,1,0],  #e
     [0,0,0,0,1,0,0,1,1,0],  #f
     [0,1,0,0,0,0,0,1,1,1],  #g
     [0,0,0,1,1,1,1,0,1,0],  #h
     [0,0,0,0,1,1,1,1,0,1],  #i
     [0,0,0,0,0,0,1,0,1,0],  #j
    ]


def solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_kingdom_names: An list of kingdom names such that node i of the graph corresponds to name index i in the list
        starting_kingdom: The name of the starting kingdom for the walk
        adjacency_matrix: The adjacency matrix from the input file

    Output:
        Return 2 things. The first is a list of kingdoms representing the walk, and the second is the set of kingdoms that are conquered
    """
    index_to_name_map = {i: x for i, x in enumerate(list_of_kingdom_names)}
    name_to_index_map = {x: i for i, x in enumerate(list_of_kingdom_names)}
    conquered_nodes = np.array([])  # names
    surrendered_nodes = set()  # names
    closed_walk = np.array([name_to_index_map[starting_kingdom]])  # initially filled with index values
    current_node = starting_kingdom

    # Keep iterating until we conquer and surrender everything.
    while (len(conquered_nodes) + len(surrendered_nodes)) < len(list_of_kingdom_names):

        not_conquered_names = np.setdiff1d(list_of_kingdom_names, conquered_nodes)
        # print(not_conquered_names)
        heuristic_values = {}

        # Calculate heuristic values for unconquered nodes
        for node in not_conquered_names:
            node_neighbor_indicies = get_neighbors(adjacency_matrix, name_to_index_map[node])  # DONE
            unvisited_node_neighbors = np.intersect1d(np.setdiff1d(node_neighbor_indicies, conquered_nodes),
                                                      np.setdiff1d(node_neighbor_indicies,
                                                                   conquered_nodes))  # Calculates neighbors that have not been surrendered/conquered
            conquering_neighbors_gain = sum([adjacency_matrix[i][i] for i in unvisited_node_neighbors])
            shortest_path = get_shortest_path(adjacency_matrix, str(name_to_index_map[current_node]), str(
                name_to_index_map[node]))  # TODO SUE shortest path.. dont worry about conquer costs.
            travel_cost = get_travel_cost(adjacency_matrix, shortest_path)  # DONE
            conquer_cost = adjacency_matrix[name_to_index_map[node]][name_to_index_map[node]]
            node_heuristic = conquering_neighbors_gain / (travel_cost + conquer_cost)
            heuristic_values[node] = node_heuristic

        # Based on heurstics, find conquer the node with largest gain
        node_to_conquer = max(heuristic_values, key=heuristic_values.get)  # name of node to conquer
        surrendered_nodes.update(get_neighbors(adjacency_matrix, name_to_index_map[node_to_conquer]))
        conquered_nodes = np.append(conquered_nodes, node_to_conquer)
        shortest_path = get_shortest_path(adjacency_matrix, name_to_index_map[current_node],
                                          name_to_index_map[node_to_conquer])
        closed_walk = np.append(closed_walk, shortest_path[
                                             1:])  # add the nodes along the path to the walk. careful to not repeat vertices
        current_node = node_to_conquer

    # Once all nodes conquered or surrendered, take the shortest path back
    shortest_path_back = get_shortest_path(adjacency_matrix, name_to_index_map[current_node],
                                           name_to_index_map[starting_kingdom])
    closed_walk = np.append(closed_walk, shortest_path_back[1:])
    closed_walk = np.array([index_to_name_map[i] for i in closed_walk])  # convert walk into names
    print(closed_walk)
    return list(closed_walk), conquered_nodes


"""
======================================================================
   No need to change any code below this line
======================================================================
"""


def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)
    
    input_data = utils.read_file(input_file)
    number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)
    closed_walk, conquered_kingdoms = solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    output_filename = utils.input_to_output(filename)
    output_file = f'{output_directory}/{output_filename}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    utils.write_data_to_file(output_file, closed_walk, ' ')
    utils.write_to_file(output_file, '\n', append=True)
    utils.write_data_to_file(output_file, conquered_kingdoms, ' ', append=True)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)

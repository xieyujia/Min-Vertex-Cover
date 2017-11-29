#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 author: syuizen (Yiran)

 Algorithm description:
 greedy algorithm described in class, please refer to the slide approx3

 Modification:
 vertices are sorted in the decreasing order of degree
"""
import os
from utils import *
#import networkx as nx
#derive a vertex cover by greedy algorithm
def approx_vc(G): #G is  nx.graph
    #G = OG.copy()
    degree_list = G.degree()
    VC = list() #vertex cover set
    max_node = max(degree_list , key = degree_list.get)
    #max_degree = degree_list[max_node]
    while degree_list[max_node] > 0:
        degree_list[max_node] = 0
        VC.append(max_node)
        #G.remove_node(max_node)
        for node in G.neighbors(max_node):
            degree_list[node] =  degree_list[node] - 1
        max_node = max(degree_list , key = degree_list.get)
    return VC

file_name_list = ['as-22july06', 'delaunay_n10', 'email', 'football', 'jazz', 
                    'karate', 'hep-th', 'netscience', 'power', 'star', 'star2']

file_dir = os.path.dirname(os.path.realpath(__file__))

def approx_main(file_list):
    #output_data = []
    for file_name in file_list:
        graph_file = file_dir + '\data\\'+file_name+'.graph'
        output_file = file_dir + '\output\\'+file_name+ '_Approx.sol'
        G = read_graph('data/'+file_name+'.graph')
        VC = approx_vc(G)
        write_vc(output_file, len(VC), VC)
        
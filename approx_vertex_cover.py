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
import time
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

def approx_main(file_name):
    output_file = './' +file_name+ '_Approx.sol'
    trace_output = './' +file_name+ '_Approx.trace'
    G = read_graph('data/'+file_name+'.graph')
    start_time = time.time()
    VC = approx_vc(G)
    used_time = time.time() - start_time
    trace = [[round(used_time,2), len(VC)]] 
    write_vc(output_file, len(VC), VC)
    write_trace(trace_output, trace)    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 15:06:25 2017

@author: yujia
"""
import networkx as nx

def read_graph( filename):

    G = nx.Graph()
    lines = []
    with open(filename, 'r') as graph:
        num_data = graph.readline().split(' ')
        num_node,num_edge = int(num_data[0]),int(num_data[1]) #not used

        for line in graph:
            lines.append(line[:-2])

    G = nx.parse_adjlist(lines, nodetype = int)
    #print(G.nodes())
    #print(G.edges())
    return G

def write_vc(output_file, quality, vc):
    
    output = open(output_file, 'w')
    output.write(str(quality)+'\n')
    vc = ','.join(map(str, vc)) 
    output.write(vc+'\n')
    
    
def write_trace(output_file, sol_trace):
    
    output = open(output_file, 'w')
    for line in sol_trace:
        line = ','.join(map(str, line)) 
        output.write(line+'\n')


##if you want to test
#graph_file = 'data/karate.graph'
#G = read_graph(graph_file)
#
#quality = 10
#vc = [0,1,2]
#write_vc('test1.txt',quality,vc)
#
#sol_trace = [[3.45, 102],[7.94, 95]]
#write_trace('test2.txt',sol_trace)

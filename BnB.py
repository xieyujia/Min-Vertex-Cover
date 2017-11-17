#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:17:46 2017

@author: yujia
"""
from utils import * 
import networkx as nx
import sys
import time

'''
still need:
    0. if right to prune all connected nodes
    1. better expand
    2. better bound
'''

class Partial_solution():
    def __init__(self):
        self.solved = []
        self.remain_nodes = [] #sort it according to degree
        self.remain = nx.Graph() 

        
def choose(F):
    return F.pop(-1)

#if the node is not connected to any remaining edges, it's dead end
def check_dead_end(i,G): 
    return G.degree(i)==0

def lower_bound(Q):
    return len(nx.maximal_matching(Q))

def branch_and_bound(G,instance,cutoff):

    P = Partial_solution()
    P.remain_nodes = G.nodes().copy()
    degree_sorted = sorted(G.degree(P.remain_nodes).items(), key=lambda x: x[1]) 
    P.remain_nodes = [x[0] for x in degree_sorted]
    P.remain = G.copy()
    
    F = [P]
    B = (nx.number_of_nodes(G)-1,G.copy())
    p=0
    
    trace = []
    start_time = time.time()
    while len(F)!=0 :
    
        p = p+1
        P = choose(F)
        num_expand = 0
        for i in P.remain_nodes:
            num_expand = num_expand+1
            if num_expand>10:
                break
            #check if dead end
            if check_dead_end(i,P.remain)==True:
                continue
            
            #set up the new partial solution
            Q = Partial_solution()
            Q.solved = P.solved.copy()
            Q.solved.append(i)
            
            Q.remain = P.remain.copy()
            Q.remain.remove_node(i)
            
            Q.remain_nodes = P.remain_nodes.copy()
            Q.remain_nodes.remove(i)
            degree_sorted = sorted(Q.remain.degree(Q.remain_nodes).items(), key=lambda x: x[1]) 
            Q.remain_nodes = [x[0] for x in degree_sorted]
            
            
            #if Q is a solution
            if len(Q.remain.edges())==0: 
                if len(Q.solved)<B[0]:
                    B = (len(Q.solved),Q.solved)
                    time_used = time.time()-start_time
                    print("A better solution found in {} step:".format(p),B[0],time_used)
                    trace.append([time_used,B[0]])
                    
            #if not solution
            else:
                #check lower bound
                lb = lower_bound(Q.remain)
                if lb+len(Q.solved)<B[0]:
                    F.append(Q)
        
        if p%10000==0:
            print('Iter: ',p,'Best: ',B[0],'Time: ',time.time()-start_time)
        
        if time.time()-start_time>cutoff:
            break
            
    write_vc('out/{}_BnB_{}.sol'.format(instance,cutoff), B[0], sorted(B[1]))
    write_trace('out/{}_BnB_{}.trace'.format(instance,cutoff), trace)
    
    print('The best quality is ',B[0])
    print('The best vc is ',B[1])

def main():

    num_args = len(sys.argv)
    if num_args < 2:
        print ("error: not enough input arguments")
        exit(1)
    
    graph_file = sys.argv[1]
    
    G = read_graph(graph_file)
    
    cutoff = 600
    instance = graph_file.split('/')[2].split('.')[0]
    print(graph_file,instance)
    branch_and_bound(G,instance,cutoff)

if __name__ == '__main__':
    # run the experiments
    main()
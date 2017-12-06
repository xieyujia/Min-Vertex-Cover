#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 19:40:19 2017

@author: yujia
"""

from utils import * 
import networkx as nx
import sys
import time
import math


class Partial_solution():
    def __init__(self):
        self.solved = []
        self.remain = nx.Graph() 

        
def choose(F):
    return F.pop(-1)

#if the node is not connected to any remaining edges, it's dead end
def check_dead_end(i,G): 
    return G.degree(i)==0

def approx_vc(G): #G is  nx.graph
    #G = OG.copy()
    degree_list =dict( G.degree())
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

def lp(Q):
    node_list = list( Q.nodes() )
    edge_list = list( Q.edges() )
    n = len(node_list)
    m = len(edge_list)
    node_dict = {}
    for i in range(n):
        node_dict[node_list[i]] = i
    c = np.ones(n)
    A = np.zeros((m,n))
    b = -np.ones(m)
    
    for i,edge in enumerate(edge_list):
        #print(i,edge)
        A[i,node_dict[edge[0]]]=-1
        A[i,node_dict[edge[1]]]=-1
        
    res = scipy.optimize.linprog(c, A_ub=A, b_ub=b, bounds=(0,1))
    return res['fun']

def lower_bound(Q):
    return len(nx.maximal_matching(Q))
    #return math.ceil(len(approx_vc(Q))/2)
    #return lp(Q)

def branch_and_bound(G,instance,cutoff):

    P = Partial_solution()
    P.remain = G.copy()
    
    F = [P]
    B = (nx.number_of_nodes(G)-1,G.copy())
    p=0
    
    trace = []
    start_time = time.time()
    
    flag_found = False
    
    Q = Partial_solution()
    Q.remain = G.copy()
    while flag_found==False :
        remain_nodes = list(Q.remain.nodes()).copy()
        degree_list = dict(Q.remain.degree(remain_nodes))
        current_node = max(degree_list, key=degree_list.get)

        Q.solved.append(current_node)        
        Q.remain.remove_node(current_node)

        #if Q is a solution
        if len(Q.remain.edges())==0: 
            B = (len(Q.solved),Q.solved)
            time_used = time.time()-start_time
            print("A better solution found in {} step:".format(p),B[0],time_used)
            trace.append(["{0:.2f}".format(time_used),B[0]])
            flag_found = True
                    
    
    
    while len(F)!=0 :
    
        p = p+1
        P = choose(F)

        remain_nodes = list(P.remain.nodes()).copy()
        degree_list = dict(P.remain.degree(remain_nodes))
        current_node = max(degree_list, key=degree_list.get)
        
        #if not put it into vertex cover
        #set up the new partial solution
        neighbors = list(P.remain.neighbors(current_node))

        Q1 = Partial_solution()
        Q1.solved = P.solved.copy()
        Q1.solved.extend(neighbors )
        
        Q1.remain = P.remain.copy()
        Q1.remain.remove_node(current_node)
        Q1.remain.remove_nodes_from(neighbors)
        
    
        #if Q is a solution
        if len(Q1.remain.edges())==0: 
            if len(Q1.solved)<B[0]:
                B = (len(Q1.solved),Q1.solved)
                time_used = time.time()-start_time
                print("A better solution found in {} step:".format(p),B[0],time_used)
                trace.append(["{0:.2f}".format(time_used),B[0]])
                
        #if not solution
        else:
            #check lower bound
            lb = lower_bound(Q1.remain)
            if lb+len(Q1.solved)<B[0]:
                F.append(Q1)
        
            #check if dead end
        if check_dead_end(current_node,P.remain)==False:
        
            #set up the new partial solution
            Q = Partial_solution()
            Q.solved = P.solved.copy()
            Q.solved.append(current_node)
            
            Q.remain = P.remain.copy()
            Q.remain.remove_node(current_node)
            
        
            #if Q is a solution
            if len(Q.remain.edges())==0: 
                if len(Q.solved)<B[0]:
                    B = (len(Q.solved),Q.solved)
                    time_used = time.time()-start_time
                    print("A better solution found in {} step:".format(p),B[0],time_used)
                    trace.append(["{0:.2f}".format(time_used),B[0]])
                    
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
    print(B[0],B[1])
    write_vc('{}_BnB_{}.sol'.format(instance,cutoff), B[0], sorted(B[1]))
    write_trace('{}_BnB_{}.trace'.format(instance,cutoff), trace)
    
    print('The best quality is ',B[0])
    print('The best vc is ',B[1])
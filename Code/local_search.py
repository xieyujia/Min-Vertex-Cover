#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 20:02:38 2017

@author: yujia
"""

#Shu Liu, E-mail:sliu459@gatech,.edu
# Local Search Algorithm 1 (Based on Shaowei Cai's paper: Balance between Complexity and Quality:
# Local Search for Minimum Vertex Cover in Massive Graphs )
# Local Search Algorithm 2 (Based on the idea of finding the Maximum Independent Set)

import random
import networkx as nx
import time
import copy
import sys

class RunLS1:

    def read_graph(self,filename):
        G = nx.Graph()
        lines = []
        with open(filename, 'r') as graph:
            num_data = graph.readline().split(' ')
            num_node, num_edge = int(num_data[0]), int(num_data[1])  # not used
            i = 0
            for line in graph:
                i = i + 1
                lines.append(str(i) + ' ' + line[:-2])
        G = nx.parse_adjlist(lines[:-1], nodetype=int)

        return G

    def write_vc(self,output_file, quality, vc):
        output = output_file
        output.write(str(quality) + '\n')
        vc = ','.join(map(str, vc))
        output.write(vc + '\n')

    def write_trace(self,output_file, sol_trace):
        output = output_file
        for line in sol_trace:
            line = ','.join(map(str, line))
            output.write(line + '\n')

    # Use the algorithm given in Shaowei Cai's paper: "Balance between Complexity and Quality:
    # Local Search for Minimum Vertex Cover in Massive Graphs" to generate the initial Vertex Cover.
    def ConstructVC(self,G):
        nx.set_edge_attributes(G,'tag',0)
        nx.set_node_attributes(G,'Ctag',0)
        nx.set_node_attributes(G, 'lossfunction', 0)

        C=[]

        for e in G.edges_iter():
            if G[e[0]][e[1]]['tag'] == 0:  # When the edge is not covered by current Vertex Cover
               degree1=G.degree(e[0])
               degree2=G.degree(e[1])
               if degree1>degree2:  # Choose the endpoint with higher degrees to add to the set C
                  node_added_to_C = e[0]
               else:
                  node_added_to_C = e[1]
               C.append(node_added_to_C)
               G.node[node_added_to_C]['Ctag'] = 1  # This node is selected in the Vertex Cover set C
               for v in G.neighbors(node_added_to_C):
                   G[node_added_to_C][v]['tag']=1  # After we include the node "node_added_to_C" to C, we need to mark every edge attached to this node as "covered by C".

        for v in C:  # Compute the loss function of every vertex in C
            for neighborvertex in G.neighbors(v):
                if G.node[neighborvertex]['Ctag'] == 0: # once there is a neighbour vertex of v is not in C, we add 1 to the loss function of v
                    G.node[v]['lossfunction']=G.node[v]['lossfunction']+1

        for v in C:  # Delete vertex in C with zero loss
            if G.node[v]['lossfunction'] == 0:
                G.node[v]['Ctag']=0  # Change the Ctag of the vertex when it is removed from C
                C.remove(v)
                for neighborvertex in G.neighbors(v):
                    if G.node[neighborvertex]['Ctag'] == 1:
                        G.node[neighborvertex]['lossfunction']=G.node[neighborvertex]['lossfunction']+1  # update the loss function of vertice in C at the same time you remove a vertex from C

        return C

    def ConstructVC_lower_quality(self,G):
        nx.set_edge_attributes(G,'tag',0)
        nx.set_node_attributes(G,'Ctag',0)
        nx.set_node_attributes(G, 'lossfunction', 0)

        C=[]

        for e in G.edges_iter():
            if G[e[0]][e[1]]['tag'] == 0:  # When the edge is not covered by current Vertex Cover
               degree1=G.degree(e[0])
               degree2=G.degree(e[1])
               if degree1>degree2:  # Choose the endpoint with higher degrees to add to the set C
                  node_added_to_C = e[0]
               else:
                  node_added_to_C = e[1]
               C.append(node_added_to_C)
               G.node[node_added_to_C]['Ctag'] = 1  # This node is selected in the Vertex Cover set C
               for v in G.neighbors(node_added_to_C):
                   G[node_added_to_C][v]['tag']=1  # After we include the node "node_added_to_C" to C, we need to mark every edge attached to this node as "covered by C".
        return C

    def ChooseRandomVertex(self,G,C,k):
        randomlist=random.sample(C, k)
#        print('random vertex chosen in VC:',randomlist)
        minloss=G.node[randomlist[0]]['lossfunction']
        vertexchosen=randomlist[0]
        for v in randomlist:
            if G.node[v]['lossfunction']<minloss:
                minloss=G.node[v]['lossfunction']
                vertexchosen=v
        return vertexchosen

    # Local Search Algorithm 1 The framework is based on Shaowei Cai's paper: "Balance between Complexity and Quality:
    # Local Search for Minimum Vertex Cover in Massive Graphs".
    def MVCLS1(self,cutoff,sample_num,seed):
        random.seed(seed)
        for i, graph in enumerate(graphFiles):
            G = self.read_graph(graph)

        C = self.ConstructVC(G)
      # f you want to focus on LS algorithm, you can choose to run ConstructVC_lower_quality which gives an initial VC with rather low quality
      # C = self.ConstructVC_lower_quality(G)

        nx.set_node_attributes(G,'gainfunction',0)

        output_file_1 = open('.\\Solutions\\' + fileNames[0] + '_LS1_' + str(cutoff) + '_' + str(seed)+'.sol', 'w')
        output_file_2 = open('.\\Solutions\\' + fileNames[0] + '_LS1_' + str(cutoff) + '_' + str(seed)+'.trace', 'w')
        sol_trace = []

        list_of_uncovered_edges=[]
        tagcover = 1 # tagcover = 1 means current C is a vertex cover
        begintime=time.time()
        cuttime=time.time()
        elapsetime=cuttime-begintime

        while elapsetime < cutoff:
            if tagcover == 1:
                Cstar = copy.copy(C)
                sol_trace.append([round(time.time()-begintime,2), len(Cstar)])
                Min_Loss=G.node[C[0]]['lossfunction']
                Min_Loss_Vertex=C[0]
                for v in C:
                    if G.node[v]['lossfunction'] < Min_Loss:
                        Min_Loss = G.node[v]['lossfunction']
                        Min_Loss_Vertex=v
                for u in G.neighbors(Min_Loss_Vertex):
                    if G.node[u]['Ctag'] == 1:
                        G.node[u]['lossfunction'] = G.node[u]['lossfunction']+1
                    else:
                        G.node[u]['gainfunction']=G.node[u]['gainfunction']+1
                        G.node[Min_Loss_Vertex]['gainfunction'] = G.node[Min_Loss_Vertex]['gainfunction'] + 1
                        G[Min_Loss_Vertex][u]['tag']=0
                        list_of_uncovered_edges.append((Min_Loss_Vertex,u))
                        list_of_uncovered_edges.append((u,Min_Loss_Vertex))
                G.node[Min_Loss_Vertex]['Ctag']=0
                G.node[Min_Loss_Vertex]['lossfunction']=0
                C.remove(Min_Loss_Vertex)
            vertex_removed=self.ChooseRandomVertex(G,C,sample_num)
            C.remove(vertex_removed)
            G.node[vertex_removed]['Ctag']=0
            G.node[vertex_removed]['lossfunction']=0
            for u in G.neighbors(vertex_removed):
                if G.node[u]['Ctag']==1:
                    G.node[u]['lossfunction']=G.node[u]['lossfunction']+1
                else:
                    G.node[vertex_removed]['gainfunction']=G.node[vertex_removed]['gainfunction']+1
                    G.node[u]['gainfunction']=G.node[u]['gainfunction']+1
                    G[vertex_removed][u]['tag']=0
                    list_of_uncovered_edges.append((vertex_removed, u))
                    list_of_uncovered_edges.append((u, vertex_removed))
            if len(list_of_uncovered_edges) > 0 :
               l=random.sample(list_of_uncovered_edges,1)
               e=l[0]
               if G.node[e[0]]['gainfunction'] > G.node[e[1]]['gainfunction']:
                   vertex_added=e[0]
               else:
                   vertex_added=e[1]
               C.append(vertex_added)
               G.node[vertex_added]['Ctag']=1
               G.node[vertex_added]['gainfunction']=0
               for u in G.neighbors(vertex_added):
                   if G.node[u]['Ctag']==1:
                       G.node[u]['lossfunction']=G.node[u]['lossfunction']-1
                   else:
                       G.node[vertex_added]['lossfunction']=G.node[vertex_added]['lossfunction']+1
                       G.node[u]['gainfunction']=G.node[u]['gainfunction']-1
                       G[u][vertex_added]['tag']=1
                       if ((u,vertex_added) in list_of_uncovered_edges) or ((vertex_added,u) in list_of_uncovered_edges):
                           list_of_uncovered_edges.remove((vertex_added,u))
                           list_of_uncovered_edges.remove((u,vertex_added))
            if len(list_of_uncovered_edges) > 0:  #If there are edges not covered by current set C, set tagcover to 0
                tagcover = 0
            else:
                tagcover = 1
            elapsetime = time.time() - begintime

        quality=len(Cstar)
       # Cstar.sort()
        self.write_vc(output_file_1,quality,Cstar)
        self.write_trace(output_file_2, sol_trace)

    # main( cutoff, sample_num, randomseed).
    # Here sample_num is a parameter of our algorithm. It can be set to any fixed positive integer. Here we set it to be 6.
    def main(self,cutoff,sample_num,seed):
        self.MVCLS1(cutoff,sample_num,seed)

class RunLS2:

    def read_graph(self,filename):
        G = nx.Graph()
        lines = []
        with open(filename, 'r') as graph:
            num_data = graph.readline().split(' ')
            num_node, num_edge = int(num_data[0]), int(num_data[1])  # not used
            i = 0
            for line in graph:
                i = i + 1
                lines.append(str(i) + ' ' + line[:-2])
        G = nx.parse_adjlist(lines[:-1], nodetype=int)
        return G

    def write_vc(self,output_file, quality, vc):
        output = output_file
        output.write(str(quality) + '\n')
        vc = ','.join(map(str, vc))
        output.write(vc + '\n')

    def write_trace(self,output_file, sol_trace):
        output = output_file
        for line in sol_trace:
            line = ','.join(map(str, line))
            output.write(line + '\n')

    def ConstructVC(self,G):
        nx.set_edge_attributes(G,'tag',0)
        nx.set_node_attributes(G,'Ctag',0)
        nx.set_node_attributes(G, 'lossfunction', 0)

        C=[]

        for e in G.edges_iter():
            if G[e[0]][e[1]]['tag'] == 0:  # When the edge is not covered by current Vertex Cover
               degree1=G.degree(e[0])
               degree2=G.degree(e[1])
               if degree1>degree2:  # Choose the endpoint with higher degrees to add to the set C
                  node_added_to_C = e[0]
               else:
                  node_added_to_C = e[1]
               C.append(node_added_to_C)
               G.node[node_added_to_C]['Ctag'] = 1  # This node is selected in the Vertex Cover set C
               for v in G.neighbors(node_added_to_C):
                   G[node_added_to_C][v]['tag']=1  # After we include the node "node_added_to_C" to C, we need to mark every edge attached to this node as "covered by C".

        for v in C:  # Compute the loss function of every vertex in C
            for neighborvertex in G.neighbors(v):
                if G.node[neighborvertex]['Ctag'] == 0: # once there is a neighbour vertex of v is not in C, we add 1 to the loss function of v
                    G.node[v]['lossfunction']=G.node[v]['lossfunction']+1

        for v in C:  # Delete vertex in C with zero loss
            if G.node[v]['lossfunction'] == 0:
                G.node[v]['Ctag']=0  # Change the Ctag of the vertex when it is removed from C
                C.remove(v)
                for neighborvertex in G.neighbors(v):
                    if G.node[neighborvertex]['Ctag'] == 1:
                        G.node[neighborvertex]['lossfunction']=G.node[neighborvertex]['lossfunction']+1  # update the loss function of vertice in C at the same time you remove a vertex from C

        return C

    def ConstructVC_lower_quality(self,G):
        nx.set_edge_attributes(G,'tag',0)
        nx.set_node_attributes(G,'Ctag',0)
        nx.set_node_attributes(G, 'lossfunction', 0)

        C=[]

        for e in G.edges_iter():
            if G[e[0]][e[1]]['tag'] == 0:  # When the edge is not covered by current Vertex Cover
               degree1=G.degree(e[0])
               degree2=G.degree(e[1])
               if degree1>degree2:  # Choose the endpoint with higher degrees to add to the set C
                  node_added_to_C = e[0]
               else:
                  node_added_to_C = e[1]
               C.append(node_added_to_C)
               G.node[node_added_to_C]['Ctag'] = 1  # This node is selected in the Vertex Cover set C
               for v in G.neighbors(node_added_to_C):
                   G[node_added_to_C][v]['tag']=1  # After we include the node "node_added_to_C" to C, we need to mark every edge attached to this node as "covered by C".
        return C

    def Is_VC(self,G,VC): # determine whether set VC is a vertex cover of G
       tag = 1
       for e in G.edges_iter():
           if e[0] not in VC:
               if e[1] not in VC:
                   tag = 0
       return tag

    # Local Search Algorithm 2, based on the idea of converting MVC to MIS (maximum independent set problem)
    def MVCLS2(self,cutoff,sample_num,seed):
        random.seed(seed)
        for i, graph in enumerate(graphFiles):
            G = self.read_graph(graph)

        numV = G.number_of_nodes()

        C = self.ConstructVC(G)
       # f you want to focus on LS algorithm, you can choose to run ConstructVC_lower_quality which gives an initial VC with rather low quality
       #C = self.ConstructVC_lower_quality(G)
        V=[i+1 for i in range(len(G.node))]
        X=[i for i in V if i not in C]
        freevertexset=[]

        nx.set_node_attributes(G, 'tagX', 0)
        nx.set_node_attributes(G, 'tau',0)
        nx.set_node_attributes(G,'tagfree',1)

        for i in X:
            G.node[i]['tagX']=1
        for i in C:
            for j in G.neighbors(i):
                if G.node[j]['tagX'] == 1:
                    G.node[i]['tagfree']=0
                    G.node[i]['tau']=G.node[i]['tau']+1
            if G.node[i]['tagfree'] == 1:
                freevertexset.append(i)

        output_file_1 = open('.\\Solutions\\' + fileNames[0] + '_LS2_' + str(cutoff) + '_' + str(seed)+'.sol', 'w')
        output_file_2 = open('.\\Solutions\\' + fileNames[0] + '_LS2_' + str(cutoff) + '_' + str(seed)+'.trace','w')
        sol_trace = []

        begintime=time.time()
        cutime=time.time()
        elapsetime=cutime-begintime
        Xstar=[]

        while elapsetime < cutoff:
            if len(X) >= len(Xstar):
                if len(X) > len(Xstar):
                    sol_trace.append([round(time.time()-begintime,2), numV-len(X)])
                Xstar=copy.copy(X)
                Gstar=G.copy()
                freevertexset_star=copy.copy(freevertexset)
            else:
                X=copy.copy(Xstar)
                G=Gstar.copy()
                freevertexset=copy.copy(freevertexset_star)

            X_c=[i for i in V if i not in X]
            randomlist=random.sample(X_c,sample_num)
            mintau=G.node[randomlist[0]]['tau']
            Min_tauvertex=randomlist[0]
            for v in randomlist:
                if G.node[v]['tau'] < mintau:
                    mintau=G.node[v]['tau']
                    Min_tauvertex=v
            # Update everything when you remove neighbors of Min_tau_vertex in X and add Min_tau vertex into X
            for v in G.neighbors(Min_tauvertex):
                G.node[v]['tau']=G.node[v]['tau']+1
                if G.node[v]['tagX'] == 1:
                    for u in G.neighbors(v):
                        if u != Min_tauvertex:
                            G.node[u]['tau']=G.node[u]['tau']-1
                    G.node[v]['tagX'] = 0
                    G.node[v]['tagfree'] = 0
                    X.remove(v)
            # Update  freevertexset
            for w in G.neighbors(Min_tauvertex):
                if (G.node[w]['tau'] == 0) and (G.node[u]['tagX'] == 0):
                    if u not in freevertexset:
                        freevertexset.append(u)
                        G.node[u]['tagfree'] = 1
            G.node[Min_tauvertex]['tagfree']=1
            G.node[Min_tauvertex]['tagX']=1
            G.node[Min_tauvertex]['tau']=0
            X.append(Min_tauvertex)

            while len(freevertexset) > 0:
                vertex = random.sample(freevertexset,1)
                for v in G.neighbors(vertex[0]):
                    G.node[v]['tau']=G.node[v]['tau']+1
                    if (G.node[v]['tagfree'] == 1) and (G.node[v]['tagX']!=1) :
                        G.node[v]['tagfree'] = 0
                        freevertexset.remove(v)
                G.node[vertex[0]]['tagX']=1
                G.node[vertex[0]]['tau'] = 0
                X.append(vertex[0])
                freevertexset.remove(vertex[0])
            elapsetime=time.time()-begintime
        Cstar = [i for i in V if i not in Xstar]
        tag = self.Is_VC(G, Cstar)
        if tag == 0:
            for e in G.edges_iter():
                if e[0] not in Cstar:
                    if e[1] not in Cstar:
                        Cstar.append(e[0])
        quality = len(Cstar)
        self.write_vc(output_file_1, quality, Cstar)
        self.write_trace(output_file_2, sol_trace)

    def main(self,cutoff,sample_num,seed):
        run = RunLS2()
        run.MVCLS2(cutoff,sample_num,seed)

if __name__ == '__main__':# run LS1 or LS2

   num_args = len(sys.argv)

   if num_args < 4:
       print("error: you lose some arguments!")
       exit(1)

   name_of_graph= sys.argv[1]
   name_of_algorithm = sys.argv[2]
   cutoff_time = float(sys.argv[3])
   randomseed = int(sys.argv[4])

   fileNames = [name_of_graph]
   graphFiles = [".\\Data\\{}.graph".format(f) for f in fileNames]

   if name_of_algorithm == 'LS1':
      run = RunLS1()
      run.main(cutoff_time,6,randomseed)
   elif name_of_algorithm == 'LS2':
      run = RunLS2()
      run.main(cutoff_time,10,randomseed)

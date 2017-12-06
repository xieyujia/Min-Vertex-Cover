#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 19:28:52 2017

@author: yujia
"""
from branch_and_bound import *
from approx_vertex_cover import *
from local_search import *
import argparse

def main():

    
   parser = argparse.ArgumentParser()
   parser.add_argument('-inst', type = str, dest = 'path_of_graph', help = 'please use / as separator', required=True)
   parser.add_argument('-alg', type = str, dest = 'name_of_alg', help = 'LS1|LS2|Approx|BnB', required=True)
   parser.add_argument('-time', type = int, dest = 'cutoff_time', required=True)
   parser.add_argument('-seed', type = int, dest = 'randomseed', required=True)
   args = parser.parse_args()

   path_of_graph_split = args.path_of_graph.split('/')
   fileNames = path_of_graph_split[-1]
   fileNames = fileNames.split('.')
   fileNames = fileNames[0]
   graphFiles = args.path_of_graph
   name_of_algorithm = args.name_of_alg
   cutoff_time = args.cutoff_time
   randomseed = args.randomseed
   
   if name_of_algorithm == 'BnB':
      G = read_graph(graphFiles)
      branch_and_bound(G,fileNames,cutoff_time)
   elif name_of_algorithm == 'LS1':
      run = RunLS1()
      run.main(cutoff_time,6,randomseed,[graphFiles], [fileNames])
   elif name_of_algorithm == 'LS2':
      run = RunLS2()
      run.main(cutoff_time,10,randomseed,[graphFiles], [fileNames])
   elif name_of_algorithm == 'Approx':
      G = read_graph(graphFiles)
      approx_main(fileNames, G)
   else:
      print("No such method!")

if __name__ == '__main__':
    # run the experiments
    main()

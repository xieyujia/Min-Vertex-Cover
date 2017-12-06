#!/bin/bash

#!`ls ./data/ | grep .graph`
graphFiles=`ls ./data/ | grep .graph`
for algorithm in LS1 LS2 BnB Approx
do
	for graph in $graphFiles
	do
		filename=`echo $graph | cut -d'.' -f1`
		echo $graph $filename
		python main.py -inst ./data/$graph -alg $algorithm -time 5 -seed 777  
	done
done
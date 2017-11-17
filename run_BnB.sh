#!/bin/bash

#!`ls ./data/ | grep .graph`
graphFiles=`ls ./data/ | grep .graph`

for graph in $graphFiles
do
	filename=`echo $graph | cut -d'.' -f1`
	echo $graph $filename
	python BnB.py  ./data/$graph 


done
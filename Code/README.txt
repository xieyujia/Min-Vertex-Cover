The excutable: main.py

How to run this executable:

1. Open Command Prompt. 

2. Enter the folder "Code"


3. Type 'python main.py -inst PATH_TO_GRAPHFILE -alg ALGORITHM_NAME -time CUTOFF_TIME -seed RANDOM_SEED'
   

Example: python main.py -inst ./data/email.graph -alg LS1 -time 60 -seed 777
This means apply algorithm LS1 to the graph 'email', set cutoff time to be 60s, choose randomseed = 1.

PATH_TO_GRAPHFILE is the path to the data file.

ALGORITHM_NAME can be "BnB", "Approx", "LS1", "LS2".

4. If you need help, type 'python main.py -h' to see usage instruction.
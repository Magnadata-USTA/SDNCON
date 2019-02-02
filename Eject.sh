#!/bin/bash

#Iterations = int(sys.argv[1])
#Mutations = int(sys.argv[2]) #0 =changelinks ; 1=changecontroller
#maxFlowSetupLatency = int(sys.argv[3])
#maxInterControllerLatency = int(sys.argv[4])
#PercentageNode = (sys.argv[5])
#MemorySize = int(sys.argv[6])
#LRQ = int(sys.argv[7])

for w in {1..10}

do

    #echo $w

    python network.py 30 0 50 70 10 10 $w

    #os.system('python network.py 30 0 50 70 10 10 w')

done


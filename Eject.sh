#!/bin/bash

#Iterations = int(sys.argv[1])
#Mutations = int(sys.argv[2]) #0 =changelinks ; 1=changecontroller
#maxFlowSetupLatency = int(sys.argv[3])
#maxInterControllerLatency = int(sys.argv[4])
#PercentageNode = (sys.argv[5])
#MemorySize = int(sys.argv[6])
#LRQ = int(sys.argv[7])

Mut=30 #Mutations
MT=0 #Moviment type
Ptg=10 #PercentageNode
MFSL=50 #maxFlowSetupLatency
MCL=70 #maxInterControllerLatency


for w in {1..10}
do
    #echo $w
    python network.py $Mut $MT $MFSL $MCL $Ptg 10 $w
    #os.system('python network.py 30 0 50 70 10 10 w')
done

cat /dev/null > Final.csv
for i in `ls MsTabu*`
do
#echo $i
var1=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $1}' | sed -r 's/^.{2}//'` # to get Cost
Mean=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $2}'`
stdd=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $3}'`
cV=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $4}'`
Mean2=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $5}'`
stdd2=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $6}'`
cV2=`cat $i | head -1 | awk 'BEGIN { FS=";" } {print $7}'`

echo $var1";"$MFSL";"$Ptg";"$MCL";"$Mean";"$stdd";"$cV";"$Mean2";"$stdd2";"$cV2
echo $var1";"$MFSL";"$Ptg";"$MCL";"$Mean";"$stdd";"$cV";"$Mean2";"$stdd2";"$cV2 >> Final.csv
#rint("El costo para la solución es: "+str(solutionCost))
#print("El Media Arit. 2LP es: "+str(mean))
#print("El Desviación Est. 2LP es: "+str(stdd))
#print("El Coeficiente de Vari. 2LP es: "+str(cV))
#print("El Media Arit. ICC es: "+str(mean1))
#print("El Desviación Est. ICC es: "+str(stdd1))
#print("El Coeficiente de Vari. ICC es: "+str(cV1))
 
#Imprimir: [costo promedio de las 10 veces, maxFlowSetupLatency; % de controladores; maxInterControllerLatency; CV; STD; TipoMovimiento]

done

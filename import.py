##############################################################################
# Nombre        : import.py
# Descripción   : It takes the information from Transfom.sh Initial Node
#                 Final Node and HAVERSINE Formule
#                                 
# Parámetros:
# Realizado Por : 
#
# HISTORIAL DE CAMBIOS:
#Richard Abuabara Caserta
# 
##############################################################################
import re
from collections import defaultdict
#from pprint import pprint
from random import randint

data_from_file=open('newAtmnet.txt', 'r').read()

def transform_to_my_format(data):
    d = defaultdict(dict)
    for (i1, i2, i3) in re.findall(r'([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)', data):
        d[i1].update({i2: float(i3)})
    return d

Graph_Lat=transform_to_my_format(data_from_file)

def dijkstra_latency(start,goal):
    Graph_Lat=transform_to_my_format(data_from_file)
    graph=Graph_Lat
    shortest_distance = {}
    predecessor = {}
    unseenNodes= {}
    unseenNodes = graph
    infinity = 9999999
    path = []
   
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
 
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
 
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)
 
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        dj2=float(shortest_distance[goal])*1.1 #Latencia +/- 10
        dj3=float(shortest_distance[goal])*1.2 #Price +/- 20 Verificar ojooo
        f= open("output.txt","a+")
        if (int(start) != int(goal)):
            f.write('LC'+start+'_'+goal+','+'"LC'+start+'_'+goal+'",'+str(shortest_distance[goal])+','+'100'+',"Claro",'+'"S'+start+'",'+'"S'+goal+'"'+ "\n")
            f.write('LM'+start+'_'+goal+','+'"LM'+start+'_'+goal+'",'+str(dj2)+','+'75'+',"Movistar",'+'"S'+start+'",'+'"S'+goal+'"'+ "\n")
            f.write('LT'+start+'_'+goal+','+'"LT'+start+'_'+goal+'",'+str(dj3)+','+'60'+',"Tigo",'+'"S'+start+'",'+'"S'+goal+'"'+ "\n")
            #f.write('mynet.addLink(LT'+start+'_'+goal+')'+ "\n")
        else:
            f.write('LC'+start+'_'+goal+','+'"LC'+start+'_'+goal+'",'+str(shortest_distance[goal])+','+'0'+',"Claro",'+'"S'+start+'",'+'"S'+goal+'"'+ "\n")
            f.write('LM'+start+'_'+goal+','+'"LM'+start+'_'+goal+'",'+str(dj2)+','+'0'+',"Movistar",'+'"S'+start+'",'+'"S'+goal+'"'+ "\n")
            f.write('LT'+start+'_'+goal+','+'"LT'+start+'_'+goal+'",'+str(dj3)+','+'0'+',"Tigo",'+'"S'+start+'",'+'"S'+goal+'"'+ "\n")
            #f.write('mynet.addLink(LT'+start+'_'+goal+')'+ "\n")
            
        f.close()

####modulo impresion######
max=(len(Graph_Lat))
for i in range(max): #este es el for - source
    #print (i)
    for j in range(max):
        dijkstra_latency(str(i), str(j))   
	#debo imprimir L571=Link("L571",77,770,"operador1",5,7)   
########Imprimir 2do Rquerimiento################

max=(len(Graph_Lat))

for i in range(max): #este es el for - source
    f= open("output.txt","a+")
    f.write('C'+str(i)+',S'+str(i)+',priceController,False'+"\n")
    f.close()


#Switch creation and aggregation
for i in range(max): #este es el for - source
    f= open("output.txt","a+")
    #f.write('S'+str(i)+' = Switch("S'+str(i)+'", '+str(randint(10000,500000))+', "C'+str(i)+'", '+str(randint(2,10))+')'+"\n")
    f.write('S'+str(i)+','+str(randint(10000,500000))+','+str(randint(2,10))+"\n")
    f.close()

#S0 = Switch("S0", randint(10000,500000), "C0", randint(2,10))
#mynet.addSwitch(S0)   

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from random import randint, uniform
from itertools import cycle
import re
filename = 'output.txt'

zip_list = []
class Controller():
    def __init__(self,idController,deployedIn,priceController,state):
        self.idController=idController
        self.deployedIn=deployedIn
        self.controlledSW= [] # lista switches que controla, lista
        self.priceController=priceController
        self.state=state
        self.receivedRequest=0 ###Crear una funcion que agregue switches a "controlledSW", e integrar funcion para que sume las peticiones
        self.totalProcessingDelay=0
        
    def __str__(self):
        return """\
idController:\t\t{}
deployedId:\t\t{}
controlledSW:\t\t{}
priceController:\t{}
state:\t\t\t{}
receivedReques:\t\t{}
processingDelay:\t{}
""".format(self.idController,self.deployedIn,self.controlledSW,self.priceController,self.state,self.receivedRequest,self.totalProcessingDelay)
        

    def getPriceController(self):
        return self.priceController
    
    def addControlledSW(self, switch):    
        self.controlledSW.append(switch)
    
    def setSWDeployed(self, switch): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        self.deployedIn=switch #Aqui van almacenadoslos awitches todos
        
    def setState(self, state): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        self.state=state
    
    def getState(self): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        return self.state
        
    def getReceivedRequest(self): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        temp = 0
        for switch in self.controlledSW:
            temp += switch.getFlowSetupRequest() #Sumatoria total de peticiones de todos los switches que tiene el controlador
        self.receivedRequest = temp
        return self.receivedRequest
        
    def getTotalProcessingDelay(self): #Get: Obtiene datos, devolver datos, procesa         
        self.totalProcessingDelay = (self.getReceivedRequest()/1.6)*self.deployedIn.getProcessingDelay()                
        return self.totalProcessingDelay
  
class Switch():
    def __init__(self,idSwitch,flowSetupRequest,processingDelay):
        self.idSwitch=idSwitch
        self.flowSetupRequest=flowSetupRequest
        self.processingDelay=processingDelay

    def getFlowSetupRequest(self):
        return self.flowSetupRequest        
        
    def getProcessingDelay(self):
        #Time to process 1.6 M of flow setup request in ms.
        return self.processingDelay    
    
    def getIdSwitch(self):
        return self.idSwitch
    
class Network():
    #def __init__(self, maxFlowSetupLatency, maxInterControllerLatency):
    def __init__(self):
        self.controllerCost = 0 #Costo de todos los controladores de la red
        self.controllerSWLinkCost = 0  #Costo total de los enlaces de controlador a Switch
        self.intercontrollerLinkCost = 0
        self.totalCost = 0
        self.switches= []    
        self.controllers= []    
        self.links = []
        #self.maxFlowSetupLatency = maxFlowSetupLatency
        #self.maxInterControllerLatency = maxInterControllerLatency
    
    def addLink(self, link):
        self.links.append(link)
    
    def calculateTotalCost(self):
        cost = 0
        for link in self.links:
            if(link.getState() == True):
                cost += link.getPrice()
        return cost
    
    def calculateControllerCost(self):
        controllerCost = 0
        for controller in self.controllers:
            if(controller.getState() == True):
                controllerCost += controller.priceController
        return controllerCost
        
    def getlinks(self):  #Imprime los links que hay
        return self.links
    
    def addSwitch(self, switch):
        self.switches.append(switch)    
    
    def addController(self, controller):
        self.controllers.append(controller)
        
    def linkActivation(self):
        '''This function activates randomly one link 
        between each pair of switches.
        '''
        #1.Iterate over "links" list and set status to False
        for link in self.links:
            link.setState(False)
        #2.Activate link: Choose each three positions a Link and set status to True
        lim_inf = 0        
        while(lim_inf <= len(self.links)-3):
            lim_sup = lim_inf + 2               
            index = randint(lim_inf,lim_sup)
            self.links[index].setState(True)
            lim_inf += 3
            
    def randomSolution(self, p_controllers):   
        SDNisValid = False
        #1.Activate controllers
        #1.1 Activa controllers randomly
        for controller in self.controllers:
            if(uniform(0, 1)<p_controllers):
                controller.setState(True)
                SDNisValid = True
                #print(controller.idController)
        #1.2 Activate at least on controller radomly (else)
        if(SDNisValid == False):
            controller = self.controllers[randint(0,len(self.switches)-1)]
            controller.setState(True)        
        #2.Assign switches to controllers
        #2.1Create list with active controllers
        activecontrollers = []
        ActiveControllers=[]
        for controller in self.controllers:
            if(controller.getState()==True):
                activecontrollers.append(controller)
                ActiveControllers.append(controller.idController)                             
        
        #2.2 Assign switches to active controllers
        #Zipping
        for controller in activecontrollers:            
            controller.addControlledSW(self.switches[0])
            print(controller.idController)
       
        ActiveSwitches=[]
        for Sws in self.switches:            
            #print(Sws.idSwitch)
            ActiveSwitches.append(Sws.idSwitch)
        print (*ActiveSwitches)
        
        #To assing Cn Sn rule
        New=()
        SelfSC=[]
        for i in ActiveSwitches:
            i= i.replace('S', 'C')
            for j in ActiveControllers:
                if (i == j):
                    #print(i)
                    i= i.replace('C', 'S')
                    ActiveSwitches.remove(i)
                    New=(i,j)
                    SelfSC.append(New)
        #print(*ActiveSwitches)
        #print(*SelfSC)            
        
        zip_list = zip(ActiveSwitches, cycle(ActiveControllers)) if len(ActiveSwitches) > len(ActiveControllers) else zip(cycle(ActiveSwitches), ActiveControllers)
        zip_list=list(zip_list)
        #print(zip_list)
        
        #Adding list Cn Sn to Zip_list after Cn Sn Rule
        for i in SelfSC:
            zip_list.append(i)
        #print(*zip_list) #para imprimir la lista CnSn
        
        #Regarding the match done by zip_list, addition from each link is required
        LLinks=[]
        Providers=["LC","LM","LT"]
        for start,target in zip_list:
            #Controller.addControlledSW(target,start)
            #target.Controller.addControlledSW(start)
            #Change to assing differents providers, due to it was just Claro 
            x=randint(0,2)
            LLinks.append(Providers[x]+str(start.lstrip('S'))+"_"+str(target.lstrip('C'))) #var = "LC"+str(start.lstrip('S'))+'_'+str(target.lstrip('C'))
            
        #print(LLinks) #Descomentar para ver la asignación Controller-Switch
        Link_Cost=0
        for w in LLinks:
            for y in self.links:
                if (y.idLink==w):
                    #print("encontrado"+str(y.idLink)+str(y.price))
                    Link_Cost+=y.price
                    
        #2.3 We have to calculate Intercontroller Cost
        #We got active controller in ActiveControllers variable, let's Do it
        IntercontrollerCostLC = 0;
        Holder = len(ActiveControllers)
        if (Holder > 1):
            print("We have Length: " + str(Holder))
            List_IntercotrollerCost = []
            New=()
            SelfSC=[]
            for w in range(Holder):
                for y in ActiveControllers:
                    flag=0
                    if(str(ActiveControllers[w].lstrip('C')) != str(y.lstrip('C'))):#cambiar esta linea cuando se cambie el formato
                        x=randint(0,2)
                        r=str(ActiveControllers[w].lstrip('C'))
                        t=str(y.lstrip('C'))
                        New=(r,t)
                        SelfSC.append(New)
                        #It is Needed to know which links were connected to skip inverse
                        for u,v in SelfSC:
                            if ((u==t) & (v==r)):
                                flag=1
                        if (flag==0):        
                            List_IntercotrollerCost.append(Providers[x]+str(ActiveControllers[w].lstrip('C'))+"_"+str(y.lstrip('C')))
                            New=(t,r)
                            SelfSC.append(New)
                            flag=0
            #print(*List_IntercotrollerCost) #descomentar para ver la lista de links-intercontrollers
            for w in List_IntercotrollerCost:
                for y in self.links:
                    if (y.idLink==w):
                        IntercontrollerCostLC+=y.price
        return (Link_Cost,IntercontrollerCostLC)
                    
            
class Link():
    def __init__(self,idLink, latency, price, carrierId, sourceId , destinationId):
        self.idLink = idLink
        #print(idLink)
        self.latency = latency
        #print(latency)        
        self.price = int(price)
        #print(price)        
        self.carrierId = carrierId        
        self.sourceId = sourceId        
        self.destinationId = destinationId
        self.state = False

    def getPrice(self):
        return self.price

    def getidLink(self):
        return self.idLink

    def getState(self):
        return self.state

    def setState(self, state):
        self.state=state

##MyNet
mynet = Network()
priceController=200
#To read the file and import the objects
with open(filename) as f:
   # Read the file contents and generate a list with each line
   lines = f.readlines()

# Iterate each line
Lkns=[]
Ctrs=[]
Swts=[]
for line in lines:
    if re.search(r'^L.*', line):
        v=line.strip('\n\r')
        z= v.split(',')
        Lkns.append(z)
    elif re.search(r'^C.*', line):
        v=line.strip('\n\r')#Take off Feed line
        z= v.split(',')#Split by ","
        Ctrs.append(z)#Build list
    elif re.search(r'^S.*', line):
        #print(line)
        v=line.strip('\n\r')#Take off Feed line
        z= v.split(',')#Split by ","
        Swts.append(z)#Build list
for pointer in Lkns:
    idl=pointer[0]
    lt=pointer[2]
    pr=pointer[3]
    cr=pointer[4]
    sc=pointer[5]
    di=pointer[6]
    test=Link(idl,lt,pr,cr,sc,di)
    mynet.addLink(test)
for pointer in Ctrs:
    Idc=pointer[0]
    Din=pointer[1]
    #Pcr=pointer[2] #Change
    Pcr=priceController
    Sta=pointer[3]
    test=Controller(Idc, Din,  priceController, Sta)
    mynet.addController(test)
for pointer in Swts:
    IdS=pointer[0]
    FlS=pointer[1]
    PrD=pointer[2]
    test =Switch(IdS,FlS,PrD)
    mynet.addSwitch(test)
#priceController=200
#C20 = Controller("C20", "S20",  priceController, False)
#mynet.addController(C20)

mynet.linkActivation()
print(str(mynet.calculateTotalCost()))
#print("El valor: " + str(mynet.randomSolution(0.2)))
x,y=mynet.randomSolution(0.2)
print("La Sumatoria de Links para LC es: " + str(x))
print("El costo Inter-controladores para LC es: " + str(y))
#mynet.randomSolution(0.2)
z=mynet.calculateControllerCost()
print("El costo por controladores es: " + str(z))
w=x+y+z
print("El costo para la solución LC es: "+str(w))

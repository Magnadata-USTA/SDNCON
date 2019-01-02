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
            temp+= int(switch.getFlowSetupRequest()) #Sumatoria total de peticiones de todos los switches que tiene el controlador
        self.receivedRequest = temp
        return self.receivedRequest
        
    def getTotalProcessingDelay(self): #Get: Obtiene datos, devolver datos, procesa         
        self.totalProcessingDelay = (self.getReceivedRequest()/1600000)*int(self.deployedIn.getProcessingDelay())                
        return self.totalProcessingDelay
  
class Switch():
    def __init__(self,idSwitch,flowSetupRequest,processingDelay):
        self.idSwitch=idSwitch
        self.flowSetupRequest=int(flowSetupRequest) 
        self.processingDelay=int(processingDelay)

    def getFlowSetupRequest(self):
        return self.flowSetupRequest        
        
    def getProcessingDelay(self):
        #Time to process 1.6 M of flow setup request in ms.
        return self.processingDelay    
    
    def getIdSwitch(self):
        return self.idSwitch
    
class Network():
    def __init__(self):
        self.controllerCost = 0 #Costo de todos los controladores de la red
        self.controllerSWLinkCost = 0  #Costo total de los enlaces de controlador a Switch
        self.intercontrollerLinkCost = 0
        self.totalCost = 0
        self.switches= []    
        self.controllers= []    
        self.links = []
    
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
    
    def eraseInfoController(self, controller):
        #self.controllers.append(controller)
        #print(self.controllers[controller])
        self.controllers[controller].controlledSW=[]
        self.controllers[controller].state = "False"
        self.controllers[controller].receivedRequest = 0
        self.controllers[controller].totalProcessingDelay = 0
        #print(self.controllers[controller])
        
    def chController(self, controller,controller2):
        #print(self.controllers[controller])
        #print(self.controllers[controller2])
        self.controllers[controller2].controlledSW=self.controllers[controller].controlledSW
        self.controllers[controller].controlledSW=[]
        self.controllers[controller].state = "False"
        self.controllers[controller2].state = "True"
        self.controllers[controller].receivedRequest = 0
        self.controllers[controller].totalProcessingDelay = 0
        self.controllers[controller2].getTotalProcessingDelay()
        #print(self.controllers[controller])
        #print(self.controllers[controller2])
        
    def calculateLP(self,activecontrollers,LLinks,List_IntercotrollerCost,maxFlowSetupLatency,maxInterControllerLatency,status):
        #To know latency by each Controller and Processing Delay
        status=0
        for w in activecontrollers:#Go for every Controller to look for Latency in each Link
            AcumL=0
            for i in LLinks:#Go for each element in the list
                z=i.split('_')#Split by "_"
                Cid="C"+z[1]
                Cid2=z[0]
                Cid2="S"+Cid2[2:]
                if (Cid==w.idController):#looking for w controller
                    for j in self.links:
                        if (j.idLink==i):#compare both lists
                            AcumT=0
                            #AcumL+=float(j.latency)
                            AcumL=float(j.latency)
                            AcumL=AcumL*2
                            #print("La latencia para "+str(w.idController)+"-"+str(Cid2)+ " (x2) es: "+str(j.latency)+" ms")
                            AcumT=AcumL+w.getTotalProcessingDelay()
                            print("2L + P para "+str(w.idController)+"-"+str(Cid2)+ " es: "+str(AcumT)+" ms")
                            if (AcumT >= maxFlowSetupLatency):
                                print("La pareja "+str(w.idController)+"-"+str(Cid2)+ " no cumple con el Constrain")
                                status=1
 
        #2.5 Max. Latency Intercontroller (Constrain)
        print("\n"+"Latencia Inter-Controller")
        if (len(activecontrollers) > 1):
            print(*List_IntercotrollerCost) #keep in mind for intercontroller Latency
            AcumL=0
            for w in activecontrollers[:-1]:#Go for every Controller to look for Latency in each Link
                #AcumL=0
                for i in List_IntercotrollerCost:#Go for each element in the list
                    z=i.split('_')#Split by "_"
                    Cid=z[0]
                    Cid="C"+Cid[2:]
                    Cid2="C"+z[1]
                    if (Cid==w.idController):#looking for w controller
                        for j in self.links:
                            if (j.idLink==i):#compare both lists
                                #AcumL+=float(j.latency)
                                AcumL=float(j.latency)
                                print("La latencia para "+str(w.idController)+"-"+str(Cid2)+ " es: "+str(j.latency)+" ms")
                                if (AcumL >= maxInterControllerLatency):
                                    print("La pareja "+str(w.idController)+"-"+str(Cid2)+ " no cumple con el Constrain")
                                    status=1
        else:
                for w in activecontrollers:
                    print("La latencia Inter-controller para "+str(w.idController)+" es: "+"0"+" ms")
                    AcumL=0
        print("La latencia Intercontroller es: "+str(AcumL)+" ms")
        return(status)
        
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
            
    def calculateLinks(self,zip_list,activecontrollers,ActiveControllers,galf):
        LLinks=[]
        #print("hola")
        for start,target in zip_list:
            startt='"'+start+'"'
            targett='"'+target+'"'
            targett= targett.replace('C', 'S')
            for j in self.links:
                if ((j.getsourceId()==startt) & (j.getdestinationId()==targett) & (j.getState()==True)):
                    Providers=j.idLink
                    Providers=Providers[0:2]
                    LLinks.append(Providers+str(start.lstrip('S'))+"_"+str(target.lstrip('C'))) #Sacarlo de For si hay problemas en Providers
            
            #x=randint(0,2)
            if (galf==0):
                for controller in activecontrollers:
                    if (controller.idController==target):
                        #print(t.idController)
                        keeperC=controller
                        p=start.lstrip('S')
                        p=int(p)
                        keeperC.addControlledSW(self.switches[p])
                    
        IntercontrollerCostLC = 0;
        List_IntercotrollerCost = []
        Holder = len(ActiveControllers)
        #Providers=["LC","LM","LT"]
        if (Holder > 1):
            print("We have Length: " + str(Holder))
            List_IntercotrollerCost = []
            New=()
            SelfSC=[]
            for w in range(Holder):
                for y in ActiveControllers:
                    flag=0
                    if(str(ActiveControllers[w].lstrip('C')) != str(y.lstrip('C'))):#cambiar esta linea cuando se cambie el formato
                        
                        #x=randint(0,2)
                        r=str(ActiveControllers[w].lstrip('C'))
                        t=str(y.lstrip('C'))
                        startt='"S'+r+'"'
                        targett='"S'+t+'"'
                        #targett= targett.replace('C', 'S')
                        for j in self.links:
                            if ((j.getsourceId()==startt) & (j.getdestinationId()==targett) & (j.getState()==True)):
                                Providers=j.idLink
                                Providers=Providers[0:2]
                        
                        New=(r,t)
                        SelfSC.append(New)
                        #It is Needed to know which links were connected to skip inverse
                        for u,v in SelfSC:
                            if ((u==t) & (v==r)):
                                flag=1
                        if (flag==0):        
                            List_IntercotrollerCost.append(Providers+str(ActiveControllers[w].lstrip('C'))+"_"+str(y.lstrip('C')))
                            New=(t,r)
                            SelfSC.append(New)
                            flag=0
            #print(*List_IntercotrollerCost) #descomentar para ver la lista de links-intercontrollers
        #Now, let's calculate Link costs
        Link_Cost=0
        for w in LLinks:
            for y in self.links:
                if (y.idLink==w):
                    #print("encontrado"+str(y.idLink)+str(y.price))
                    Link_Cost+=y.price
         
        #We have to calculate Intercontroller Cost (Links)
        #We got active controller in ActiveControllers variable, let's Do it
        IntercontrollerCostLC = 0
        for w in List_IntercotrollerCost:
            for y in self.links:
                if (y.idLink==w):
                    IntercontrollerCostLC+=y.price
        return (LLinks,List_IntercotrollerCost,Link_Cost,IntercontrollerCostLC)         
    #def randomSolution(self, p_controllers,maxFlowSetupLatency, maxInterControllerLatency):
    def randomSolution(self, p_controllers,maxFlowSetupLatency,maxInterControllerLatency,status): 
        SDNisValid = False
        #1.Activate controllers
        #1.1 Activa controllers randomly
        for controller in self.controllers:
            if(uniform(0, 1)<p_controllers):
                controller.setState(True)
                #controller.
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
            #controller.addControlledSW(self.switches[0])
            #print(controller)
            print(controller.idController)
       
        ActiveSwitches=[]
        for Sws in self.switches:            
            #print(Sws.idSwitch)
            ActiveSwitches.append(Sws.idSwitch)
        print (*ActiveSwitches)

        #To assing Cn Sn rule
        New=()
        SelfSC=[]
        zip_list=()
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
        galf=0
        LLinks,List_IntercotrollerCost,Link_Cost,IntercontrollerCostLC=mynet.calculateLinks(zip_list,activecontrollers,ActiveControllers,galf)         
        print(LLinks) #Descomentar para ver la asignación Controller-Switch
        
        #2.4 To know latency by each Controller and Processing Delay
        status=mynet.calculateLP(activecontrollers,LLinks,List_IntercotrollerCost,maxFlowSetupLatency,maxInterControllerLatency,status)       
        #return (Link_Cost,IntercontrollerCostLC)
        return (Link_Cost,IntercontrollerCostLC,zip_list,LLinks,List_IntercotrollerCost,status)
    
    def changeController(self,LLinks,List_IntercotrollerCost,maxFlowSetupLatency,maxInterControllerLatency,status):
        activecontrollers=[]
        unActiveControllers=[]
        for controller in self.controllers:
            #print(controller)
            if(controller.getState()==True):
                activecontrollers.append(controller)
            else:
                unActiveControllers.append(controller)
                
        #for controller in unActiveControllers:            
            #print(controller.idController)
        copyLLinks=LLinks    
        copyList_IntercotrollerCost=List_IntercotrollerCost
        #let's choose one active controller randomly from active controller list         
        lnt=len(activecontrollers)
        valueActive=randint(0,lnt-1)
        print("Se cambiara este controllador :"+activecontrollers[valueActive].idController)
        OriValue=activecontrollers[valueActive].idController #C_xold
        OriValue=OriValue.lstrip('C') #C_xold
        lnt=len(unActiveControllers)
        valueUnactive=randint(0,lnt-1)
        print("Por este Controllador :"+unActiveControllers[valueUnactive].idController)
        NewValue=unActiveControllers[valueUnactive].idController ##Cx_new
        NewValue=NewValue.lstrip('C')
        #print(*LLinks)
        for i in LLinks:
            #print(i)
            z=i.split('_')#Split by "_"
            Cid=z[0]
            lkn=Cid[0:2] #link
            Swt=Cid[2:] #Switch
            Cic=z[1] #Controller
            #var=lkn+OriValue+"_"+OriValue
            #print(var)
            if (i == lkn+OriValue+"_"+OriValue): #ie. LM7_7
                LLinks[LLinks.index(i)] = lkn+NewValue+"_"+NewValue
            elif(Cic == OriValue): #i.e C7 replace x C0 (LM5_7) 
                LLinks[LLinks.index(i)] = lkn+Swt+"_"+NewValue
            elif((Swt == NewValue) & (Cic == OriValue)): #ie. the same C7 replace x C0 (LT0_7)
                remove=LLinks.index(i)
                LLinks.pop(remove)
  
        print(*LLinks)
        #Now, we have to change inter-controller list
        print("\n"+"New List controllers"+"\n")
        #print(*List_IntercotrollerCost) #To know Inter-Controller List changed
        for i in List_IntercotrollerCost:
            #print(i)
            z=i.split('_')#Split by "_"
            Cid=z[0]
            lkn=Cid[0:2] #link
            Swt=Cid[2:] #Switch
            Cic=z[1] #Controller
            #var=lkn+OriValue+"_"+OriValue
            #print(var)
            if(Swt == OriValue):
                List_IntercotrollerCost[List_IntercotrollerCost.index(i)] = lkn+NewValue+"_"+Cic
            elif(Cic == OriValue):
                List_IntercotrollerCost[List_IntercotrollerCost.index(i)] = lkn+Swt+"_"+NewValue    
        print(*List_IntercotrollerCost)
        #To activate the old Controller and activate the new, Calculate 
        mynet.chController(int(OriValue),int(NewValue))
        
        status=mynet.calculateLP(activecontrollers,LLinks,List_IntercotrollerCost,maxFlowSetupLatency,maxInterControllerLatency,status)
        print("Este es el valor de status "+str(status))
        
        #Now, let's know Latency inter-controller and LS-C
        #Fisrt at all, we need to update new intercontroller acive list
        activecontrollers=[]
        unActiveControllers=[]
        for controller in self.controllers:
            #print(controller)
            if(controller.getState()==True):
                activecontrollers.append(controller)
            else:
                unActiveControllers.append(controller)
               
        #We need to check status value, due to we did change, so we have to revert it
        if status==1:
            LLinks=copyLLinks    
            List_IntercotrollerCost=copyList_IntercotrollerCost   
            mynet.chController(int(NewValue),int(OriValue))

    def changeLinks(self,zip_list,LLinks,List_IntercotrollerCost,maxFlowSetupLatency,maxInterControllerLatency,status):
        
        activecontrollers=[]
        unActiveControllers=[]
        copyLLinks=LLinks    
        copyList_IntercotrollerCost=List_IntercotrollerCost
        List_IntercotrollerCost=[]
        for controller in self.controllers:
            #print(controller)
            if(controller.getState()==True):
                activecontrollers.append(controller)
            else:
                unActiveControllers.append(controller)
        
        #To change links state
        lim_inf = 0        
        while(lim_inf < len(self.links)-3):
            hlp=lim_inf
            if(uniform(0, 1)<0.5):
                #print("entro en :" + str(hlp)+"<"+str(len(self.links)-3))
                for i in list(range(3)):
                    if (i > 0):#print (i)
                        hlp=hlp+1
                    self.links[hlp].setState(False)
                    #print(self.links[hlp].idLink)
                    #print(hlp)
                index = randint(lim_inf,lim_inf+2)
                #print(index)
                self.links[index].setState(True)
            lim_inf=lim_inf+ 3
        
        ActiveControllers=[]
        for controller in self.controllers:
            if(controller.getState()==True):
                ActiveControllers.append(controller.idController) 
        
#        for j in self.links:
#            if (j.getState()==True):
#                print(j.idLink)
        galf=1        
        LLinks,List_IntercotrollerCost,Link_Cost,IntercontrollerCostLC=mynet.calculateLinks(zip_list,activecontrollers,ActiveControllers,galf)
        print("Asignación C-S")
        print(LLinks)
        print("Intercontroller List")
        print(*List_IntercotrollerCost)  
        status=mynet.calculateLP(activecontrollers,LLinks,List_IntercotrollerCost,maxFlowSetupLatency,maxInterControllerLatency,status)
                           
        print("La Sumatoria de Links para L(C/M/T) es: " + str(Link_Cost))
        print("El costo Inter-controladores para L(C/M/T) es: " + str(IntercontrollerCostLC))
        
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

    def getsourceId(self):
        #print(self.sourceId)
        return self.sourceId
    
    def getdestinationId(self):
        #print(self.destinationId)
        return self.destinationId    

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
for pointer in Swts:
    IdS=pointer[0]
    FlS=pointer[1]
    PrD=pointer[2]
    test =Switch(IdS,FlS,PrD)
    mynet.addSwitch(test)
    
for pointer in Ctrs:
    Idc=pointer[0]
    p=Idc.lstrip('C')
    p=int(p)
    Din=mynet.switches[p]
    #Din=pointer[1]
    #Pcr=pointer[2] #Change
    Pcr=priceController
    Sta=pointer[3]
    test=Controller(Idc, Din,  priceController, Sta)
    mynet.addController(test)
    
#priceController=200
#C20 = Controller("C20", "S20",  priceController, False)
#mynet.addController(C20)

mynet.linkActivation()
print(str(mynet.calculateTotalCost()))
#print("El valor: " + str(mynet.randomSolution(0.2)))
status=1
cont=0
while(status>0):
    cont+=1
    if (cont == 1):
        x,y,zip_list,LLinks,List_IntercotrollerCost,status=mynet.randomSolution(0.2 , 80, 100,status)
        print("La Sumatoria de Links para L(C/M/T) es: " + str(x))
        print("El costo Inter-controladores para L(C/M/T) es: " + str(y))
        #mynet.randomSolution(0.2)
        z=mynet.calculateControllerCost()
        print("El costo por controladores es: " + str(z))
        w=x+y+z
        print("El costo para la solución es: "+str(w))
    else:
        #To clean Objects in mynet
        for x in range(0,len(Ctrs)):
            mynet.eraseInfoController(x)
        x,y,zip_list,LLinks,List_IntercotrollerCost,status=mynet.randomSolution(0.1 , 80, 100,status)
        print("La Sumatoria de Links para L(C/M/T) es: " + str(x))
        print("El costo Inter-controladores para L(C/M/T) es: " + str(y))
        #mynet.randomSolution(0.2)
        z=mynet.calculateControllerCost()
        print("El costo por controladores es: " + str(z))
        w=x+y+z
        print("El costo para la solución es: "+str(w))
        
#Let's change the one controller
#mynet.changeController(LLinks,List_IntercotrollerCost,40, 60,1)

#Now let's create change link 
#mynet.changeLinks(zip_list,LLinks,List_IntercotrollerCost,80, 100,1)

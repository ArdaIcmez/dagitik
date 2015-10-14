from Airline import *

def canRedeem(current,goal,pathForMiles,airlinesVisited,network) :
    if current == goal:
        pathForMiles.append(current)
        return True 
    elif current in airlinesVisited:
        return False
    else:
        airlinesVisited.append(current)
        pathForMiles.append(current)
        
        pos = -1
        index = 0
        while (pos ==-1 & index < len(network)):
            if network[index].getName == current:
                pos=index
            index+=1
        
myFile = None
try:
    myFile = open('airlines.txt','r')
except:
    print "Opening failed"
    exit
airlinesPartnersNetwork = []
pathForMiles = []
airlinesVisited = []
for myLine in myFile:
    print myLine
    airlineNames = myLine.split(',')
    airlinesPartnersNetwork.append(Airline(airlineNames))
start = raw_input("Enter airline miles are on: ")
goal = raw_input("Enter goal airline: ")

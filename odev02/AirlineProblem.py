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
        if pos == -1:
            return False
        index=0
        partners = network[pos].getPartners()
        foundPath = False
        while (not foundPath & index < len(network)):
            foundPath = canRedeem(partners[index], goal, pathForMiles, airlinesVisited, network)
            index+=1
        if not foundPath:
            pathForMiles.remove(len(pathForMiles)-1)
        return foundPath
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

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
        while (pos ==-1 and index < len(network)): 
            if (network[index].getName() == current):
                pos=index
            index+=1
        if pos == -1:
            return False
        index=0
        partners = network[pos].getPartners()
        foundPath = False
        while (not foundPath and index < len(partners)):
            foundPath = canRedeem(partners[index], goal, pathForMiles, airlinesVisited, network)
            index+=1
        if not foundPath:
            del pathForMiles[len(pathForMiles)-1]
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
    airlineNames[-1] = airlineNames[-1].replace('\n','')
    airlinesPartnersNetwork.append(Airline(airlineNames))
start = raw_input("Enter airline miles are on: ")
goal = raw_input("Enter goal airline: ")
if canRedeem(start,goal,pathForMiles,airlinesVisited,airlinesPartnersNetwork):
    print "Path to redeem miles: ", pathForMiles
else:
    print "Cannot convert miles from " , start , " to " , goal , "."
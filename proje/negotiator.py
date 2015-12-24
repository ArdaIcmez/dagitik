__author__ = 'arda'

import sys
import threading
import socket
import Queue
import time
"""
TODO:
-UPDATER THREAD (with UPDATE_INTERVAL)    
"""
class ClientThread (threading.Thread):
    def __init__(self, name, test, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.test = test
        self.cpl = cpl
        self.cplLock = cplLock
        
    def clientParser(self, data, ip, port):
        if len(data) == 0:
            return
        if data[0:5] == "SALUT":
            cType = data[6]
            self.cplLock.acquire()
            self.cpl.append([ip,port,None,cType,"W"])
            self.cplLock.release()
        if data[0:5] == "BUBYE":
            pass
            
    def run(self):
        print "Starting "+self.name
        while True:
            
            #Check to see if there are any peers to test
            if not self.test.empty():
                print "queue ya birseyler girdi"
                ipPort = self.test.get()
                try:
                    testSocket = socket.socket()
                    testSocket.connect((str(ipPort[0]),int(ipPort[1])))
                    testSocket.send("HELLO")
                    data = testSocket.recv(1024)
                    self.clientParser(data,ipPort[0],ipPort[1])
                    testSocket.send("CLOSE")
                    testSocket.recv(1024)
                    
                #Did not receive a response or something went wrong, do nothing
                except:
                    pass
                    
class ServerThread (threading.Thread):
    def __init__(self, name, cSocket, test, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.test = test
        self.cpl = cpl
        self.cplLock = cplLock
        self.clIp = ""
        self.clPort = 0
        self.isActive = True
    def serverParser(self, data):
        if len(data) == 0:
            return
        if data[0:5] == "CLOSE":
            self.cSocket.send("BUBYE")
            print "Server ",self.name , "closing"
            self.isActive = False
        if data[0:5] == "HELLO":
            self.cSocket.send("SALUT N")
            return
        if data[0:5] == "REGME":
            ipPort = data[6:].split(':')
            print "REGME ile gelen ip port ikilisi : ", ipPort
            
            #ip : port has errors 
            if((len(ipPort[0]))<5):
                self.cSocket.send("REGER")
                return
            
            #holding client ip and port information for GETNL purposes
            self.clIp=str(ipPort[0])
            self.clPort=int(ipPort[1])
            
            #check to see if peer exists in CONNECT_POINT_LIST
            self.cplLock.acquire()
            for i in range(0,len(self.cpl)):
                if (self.cpl[i][0] == ipPort[0] and self.cpl[i][1] == ipPort[1]):
                    self.cpl[i][2] = time.ctime()
                    self.cpl[i][4] = "S"
                    self.cplLock.release()
                    self.cSocket.send("REGOK "+ str(self.cpl[i][2]))
                    print "Listede buldum"
                    return
            self.cplLock.release()
            
            #Peer does not exist in CPL, time to test
            self.cSocket.send("REGWA")
            self.test.put((ipPort[0],ipPort[1]))
            return
        
        if data[0:5] == "GETNL":
            
            #test to see if peer is tested before
            self.cplLock.acquire()
            for item in self.cpl:
                print item
            print self.clIp, self.clPort
            if not [peer for peer in self.cpl if (peer[0] == self.clIp and str(peer[1])==str(self.clPort) and peer[4]=="S")]:
                
                self.cSocket.send("REGER")
                return
            self.cplLock.release()
            
            myConnections = ""
            if(len(data)>6):
                limit = int(data[6:])
                for i in range(0,limit):
                    if(i>len(self.cpl)):
                        break
                    if(self.cpl[i][4]=="S"):
                        myConnections += str(item[0])+":"+str(item[1])+":"+str(item[2])+":"+str(item[3])+"\n"
            else:
                for item in self.cpl:
                    if(item[4]=="S"):
                        myConnections += str(item[0])+":"+str(item[1])+":"+str(item[2])+":"+str(item[3])+"\n"
            self.cSocket.send("NLIST BEGIN\n"+myConnections+"NLIST END")
            
        else:
            self.cSocket.send("CMDER")
    
    def run(self):
        print "Starting "+self.name
        while self.isActive:
            data = self.cSocket.recv(1024)
            self.serverParser(data)
        
#UPDATE_INVERVAL kadar zaman gecmis mi kontrolu yapan thread
class TimeThread (threading.Thread):
    def __init__(self, name,flagQueue,timeQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.timeQueue = timeQueue
        self.flagQueue = flagQueue
    def run(self):
        print "Starting "+self.name
        while True:
            if not self.timeQueue.empty():                
                timeFlag = self.timeQueue.get()
                if timeFlag == 1:
                    time.sleep(UPDATE_INVERVAL)
                    self.flagQueue.put(2)
                elif timeFlag == -1:
                    return

def main():
    
    global UPDATE_INTERVAL
    UPDATE_INTERVAL = 60*10
    nlsize = 50
    
    #Lists are not thread safe, need to add lock
    cplLock = threading.Lock()
    
    #cplElement = (ip,port,time,type,status), if Status = S == send
    conPointList = []
    
    #Opening the negotiator socket for server
    host = "localhost"
    port = 11111
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    
    #initialise CPL with itself
    conPointList.append([host,port,time.ctime(),"N","S"])
    
    threadQueue = Queue.Queue()
    
    #For client to test connections
    testQueue = Queue.Queue()
    
    threadCounter = 1
    
    clientThread = ClientThread("Negotiator Client", testQueue,conPointList,cplLock)
    clientThread.setDaemon(True)
    clientThread.start()
    while True:
        c, addr = s.accept()
        serverThread = ServerThread("NegotiatorSubserver-"+`threadCounter`, c, testQueue,conPointList,cplLock)
        serverThread.setDaemon(True)
        serverThread.start()

        threadCounter+=1
        
if __name__ == '__main__':
    main()
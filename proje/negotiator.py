import sys
import threading
import socket
import Queue
import time
class ClientThread (threading.Thread):
    def __init__(self, name, socket, test, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.socket = socket
        self.test = test
        self.cpl = cpl
        self.cplLock = cplLock
        self.timeQueue = timeQueue
        
    def clientParser(self, data, addr):
        if len(data) == 0:
            return
        if data[0:5] == "SALUT":
            self.cplLock.acquire()
            self.cpl.append((self.addr[0],self.addr[1],time.ctime(),cType,"W"))
            self.cplLock.release()
        if data[0:5] == "BUBYE":
            pass
        else:
            self.cSocket.send("CMDER")
            
    def run(self):
        print "Starting "+self.name
        while True:
            
            #Server, Queue yu doldurdu
            if not self.test.empty():
                ipPort = self.test.get()
                try:
                    pass
                except:
                    pass
                    except:
                        #self.socket.send("CLOSE")
                        #self.socket.recv(1024)
                        self.cplLock.acquire()
                        for i in range(0,len(self.cpl)):
                            if self.cpl[i][0] == self.addr[0]:
                                del self.cpl[i]
                                break
                        self.cplLock.release()
                            
                        #Server thread ini ve time thread ini kapanma konusunda bilgilendir
                        self.flag.put(-1)
                        self.timeQueue.put(-1)
                        return
                    
class ServerThread (threading.Thread):
    def __init__(self, name, socket, cSocket, test, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.test = test
        self.cpl = cpl
        self.cplLock = cplLock
        
    def serverParser(self, data):
        if len(data) == 0:
            return
        if data[0:5] == "REGME":
            ipPort = data[6:].split(':')
            
            #ip : port has errors 
            if((len(ipPort[1])+len(ipPort[0]))<12):
                self.cSocket.send("REGER")
                return
            
            #check to see if peer exists in CONNECT_POINT_LIST
            cplLock.acquire()
            for i in range(0,len(self.cpl)):
                if (self.cpl[i][0] == ipPort[0] and self.cpl[i][1] == ipPort[1]):
                    self.cSocket.send("REGOK "+self.cpl[i][2])
                    self.cpl[i][3] = "S"
                    cplLock.release()
                    return
            cplLock.release()
            
            #Peer does not exist in CPL, time to test
            self.cSocket.send("REGWA")
            self.test.put((ipPort[0],ipPort[1]))
            return
        if data[0:5] == "GETNL":
            for item in cpl:
                myConnections = str(item[0])+":"+str(item[1])+":"+str(item[2])+":"+str(item[3])+"\n"
            self.cSocket.send("NLIST BEGIN\n"+myConnections+"NLIST END")
            
        else:
            self.cSocket.send("CMDER")
    
    def run(self):
        print "Starting "+self.name
        while True:
            pass
        time.sleep(.01)
        
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
    
    #Opening the negotiator socket
    host = "localhost"
    port = 11112
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    
    
    threadQueue = Queue.Queue()
    
    #For client to test connections
    testQueue = Queue.Queue()
    
    threadCounter = 1
    
    clientThread = ClientThread("NegotiatorClient", s, testQueue,conPointList,cplLock)
    while True:
        print "Waiting connection"
        c, addr = s.accept()
        
        serverThread = ServerThread("NegotiatorSubserver-"+`threadCounter`, socket, c,testQueue,conPointList,cplLock)
        timeThread = TimeThread("NegotiatorTimer-"+`threadCounter`,flagQueue ,timeQueue)
        serverThread.setDaemon(True)
        clientThread.setDaemon(True)
        timeThread.setDaemon(True)
        serverThread.start()
        clientThread.start()
        timeThread.start()
        threadCounter+=1
        
if __name__ == '__main__':
    main()
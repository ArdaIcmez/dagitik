import sys
import threading
import socket
import Queue
import time
class ClientThread (threading.Thread):
    def __init__(self, name, socket, addr, flag, cpl, cplLock, timeQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.socket = socket
        self.flag = flag
        self.cpl = cpl
        self.addr = addr
        self.cplLock = cplLock
        self.timeQueue = timeQueue
        self.exitFlag=0
    def clientParser(self, data):
        if len(data) == 0:
            return
        if data[0:5] == "SALUT":
            return data[6]
        if data[0:5] == "BUBYE":
            pass
        
    def run(self):
        print "Starting "+self.name
        while not exitFlag:
            if not self.flag.empty():
                myFlag = self.flag.get()
                if myFlag==1:
                    try:
                        self.socket.send("HELLO")
                        self.socket.settimeout(20)
                        data = self.socket.recv(1024)
                        cType = self.clientParser(data)
                        self.cplLock.acquire()
                        self.cpl.append((self.addr[0],self.addr[1],time.ctime(),cType,"W"))
                        self.cplLock.release()
                        self.timeQueue.put(1)
                    except:
                        print "Client side registering failed"
                if myFlag ==2:
                    self.timeQueue.put(0)
                    try:
                        self.socket.send("HELLO")
                        self.socket.settimeout(20)
                        data = self.socket.recv(1024)
                        cType = self.clientParser(data)
                        self.cplLock.acquire()
                        for i in range(0,len(self.cpl)):
                            if self.cpl[i][0] == self.addr[0]:
                                self.cpl[i][2] = time.ctime()
                                break
                        self.cplLock.release()
                        self.timeQueue.put(1)
                    except:
                        
class ServerThread (threading.Thread):
    def __init__(self, name, socket, flag, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.socket = socket
        self.flag = flag
        self.cpl = cpl
        self.cplLock = cplLock
    def run(self):
        print "Starting "+self.name
        while True:
            pass
        time.sleep(.01)
        
class TimeThread (threading.Thread):
    def __init__(self, name, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.socket = socket
        self.flag = flag
        self.isConnected = False
    def run(self):
        print "Starting "+self.name
        while True:
            pass
        time.sleep(.01)

def main():
    # the queue should contain no more than maxSize elements
    global UPDATE_INTERVAL
    UPDATE_INTERVAL = 1000*60*10
    nlsize = 50
    cplLock = threading.Lock()
    conPointList = []
    host = "localhost"
    port = 11111
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    threadQueue = Queue.Queue()
    threadCounter = 1
    while True:
        print "Waiting connection"
        c, addr = s.accept()
        flagQueue = Queue.Queue(3)
        timeQueue = Queue.Queue(3)
        serverThread = ServerThread("NegotiatorSubserver-"+`threadCounter`,c,flagQueue,conPointList,cplLock)
        clientThread = ClientThread("NegotiatorSubclient-"+`threadCounter`,c,addr,flagQueue,conPointList,cplLock,timeQueue)
        timeThread = TimeThread("NegotiatorTimer-"+`threadCounter`,timeQueue)
        serverThread.setDeamon(true)
        clientThread.setDeamon(true)
        timeThread.setDeamon(true)
        serverThread.start()
        clientThread.start()
        threadCounter+=1
        
if __name__ == '__main__':
    main()
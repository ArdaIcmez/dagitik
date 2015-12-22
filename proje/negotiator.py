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
        
    def clientParser(self, data):
        if len(data) == 0:
            return
        if data[0:5] == "SALUT":
            return str(data[6])
        else:
            self.socket.send("CMDER")
    def run(self):
        print "Starting "+self.name
        while True:
            
            #Server, Queue yu doldurdu
            if not self.flag.empty():
                myFlag = self.flag.get()
                
                #Peer'dan REGME geldi, kontrol vakti
                if myFlag == 1:
                    try:
                        self.socket.send("HELLO")
                        self.socket.settimeout(20)
                        data = self.socket.recv(1024)
                        cType = self.clientParser(str(data))
                        self.cplLock.acquire()
                        self.cpl.append((self.addr[0],self.addr[1],time.ctime(),cType,"W"))
                        self.cplLock.release()
                        self.timeQueue.put(1)
                    except:
                        print "Client side registering failed"
                        
                #UPDATE_INTERVAL kadar zaman gecti, kontrol vakti
                if myFlag == 2:
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
                            
                    #Cevap gelirken hata olustu veya zaman asimina ugradi(20s), atma zamani
                    
        #Mantiken bir negotiator un peer ile baglantiyi kopartmak istedigimiz durum = baglanamadigimiz durum
        #Bunun icin CLOSE protokolunu gondermeyi gerektirecek bir durum var midir bilemiyorum.
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
    # the queue should contain no more than maxSize elements
    global UPDATE_INTERVAL
    UPDATE_INTERVAL = 60*10
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
        timeThread = TimeThread("NegotiatorTimer-"+`threadCounter`,flagQueue ,timeQueue)
        serverThread.setDeamon(true)
        clientThread.setDeamon(true)
        timeThread.setDeamon(true)
        serverThread.start()
        clientThread.start()
        threadCounter+=1
        
if __name__ == '__main__':
    main()
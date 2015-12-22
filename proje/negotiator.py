import sys
import threading
import Queue
import numpy as np
import time
import math
class ClientThread (threading.Thread):
    def __init__(self, name, socket, test, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.socket = socket
        self.test = test
        self.cpl = cpl
        self.cplLock = cplLock
    def run(self):
        print ": Starting Negotiator Client."
        while True:
            pass
        time.sleep(.01)
        
class ServerThread (threading.Thread):
    def __init__(self, name, socket, test, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.socket = socket
        self.test = test
        self.cpl = cpl
        self.cplLock = cplLock
    def run(self):
        print ": Starting Negotiator Server."
        while True:
            c,adr
        time.sleep(.01)

def main():
    # the queue should contain no more than maxSize elements
    UPDATE_INTERVAL = 1000*60*10
    nlsize = 50
    cplLock = threading.Lock()
    conPointList = {}
    testQueue = Queue.Queue()
    host = "localhost"
    port = 11111
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    serverThread = ServerThread("NegServer",s,testQueue,conPointList,cplLock)
    clientThread = ClientThread("NegClient",s,testQueue,conPointList,cplLock)
    serverThread.start()
    clientThread.start()
    for a in range(0,numThreads):
        workQueue.put("END")

    for thread in workThreads:
        thread.join()

if __name__ == '__main__':
    main()
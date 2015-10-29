import random as rm
import socket,sys
import threading
import time
class myThread (threading.Thread):
    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
    def run(self):
        exitFlag = 0
        while not exitFlag:
            try:
                self.clientSocket.settimeout(rm.randint(8,20))
                msgRecieved = self.clientSocket.recv(1024)
                if msgRecieved.upper() == "BALTAZOR":
                    exitFlag=1
                    self.clientSocket.send("Don't cry because it's over. Smile because it happened.")
                else:
                    myMsg = "Message Recieved, " + ''.join(str(self.clientAddr))
                    self.clientSocket.send(myMsg)
            except:
                localTime = "Hello, current time is :" + time.asctime( time.localtime(time.time()) )
                self.clientSocket.send(localTime)
        print "thread closed", self.clientAddr
        return
s = socket.socket()
host = "localhost"
port = 12345
s.bind((host, port))
s.listen(5)
threadCounter = 0
threadList = []
while True:
    print "Waiting for connection"
    c, addr = s.accept()
    print 'Got a connection from ', addr
    threadCounter += 1
    threadList.append(c)
    thread = myThread(threadCounter, c, addr)
    thread.start()
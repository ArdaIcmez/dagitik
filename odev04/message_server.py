#author : Arda Icmez
#date : 29.10.2015
import random as rm
import socket,sys
import threading
import time
import signal
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
                self.clientSocket.settimeout(rm.randint(3,7))#could also use another thread to send the time
                msgRecieved = self.clientSocket.recv(1024)
                if msgRecieved.upper() == "BALTAZOR":
                    exitFlag=1
                    #Server saying goodbye to the thread, kind of a handshake.
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
threadList = [] # For the next homework, ignore for this one.
while True:
    print "Waiting for connection"
    c, addr = s.accept()
    print 'Got a connection from ', addr
    threadCounter += 1
    threadList.append(c)
    thread = myThread(threadCounter, c, addr)
    thread.start()
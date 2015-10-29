import random,socket,sys
import time as tm
class myThread (threading.Thread):
    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
    self.threadID = threadID
    self.clientSocket = clientSocket
    self.clientAddr = clientAddr
    def run(self):
        self.clientSocket.settimeout(randint(8,20))
        self.clientSocket.recv(1024)
        print tm.localtime()

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
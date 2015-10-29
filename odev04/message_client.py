import socket
import threading
import random
global exitFlag
exitFlag=0
class readThread (threading.Thread):
    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
    def run(self):
        readFunct(self)
class writeThread (threading.Thread):
    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
    def run(self):
        writeFunct(self)
        
def readFunct(myThread):
    global exitFlag
    while not exitFlag:
        print myThread.serverSocket.recv(1024)
    print "Closing read"
    
def writeFunct(myThread):
    global exitFlag
    while not exitFlag:
        msgToSend = raw_input()
        print msgToSend , "HAHA"
        myThread.serverSocket.send(msgToSend)
        if (msgToSend.upper() == "END"):
            exitFlag = 1
    print "Closing write"
    
s = socket.socket()
host = "127.0.0.1"
port = 12345
s.connect((host, port))

rThread = readThread(s)
rThread.start()
wThread = writeThread(s)
wThread.start()
rThread.join()
wThread.join()
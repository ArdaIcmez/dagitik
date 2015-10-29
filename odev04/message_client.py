#author : Arda Icmez
#date : 29.10.2015
import socket
import threading
import random
global exitFlag
exitFlag=0
class readThread (threading.Thread):
    """
        Thread instance class for reading the message sent from the server
    """
    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
    def run(self):
        readFunct(self)
class writeThread (threading.Thread):
    """
        Thread instance class for writing the message and sending it to the server
    """
    def __init__(self, serverSocket):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
    def run(self):
        writeFunct(self)
        
def readFunct(myThread):
    """
        Read function designed for readThread class
        @myThread thread variable
    """
    global exitFlag
    while not exitFlag:
        print myThread.serverSocket.recv(1024)
    
def writeFunct(myThread):
    """
        Write function designed for readThread class
        @myThread thread variable
    """
    global exitFlag
    while not exitFlag:
        msgToSend = raw_input()
        myThread.serverSocket.send(msgToSend)
        if (msgToSend.upper() == "BALTAZOR"): # Exit message
            exitFlag = 1
    
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
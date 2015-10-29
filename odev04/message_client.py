import socket
import threading
import random

class readThread (threading.Thread):
    def __init__(self, serverSocket,exitFlag):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
        self.exitFlag = exitFlag
    def run(self):
        while self.exitFlag != 1:
            print self.serverSocket.recv(1024)
        print "Closing read"
class writeThread (threading.Thread):
    def __init__(self, serverSocket,exitFlag):
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
        self.exitFlag = exitFlag
    def run(self):
        while self.exitFlag != 1:
            msgToSend = raw_input()
            print msgToSend , "HAHA"
            self.serverSocket.send(msgToSend)
            if (msgToSend.upper() == "END"):
                exitFlag = 1
        print "Closing write"
s = socket.socket()
host = "127.0.0.1"
port = 12345
s.connect((host, port))
global exitFlag
exitFlag=0

rThread = readThread(s,exitFlag)
rThread.start()
wThread = writeThread(s,exitFlag)
wThread.start()
rThread.join()
wThread.join()
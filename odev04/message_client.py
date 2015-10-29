import socket
import threading
import random
class readThread (threading.Thread):
    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
    self.threadID = threadID
    self.clientSocket = clientSocket
    self.clientAddr = clientAddr
    def run(self):
        pass
class writeThread (threading.Thread):
    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
    self.threadID = threadID
    self.clientSocket = clientSocket
    self.clientAddr = clientAddr
    def run(self):
        pass
s = socket.socket()
host = "127.0.0.1"
port = 12345
s.connect((host, port))
...
...
...
rThread = readThread(...)
rThread.start()
wThread = writeThread(...)
wThread.start()
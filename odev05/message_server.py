import Queue
import time
import socket
import sys
import threading
class WriteThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
    def run(self):
        exitFlag = 0
        self.lQueue.put("Starting " + self.name)
        while not exitFlag:
            if self.tQueue.qsize() > 0:
                queue_message = self.threadQueue.get()
                
                # gonderilen ozel mesajsa
                if queue_message[0]:
                    message_to_send = "MSG " + queue_message[2]
                    
                # genel mesajsa
                elif queue_message[1]:
                    message_to_send = "SAY " + queue_message[2]
                    
                # hicbiri degilse sistem mesajidir
                else:
                    if queue_message[2][0:3] == "BYE":
                        exitFlag=1
                    message_to_send = queue_message[2]
                    
                try:
                    self.cSocket.send(message_to_send)
                except socket.error:
                    self.cSocket.close()
                    break
        try:
            self.cSocket.close()
        except:
            pass
        self.lQueue.put("Exiting " + self.name)
        
class ReadThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.fihrist = fihrist
        self.tQueue = threadQueue
    def parser(self, data):
        global queueLock
        data = data.strip('\n')
        
        # henuz login olmadiysa
        if not self.nickname and not data[0:3] == "USR":
            response  = "ERL"
            self.threadQueue.put((None,None,response))
            return 0
        
        if data[0:3] == "USR":
            nickname = data[4:]
            
            # kullanici yoksa
            if nickname not in self.fihrist.keys():
                self.nickname = nickname
                response = "HEL " + nickname
                self.threadQueue.put((None,None,response))
                
                # fihristi guncelle
                self.fihrist[nickname] = self.tQueue
                
                # tell users that another person has joined to chat
                queueLock.acquire()
                for key in self.fihrist.keys():
                    self.fihrist[key].put((None,None,"SYS "+self.nickname+" has joined the chat"))
                queueLock.release()
                
                self.lQueue.put(self.nickname + " has joined.")
                return 0
            
            else:
                # kullanici reddedilecek
                response = "REJ " + nickname
                self.threadQueue.put((None,None,response))
                return 1
            
        elif data[0:3] == "QUI":
            response = "BYE " + self.nickname
            self.threadQueue.put((None,None,response))
            
            # notify other users
            queueLock.acquire()
            for key in self.fihrist.keys():
                self.fihrist[key].put((None,None,"SYS "+self.nickname+" has left the chat"))
            queueLock.release()
            
            # fihristten sil
            del self.fihrist[self.nickname]
            # log gonder
            self.lQueue.put(self.nickname + " has left.")
            return 1
        
        elif data[0:3] == "LSQ":
            response = "LSA "
            
            for key in sorted(self.fihrist.keys()):
                response += key+":"
                
            response = response[:-1]
            self.threadQueue.put((None,None,response))
            return 0
        
        elif data[0:3] == "TIC":
            response = "BALTAZOR"
            self.csend(response)
            return 0
        
        elif data[0:3] == "SAY":
            response = "SOK"
            self.threadQueue.put((None,None,response))
            messageAll = data[4:]
            
            queueLock.acquire()
            for key in self.fihrist.keys():
                self.fihrist[key].put((None,self.nickname,messageAll))
            queueLock.release()
            
            return 0
        
        elif data[0:3] == "MSG":
            restMessage = data[4:].split(':',1)
            to_nickname=restMessage[0]
            message = restMessage[1]
            
            if to_nickname not in self.fihrist.keys():
                response = "MNO" + to_nickname
                
            else:
                queue_message = (to_nickname, self.nickname, message)
                
                # gonderilecek threadQueueyu fihristten alip icine yaz
                queueLock.acquire()
                self.fihrist[to_nickname].put(queue_message)
                queueLock.release()
                
                response = "MOK"
            self.threadQueue.put((None,None,response))
            return 0
        
        else:
        # bir seye uymadiysa protokol hatasi verilecek
            response = "ERR"
            self.threadQueue.put((None,None,response))
            return 0
        
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            try:
                self.cSocket.settimeout(10)
                incoming_data = self.cSocket.recv(1024)
                returnCode = parser(incoming_data)
                if returnCode:
                    return
            except:
                pass
            
        self.lQueue.put("Exiting " + self.name)
        return
class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.name = name
        self.lQueue = logQueue
    # dosyayi appendable olarak ac
        self.fid = open(logFileName,'a')
    def log(self,message):
        # gelen mesaji zamanla beraber bastir
        t = time.ctime()
        self.fid.write(t +": " + message+"\n")
        self.fid.flush()
    def run(self):
        self.log("Starting " + self.name)
        while True:
            if not self.lQueue.empty():
            # lQueue'da yeni mesaj varsa
            # self.log() metodunu cagir
                to_be_logged = self.lQueue.get()
                self.log(to_be_logged)
        self.log("Exiting" + self.name)
        self.fid.close() 

def main():
    global logLock
    global queueLock
    global fihrist
    logQueue = Queue.Queue()
    queueLock = threading.Lock()
    fihrist = {}
    threadCounter = 1
    logThread = LoggerThread("LoggerThread",logQueue,"cikti.txt")
    logThread.setDaemon(True)
    logThread.start()
    s = socket.socket()
    host = "localhost"
    port = 12345
    s.bind((host, port))
    s.listen(5)
    while True:
        logQueue.put("Waiting for connection")
        print "Waiting for connection"
        c, addr = s.accept()
        logQueue.put("Got a connection from "+ str(addr))
        print 'Got a connection from ', addr
        threadQueue = Queue.Queue()
        readThread = ReadThread("ReadingThread-"+`threadCounter`, c, addr,threadQueue,logQueue)
        writeThread = WriteThread("WritingThread-"+`threadCounter`, c, addr,threadQueue,logQueue)
        readThread.start()
        writeThread.start()
        threadCounter+=1

if __name__ == '__main__':
    main()
    
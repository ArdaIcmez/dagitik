from multiprocessing import Queue, Array
import sys, threading
class WriteThread (threading.Thread):
    def __init__(self, name, cSocket, address, threadQueue, logQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            pass
        # burasi kuyrukta sirasi gelen mesajlari
        # gondermek icin kullanilacak
            if self.threadQueue.qsize() > 0:
                queue_message = self.threadQueue.get()
            # gonderilen ozel mesajsa
                if queue_message[0]:
                    message_to_send = "MSG " + queue_message[2]
                # genel mesajsa
                elif queue_message[1]:
                    message_to_send = "SAY " + queue_message[2]
                # hicbiri degilse sistem mesajidir
                else:
                    message_to_send = "SYS " + queue_message[2]
        self.lQueue.put("Exiting " + self.name)
        
class ReadThread (threading.Thread):
    def __init__(self, name, cSocket, address, logQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.lQueue = logQueue
        self.fihrist = fihrist
        self.tQueue = threadQueue
    def csend(self,response):
        self.cSocket.send(response)
    def parser(self, data):
        data = data.strip('\n')
        # henuz login olmadiysa
        if not self.nickname and not data[0:3] == "USR":
            response  = "ERL"
            self.csend(response)
            return 0
        """if data[3] != " ":
            response = "ERR"
            self.csend(response)
            return 0"""
        if data[0:3] == "USR":
            nickname = data[4:]
            # kullanici yoksa
            if nickname not in self.fihrist.keys():
                self.nickname = nickname
                response = "HEL " + nickname
                self.csend(response)
                # fihristi guncelle
                self.fihrist[nickname] = self.tQueue
                # tell users that another person has joined to chat
                for key in self.fihrist.keys():
                    self.fihrist[key].put((None,None,self.nickname+" has joined the chat"))
                self.lQueue.put(self.nickname + " has joined.")
                return 0
            else:
                # kullanici reddedilecek
                response = "REJ " + nickname
                self.csend(response)
                # baglantiyi kapat
                self.cSocket.close()
                return 1
        elif data[0:3] == "QUI":
            response = "BYE " + self.nickname
            self.csend(response)
            # notify other users
            for key in self.fihrist.keys():
                self.fihrist[key].put((None,None,self.nickname+" has left the chat"))
            # fihristten sil
            del self.fihrist[self.nickname]
            # log gonder
            self.lQueue.put(self.nickname + " has left.")
            # baglantiyi sil
            self.cSocket.close()
            return 1
        elif data[0:3] == "LSQ":
            response = "LSA "
            for key in sorted(self.fihrist.keys()):
                response += key
            self.csend(response)
        elif data[0:3] == "TIC":
            response = "BALTAZOR"
            self.csend(response)
        elif data[0:3] == "SAY":
            response = "SOK"
            self.csend(response)
            messageAll = data[4:]
            for key in self.fihrist.keys():
                self.fihrist[key].put((None,self.nickname,messageAll))
        elif data[0:3] == "MSG":
            restMessage = data[4:].split(':',1)
            to_nickname=restMessage[0]
            message = restMessage[1]
            if to_nickname not in self.fihrist.keys():
                response = "MNO"
            else:
                queue_message = (to_nickname, self.nickname, message)
                # gonderilecek threadQueueyu fihristten alip icine yaz
                self.fihrist[to_nickname].put(queue_message)
                response = "MOK"
            self.csend(response)
        else:
        # bir seye uymadiysa protokol hatasi verilecek
            response = "ERR"
            self.csend(response)
            return 0
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            incoming_data = self.cSocket.recv(1024)
            parser(incoming_data)

        self.lQueue.put("Exiting " + self.name)
class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.name = name
        self.lQueue = logQueue
    # dosyayi appendable olarak ac
        self.fid = ...
    def log(self,message):
        # gelen mesaji zamanla beraber bastir
        t = time.ctime()
        self.fid.write(t + ...)
        self.fid.flush()
    def run(self):
        self.log("Starting " + self.name)
        while True:
    ...
    ...
    ...
        # lQueue'da yeni mesaj varsa
        # self.log() metodunu cagir
        to_be_logged = ...
        self.log(to_be_logged)
        self.log("Exiting" + self.name)
        self.fid.close() 

def main():
    global logLock
    global fihrist
    logLock = threading.Lock()
    fihrist = {}

if __name__ == '__main__':
    main()
    
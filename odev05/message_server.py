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
        if ...
            message_to_send = "MSG " + ...
        # genel mesajsa
        elif queue_message[1]:
            message_to_send = "SAY " + ...
        # hicbiri degilse sistem mesajidir
        else:
            message_to_send = "SYS " + ...

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
    def parser(self, data):
        data = data.strip(' ')
        # henuz login olmadiysa
        if not self.nickname and not data[0:3] == "USR":
            response  = "ERL"
            self.csend(response)
            return 0
        # data sekli bozuksa
        #if ...
            
        if data[0:3] == "USR":
            nickname = data[4:]
            # kullanici yoksa
            if nickname not in self.fihrist.keys():
                response = "HEL " + nickname
                # fihristi guncelle
                self.fihrist.update(...)
                ...
                ...
                self.lQueue.put(self.nickname + " has joined.")
                return 0
            else:
                # kullanici reddedilecek
                response = "REJ " + nickname
                self.csend(response)
                ....
                # baglantiyi kapat
                self.csoc.close()
                return 1
        elif data[0:3] == "QUI":
            response = "BYE " + self.nickname
            ...
            ...
            # fihristten sil
            ...
            ...
            # log gonder
            ...
            # baglantiyi sil
            ...
            ...
        elif data[0:3] == "LSQ":
            response = "LSA "
            ...
            ...
        elif data[0:3] == "TIC":
        ...
        ...
        elif data[0:3] == "SAY":
        ...
        ...
        elif data[0:3] == "MSG":
        ...
        ...
        ...
            if not to_nickname in self.fihrist.keys():
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
        ...
        ...
        ...
        # burasi blocking bir recv halinde duracak
        # gelen protokol komutlari parserdan gecirilip
        # ilgili hareketler yapilacak
        ...
        ...
        queue_message = parser(incoming_data)
        ...
        ...
        # istemciye cevap h a z r l a.
        ...
        ...
        # cevap veya cevaplari gondermek zere
        # threadQueue'ya yaz
        # lock mekanizmasini unutma
        ...
        ...
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
    
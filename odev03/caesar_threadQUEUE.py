import sys, profile, threading, Queue, time

queueLock = threading.Lock()
outputLock = threading.Lock()
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class myThread (threading.Thread):
    outputOrder = 0
    def __init__(self, threadID, name, order,q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.order = order
        self.q = q
    def run(self):
        readFile(self)

def createKey():
    encryptedText = ""
    myLenght = len(alphabet)
    for i in alphabet:
        encryptedText += alphabet[(alphabet.index(i)-configParam[0])%myLenght]
    return encryptedText

def encryptBlock(text):
    encryptedText = ""
    text = text.upper()
    for i in text:
        if i in alphabet:
            encryptedText += keyAlphabet[alphabet.index(i)]
        else:
            encryptedText += i
    return encryptedText

def readFile(thread):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = thread.q.get()
            thread.order = myThread.outputOrder
            myThread.outputOrder+=1
            queueLock.release()
            data = encryptBlock(data);
            outputLock.acquire()
            myOutputFile.seek(thread.order*configParam[2])
            myOutputFile.write(data)
            outputLock.release()
        else:
            queueLock.release()
    
def main():
    global keyAlphabet
    global configParam
    global workQueue
    global exitFlag
    exitFlag=0
    configParam = []
    workQueue = Queue.Queue(10)
    if len(sys.argv) == 4:
        for e in range(1,4):
            if sys.argv[e].isdigit():
                configParam.append(int(sys.argv[e]))
            else:
                print "parameters other than filename have to be integers"
                sys.exit()
    else:
        print "usage : <filename> <shift> <numThread> <length> "
        sys.exit()
    try:
        global myInputFile,myOutputFile
        myInputFile = open('metin.txt','r')
        myOutputFile = open('crypted_'+`configParam[0]`+'_'+`configParam[1]`+'_'+`configParam[2]`+".txt",'w')
    except:
        print "Opening failed"
        sys.exit()
    
    myThreads = []
    keyAlphabet = createKey()
    
    queueLock.acquire()
    myText = myInputFile.read(configParam[2])
    while myText != "":
        workQueue.put(myText)
        myText = myInputFile.read(configParam[2])
    queueLock.release()
    
    for i in range(0,configParam[1]):
        thread = myThread(i,"Thread0"+`i`,0,workQueue)
        thread.start()
        myThreads.append(thread)
        
    while not workQueue.empty():
        pass
    
    exitFlag = 1
    for t in myThreads:
        t.join()
    myInputFile.close()
    myOutputFile.close()
if __name__ == '__main__':
    #main()
    profile.run('print main(); print')
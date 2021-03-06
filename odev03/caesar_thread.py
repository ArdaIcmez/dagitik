import sys, profile, threading

inputLock = threading.Lock()
outputLock = threading.Lock()
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class myThread (threading.Thread):
    outputOrder = 0
    def __init__(self, threadID, name, order):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.order = order
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
    while True:
        inputLock.acquire()
        myText = myInputFile.read(configParam[2])
        if myText == "":
            inputLock.release()
            break
        thread.order = myThread.outputOrder
        myThread.outputOrder+=1
        inputLock.release()
        
        myText = encryptBlock(myText);

        outputLock.acquire()
	#Waiting for other threads version is implemented in caesar_fork.py, wanted to try something different here.
        myOutputFile.seek(thread.order*configParam[2])
        myOutputFile.write(myText)
        outputLock.release()
    
def main():
    global keyAlphabet
    global configParam
    configParam = []
    
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
    for i in range(0,configParam[1]):
        thread = myThread(i,"Thread0"+`i`,0)
        thread.start()
        myThreads.append(thread)
    for t in myThreads:
        t.join()
    myInputFile.close()
    myOutputFile.close()
if __name__ == '__main__':
    #main()
    profile.run('print main(); print')

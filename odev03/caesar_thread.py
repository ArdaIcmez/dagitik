import sys, profile, threading

inputLock = threading.Lock()
outputLock = threading.Lock()
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class myThread (threading.Thread):
    outputOrder = 1 
    def __init__(self, threadID, name, order,inputfile):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.order = order
        self.inputfile = inputfile
    def run(self):
        readFile(self)

def createKey(shift,alphabet):
    encryptedText = ""
    myLenght = len(alphabet)
    for i in alphabet:
        encryptedText += alphabet[(alphabet.index(i)-shift)%myLenght]
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
        myText = thread.inputfile.read(5)
        if myText == "":
            break
        myText = encryptBlock(myText);
        thread.order = myThread.outputOrder
        myThread.outputOrder+=1
        outputLock.acquire()
        print "outpt",thread.order ,thread.threadID, myText
        outputLock.release()
    
def main():
    configParam = []
    global keyAlphabet
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
        myOutputFile = open('crypted_'+`configParam[0]`+'_'+`configParam[1]`+'_'+`configParam[2]`,'w')
    except:
        print "Opening failed"
        sys.exit()
    
    myThreads = []
    keyAlphabet = createKey(configParam[0],alphabet)
    for i in range(0,configParam[1]):
        thread = myThread(i,"Thread0"+`i`,0,myInputFile)
        thread.start()
        myThreads.append(thread)
    for t in myThreads:
        t.join()
    myFile.close()
    myOutputFile.close()
if __name__ == '__main__':
    main()
    #profile.run('print main(); print')
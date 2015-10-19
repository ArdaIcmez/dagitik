from multiprocessing import Process, Queue, Lock, Array
import sys, profile

alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

def readFile(arr,q,ql,ol):
    myOrder = 0
    print arr[0],arr[1]
    arr[0]+=1
    arr[1]+=1
    while not q.empty():
        print "whiledayim"
        ql.acquire()
        if not q.empty():
            print "ifteyim"
            data = q.get()
            myOrder = arr[0]
            arr[0]+=1
            ql.release()
            data = encryptBlock(data);
            while arr[1] != myOrder:
                print "ordergelmedi"
                pass
            ol.acquire()
            print "yazdim",data
            
            myOutputFile.write(data)
            arr[1] += 1
            ol.release()
        else:
            ql.release()
            print "else"
def main():
    global keyAlphabet
    global configParam
    global exitFlag
    queueLock = Lock()
    outputLock = Lock()
    exitFlag=0
    configParam = []
    workQueue = Queue()
    myProcesses= []
    orderArray = Array('i',[0,0])
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
    
    keyAlphabet = createKey()
    
    queueLock.acquire()
    print "aldim locku"
    myText = myInputFile.read(configParam[2])
    while myText != "":
        workQueue.put(myText)
        myText = myInputFile.read(configParam[2])
    print "biraktim"
    queueLock.release()

    for i in range(0,configParam[1]):
        process = Process(target=readFile,args=(orderArray,workQueue,queueLock,outputLock))
        process.start()
        myProcesses.append(process)
        
    
    for p in myProcesses:
        p.join()

    myInputFile.close()
    myOutputFile.close()
    
if __name__ == '__main__':
    main()
    #profile.run('print main(); print')
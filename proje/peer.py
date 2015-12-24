__author__ = 'arda'

from pyGraphics_ui import Ui_ImageProcessor
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import threading
import Queue
import numpy as np
import time
import math
import socket
"""
TODO:
-WARNING : "S" or "W" when init?
-UPDATER THREAD (with UPDATE_INTERVAL)
-UPDATER THREAD (check other peers)
-Client thread for peers
-Worker thread implementation for Server thread
-Protocol Implementation of client & server
-Somehow get GUI working with other threads
-Debug a ton
"""
def rgb2gray(rgbint):
    # convert the 32 bit color into 8-bit grayscale
    b = rgbint & 255
    g = (rgbint >> 8) & 255
    r = (rgbint >> 16) & 255
    return (r + g + b) // 3

def gray2rgb(gray):
    # convert the 8bit ro 32bit (of course the color info is lost)
    return gray * 65536 + gray * 256 + gray

class MainThread (threading.Thread):
    def __init__(self, workQueue, processedQueue, pLock, iPort):
        threading.Thread.__init__(self)
        self.pQueue = processedQueue
        self.wQueue = workQueue
        self.pLock = pLock
        self.iPort = iPort
    def run(self):
        
        print "Starting MainThread"
        cpl = []
        cplLock = threading.Lock()
        
        funcList = []
        funcList.append(["GrayScale"])
        funcList.append(["SobelFilter",255])
        
        negIp = "localhost"
        negPort = 11111
        
        ip = str(self.iPort[0])
        port = int(self.iPort[1])
        
        mySocket = socket.socket()
        mySocket.bind((ip,port))
        mySocket.listen(5)
        
        clientCount = 1
        testQueue = Queue.Queue()
        
        try:
            print "Socket actim, Client calistiriyorum"
            negClient = NegClientThread("NegClient", negIp, negPort, ip, port, cpl, cplLock)
            negClient.setDaemon(True)
            negClient.start()
        except:
            print "negclient sikinti cikardi"
            
        try:
            testerThread = TesterThread("TesterThread", cpl, cplLock, testQueue)
            testerThread.start()
        except:
            print "testerthread sikinti cikardi"
            
        while True:
            print "Main Thread waiting connection"
            c, addr = mySocket.accept()
            servThread = ServerThread("Server Thread",c,addr,self.wQueue,self.pQueue,self.pLock,cpl,cplLock,testQueue, funcList)
            servThread.start()


#For the case when 1 Peer knows the ip and tries to connect, other does not

class TesterThread (threading.Thread):
    def __init__(self, name,cpl, cplLock, testQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.cpl = cpl
        self.cplLock = cplLock
        self.testQueue = testQueue  
    def clientParser(self, data, ip, port):
        if len(data) == 0:
            return
        if data[0:5] == "SALUT":
            cType = data[6]
            self.cplLock.acquire()
            self.cpl.append([ip,port,None,cType,"W"])
            self.cplLock.release()
        if data[0:5] == "BUBYE":
            pass
    def run(self):
        print "Starting "+self.name
        while True:

            #Check to see if there are any peers to test
            if not self.testQueue.empty():
                print "queue ya birseyler girdi"
                ipPort = self.testQueue.get()
                try:
                    testSocket = socket.socket()
                    testSocket.connect((str(ipPort[0]),int(ipPort[1])))
                    testSocket.send("HELLO")
                    data = testSocket.recv(1024)
                    self.clientParser(data,ipPort[0],ipPort[1])
                    testSocket.send("CLOSE")
                    testSocket.recv(1024)
                    
                #Did not receive a response or something went wrong, do nothing
                except:
                    pass
            #if exitflag == 1:
                #return

class ServerThread (threading.Thread):
    def __init__(self, name, cSocket, addr, workQueue, processedQueue, pLock , cpl, cplLock, testQueue, funcList):
        threading.Thread.__init__(self)
        workThreads = []
        self.name = name
        self.cSocket = cSocket
        self.addr = addr
        self.workQueue = workQueue
        self.processedQueue = processedQueue
        self.pLock = pLock
        self.cpl = cpl
        self.cplLock = cplLock
        self.testQueue = testQueue
        self.funcList = funcList
        self.isActive = True
        self.clIp = ""
        self.clPort = 0
    def incomingParser(self, data):
        if data[0:5] == "HELLO":
            self.cSocket.send("SALUT P")
            return
        elif data[0:5] == "CLOSE":
            self.cSocket.send("BUBYE")
            self.isActive = False
            return
        
        if data[0:5] == "REGME":
            ipPort = data[6:].split(':')
            print "REGME ile gelen ip port ikilisi : ", ipPort
            
            #ip : port has errors 
            if((len(ipPort[0]))<5):
                self.cSocket.send("REGER")
                return
            
            self.clIp = str(ipPort[0])
            self.clPort = int(ipPort[1])
            #check to see if peer exists in CONNECT_POINT_LIST
            self.cplLock.acquire()
            for i in range(0,len(self.cpl)):
                if (self.cpl[i][0] == ipPort[0] and self.cpl[i][1] == ipPort[1]):
                    self.cpl[i][2] = time.ctime()
                    self.cpl[i][4] = "S"
                    self.cplLock.release()
                    self.cSocket.send("REGOK "+ str(self.cpl[i][2]))
                    print "Listede buldum"
                    return
            self.cplLock.release()
            
            #Peer does not exist in CPL, time to test
            self.cSocket.send("REGWA")
            self.testQueue.put((ipPort[0],ipPort[1]))
            return
        
        if data[0:5] == "GETNL":
            
            #test to see if peer is tested before
            self.cplLock.acquire()
            for item in self.cpl:
                print item
            print self.clIp, self.clPort
            if not [peer for peer in self.cpl if (peer[0] == self.clIp and str(peer[1])==str(self.clPort) and peer[4]=="S")]:  
                self.cSocket.send("REGER")
                return
            self.cplLock.release()
            
            myConnections = ""
            if(len(data)>6):
                limit = int(data[6:])
                for i in range(0,limit):
                    if(i>len(self.cpl)):
                        break
                    if(self.cpl[i][4]=="S"):
                        myConnections += str(item[0])+":"+str(item[1])+":"+str(item[2])+":"+str(item[3])+"\n"
            else:
                for item in self.cpl:
                    if(item[4]=="S"):
                        myConnections += str(item[0])+":"+str(item[1])+":"+str(item[2])+":"+str(item[3])+"\n"
            self.cSocket.send("NLIST BEGIN\n"+myConnections+"NLIST END")
            
        elif data[0:5] == "FUNLS":
            
            #test to see if peer is tested before
            self.cplLock.acquire()
            for item in self.cpl:
                print item
            print self.clIp, self.clPort
            if not [peer for peer in self.cpl if (peer[0] == self.clIp and str(peer[1])==str(self.clPort) and peer[4]=="S")]:  
                self.cSocket.send("REGER")
                return
            self.cplLock.release()
            
            myFunctions = ""
            for item in self.funcList:
                if(len(item)==1):
                    myFunctions += str(item[0])+":"+"0\n"
                else:
                    myFunctions += str(item[0]) + ":"+str(item[1])+"\n"
            
            print "Gonderdigim fonksiyonlar : ",myFunctions
            
            #Different than GETNL protocol, don't know which one is preferred
            self.cSocket.send("FUNLI BEGIN")
            self.cSocket.send(myFunctions)
            self.cSocket.send("FUNLI END")
            return
        
        elif data[0:5] == "FUNRQ":
            funcName = data[6:]
            
            #test to see if peer is tested before
            self.cplLock.acquire()
            for item in self.cpl:
                print item
            print self.clIp, self.clPort
            if not [peer for peer in self.cpl if (peer[0] == self.clIp and str(peer[1])==str(self.clPort) and peer[4]=="S")]:  
                self.cSocket.send("REGER")
                return
            self.cplLock.release()
            
            theFunc = ""
            for item in self.funcList:
                print "Aradigim func : ",funcName,"elimdeki func : ", item
                if item[0]==funcName:
                    if(len(item)==1):
                        theFunc = str(item[0])+":"+"0"
                    else:
                        theFunc = str(item[0]) + ":"+str(item[1])
                    self.cSocket.send("FUNYS "+theFunc)
                    return
            self.cSocket.send("FUNNO "+funcName)
            return
        elif data[0:5] == "EXERQ":
            restData = data[6:].split(':')
            #TODO
            return
        elif data[0:5] == "PATCH":
            restData = data[6:].split(':')
            #TODO
            return
        else:
            self.cSocket.send("CMDER")
            return
    def run(self):
        workThreads = []
        print "Starting "+self.name
        while self.isActive:
            data = self.cSocket.recv(1024)
            self.incomingParser(data)
        """for i in range(0,numThreads):
            workThreads.append(WorkerThread("WorkerThread" + str(i),
                                        workQueue,
                                        processedQueue,
                                        pLock))
            workThreads[i].start()
            
        for a in range(0,numThreads):
            self.workQueue.put("END")

        for thread in workThreads:
            thread.join()"""
        print "Kapaniyor ", self.name


#Ilk basta negotiator a baglanmak ve CPL almak icin 
class NegClientThread (threading.Thread):
    def __init__(self, name, negIp, negPort, ip, port, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.negIp = negIp
        self.negPort = negPort
        self.ip = ip
        self.port = port
        self.cpl = cpl
        self.cplLock = cplLock
        self.socket = socket.socket()
    def clientParser(self, data):
        print "Peer a gelen data :", data
        if data[0:5] == "REGWA":
            
            #Resend registration after 5s
            time.sleep(5)
            self.socket.send("REGME "+str(self.ip)+":"+str(self.port))
            data = self.socket.recv(1024)
            
        if data[0:5] == "REGOK":
            print "REGOK GELDI :D"
            
        if data[0:5] == "REGER":
            print "REGER geldi", self.name
        
        elif data[0:11] == "NLIST BEGIN":
            myList = data[12:].split('\n')
            
            #Check if last item is NLIST END
            if myList[-1] != "NLIST END":
                return
            #Remove NLIST END
            del myList[-1]
            
            self.cplLock.acquire()
            for item in myList:
                parsed = item.split(':')
                
                #exists?
                if [item for item in self.cpl if (item[0] == str(parsed[0]) and item[1]==str(parsed[1]))]:
                    pass # belki hangisinin time i daha yeniyse o implemente edilebilir?
                #new peer
                else:
                    theTime = str(parsed[2])+":"+str(parsed[3])+":"+str(parsed[4])
                    actTime = time.asctime(time.strptime(theTime, "%a %b %d %H:%M:%S %Y"))
                    self.cpl.append([str(parsed[0]),str(parsed[1]),actTime,str(parsed[5]),"S"])
            self.cplLock.release()
            for item in self.cpl:
                print item
                
    def run(self):
        print "Starting "+self.name
        self.socket.connect((str(self.negIp),int(self.negPort)))
        self.socket.send("REGME "+str(self.ip)+":"+str(self.port))
        data = self.socket.recv(1024)
        self.clientParser(data)
        self.socket.send("GETNL")
        data = self.socket.recv(1024)
        self.clientParser(data)
        print "Negotiator Client calisiyor"
        
        time.sleep(10)
        
        #To close Negotiator Server thread
        self.socket.send("CLOSE")
        self.socket.recv(1024) 
        self.socket.close()
        print "NegClient kapaniyor"
        
        
class ClientThread (threading.Thread):
    def __init__(self, name, negIp, negPort, ip, port, cpl, cplLock):
        threading.Thread.__init__(self)
        self.name = name
        self.negIp = negIp
        self.negPort = negPort
        self.ip = ip
        self.port = port
        self.cpl = cpl
        self.cplLock = cplLock
        self.socket = socket.socket()
    def clientParser(self, data):
        print "Peer a gelen data :", data
        if data[0:5] == "REGWA":
            
            #Resend registration after 5s
            time.sleep(5)
            self.socket.send("REGME "+str(self.ip)+":"+str(self.port))
            data = self.socket.recv(1024)
            
        if data[0:5] == "REGOK":
            print "REGOK GELDI :D"
            
        if data[0:5] == "REGER":
            print "REGER geldi", self.name
        
        elif data[0:11] == "NLIST BEGIN":
            myList = data[12:].split('\n')
            
            #Check to see if last element is correct
            if myList[-1] != "NLIST END":
                return
            
            #Remove NLIST END
            del myList[-1]
            
            self.cplLock.acquire()
            for item in myList:
                parsed = item.split(':')
                
                #exists?
                if [item for item in self.cpl if (item[0] == str(parsed[0]) and item[1]==str(parsed[1]))]:
                    pass # belki hangisinin time i daha yeniyse o implemente edilebilir?
                #new peer
                else:
                    theTime = str(parsed[2])+":"+str(parsed[3])+":"+str(parsed[4])
                    actTime = time.asctime(time.strptime(theTime, "%a %b %d %H:%M:%S %Y"))
                    self.cpl.append([str(parsed[0]),str(parsed[1]),actTime,str(parsed[5]),"W"])
            self.cplLock.release()
            for item in self.cpl:
                print item
                
                
class WorkerThread (threading.Thread):
    def __init__(self, name, inQueue, outQueue, pLock):
        threading.Thread.__init__(self)
        self.name = name
        self.inQueue = inQueue # the queue to read unprocessed data
        self.outQueue = outQueue # the queue to put processed data
        self.pLock = pLock
        self.patchsize = 128

    def convertGray(self, header, patch):
        # convert the patch to gray (actually does nothing as the incoming
        # data is already 8bit grayscale data)
        newMessage = [0] * self.patchsize * self.patchsize
        for i in range(0,self.patchsize * self.patchsize):
            newMessage[i] = patch[i]
        return (header, newMessage)

    def filterSobel(self, header, patch, threshold):
        # convolve the patch with the matrix [[1,0,-1],[2,0,-2][1,0,-1]]
        # read how the convolution is applied in discrete domain
        newMessage = [0] * self.patchsize * self.patchsize
        for i in range(1, self.patchsize-1):
            for j in range(1, self.patchsize-1):
                index0 = j * self.patchsize + i # top line index
                index1 = (j+1) * self.patchsize + i # same line index
                index1r = (j-1) * self.patchsize + i # bottom line index
                temp0 = \
                    + 1* patch[index1r - 1] \
                    - 1* patch[index1r + 1] \
                    + 2* patch[index0 - 1] \
                    - 2* patch[index0 + 1] \
                    + 1* patch[index1 - 1] \
                    - 1* patch[index1 + 1]

                temp1 = \
                    - 1* patch[index1r - 1] \
                    - 2* patch[index1r]\
                    - 1* patch[index1r + 1] \
                    + 1* patch[index1 - 1] \
                    + 2* patch[index1]\
                    + 1* patch[index1 + 1]

                newMessage[index0] = int(math.sqrt(temp0**2 + temp1**2))
                # apply the threshold parameter
                # if newMessage[index0] > threshold:
                #     newMessage[index0] = 255
                # else:
                #     newMessage[index0] = 0
        return (header, newMessage)


    def run(self):
        print self.name + ": Starting."
        while(True):
            if self.inQueue.qsize() > 0:
                message = self.inQueue.get()
                if message == "END":
                    print self.name + ": Ending."
                    break
                print self.name + ": " + str(message[0][0]) + \
                    " " + str(message[0][1]) + " Queue size: " \
                      + str(self.inQueue.qsize())
                if str(message[0][0]) == "SobelFilter":
                    outMessage = self.filterSobel(message[0][1], message[1],
                                                  128)
                if str(message[0][0]) == "GrayScale":
                    outMessage = self.convertGray(message[0][1], message[1])
                # self.pLock.acquire()
                self.outQueue.put(outMessage)
                # self.pLock.release()
            time.sleep(.01)

class imGui(QMainWindow):
    def __init__(self, workQueue, processedQueue, pLock):
        self.qt_app = QApplication(sys.argv)
        QWidget.__init__(self, None)

        # create the main ui
        self.pQueue = processedQueue
        self.wQueue = workQueue
        self.ui = Ui_ImageProcessor()
        self.ui.setupUi(self)
        self.imageScene = QGraphicsScene()
        self.original = None
        self.processed = None
        self.frameScaled = None
        self.imageFile = None
        self.pLock = pLock
        self.patchsize = 128

        # fill combobox
        self.ui.boxFunction.addItem("GrayScale")
        self.ui.boxFunction.addItem("SobelFilter")

        # connect buttons
        self.ui.buttonLoadImage.clicked.connect(self.loadImagePressed)
        self.ui.buttonResetImage.clicked.connect(self.resetImagePressed)
        self.ui.buttonStartProcess.clicked.connect(self.startProcess)
        self.ui.buttonStopProcess.clicked.connect(self.stopProcess)

        # start timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.collectPatch)
        self.timer.start(10)

        self.sTimer = QTimer()
        self.sTimer.timeout.connect(self.scheduler)

        self.perms = None

        self.sceneObject = None

    def loadImagePressed(self):
        # load the image from a file into a QImage object
        imageFile = QFileDialog.getOpenFileName(self,
                                              'Open file',
                                              '.',
                                              'Images (*.png *.xpm '
                                              '*.jpg)' )
        if not imageFile:
            return
        with open(imageFile, 'r') as f:
            try:
                self.imageFile = imageFile
                self.original = QImage(imageFile)
                # say that an image is loaded
                print "Image loaded: " + imageFile
            except:
                print "Problem with image file: " + self.imageFile
                self.imageFile = None
            finally:
                self.processed = self.original.convertToFormat(
                    QImage.Format_RGB16)
                if self.imageFile:
                    # find the horizontal and vertical patch numgers
                    self.tmpPatchNum = (
                        self.processed.size().width() / self.patchsize,
                        self.processed.size().height() / self.patchsize )
                    self.numPatches = self.tmpPatchNum[0] * \
                                      self.tmpPatchNum[1]

                self.updateImage()

    def resetImagePressed(self):
        # return to the original image
        if not self.imageFile:
            return
        self.processed = self.original
        self.updateImage()

    def updateImage(self):
        # update the visual of the image with the new processed image
        if self.processed:
            multiplierh = float(self.processed.size().height())/float(self.ui.imageView.size().height())
            multiplierw = float(self.processed.size().width())/float(self.ui.imageView.size().width())
            if multiplierh > multiplierw:
                self.frameScaled = self.processed.scaledToHeight(self.ui.imageView.size().height() - 5 )
            else:
                self.frameScaled = self.processed.scaledToWidth(self.ui.imageView.size().width() - 5 )

            if self.sceneObject:
                self.imageScene.removeItem(self.sceneObject)
            self.sceneObject = self.imageScene.addPixmap(QPixmap.fromImage(self.frameScaled))
            self.imageScene.update()
            self.ui.imageView.setScene(self.imageScene)

    def serializePatch(self, x, y, offset = 0):
        # serializes the patch and prepares the message data
        tempVector = [0] * (self.patchsize**2)
        rect = (x*self.patchsize, y*self.patchsize)
        rng = range(0,self.patchsize)

        for j in rng:
            Y = j + rect[1]
            for i in rng:
                X = i + rect[0]
                # the message contains 8-bit grayscale (0-255) data
                tempVector[j*self.patchsize + i] = \
                    rgb2gray(self.processed.pixel(X,Y))
                # we should also send the reference rectangle information
                # where to put the patch when we receive the processed
        return rect, tempVector

    def deserializePatch(self, refPix, data):
        # convert the message data into the matrix and put directy on the
        # image using the reference pixels (refPix)
        counter = 0
        for color in data:
            x = counter % self.patchsize
            y = counter // self.patchsize
            self.processed.setPixel(refPix[0] + x,
                                    refPix[1] + y,
                                    gray2rgb(color))
            counter += 1


    def scheduler(self):
        # puts the serialized patches into the work queue
        if self.processed:
            function = self.ui.boxFunction.currentText()
            if len(self.perms) > 0:
                p = self.perms.pop()
                x = p % self.tmpPatchNum[0]
                y = p // self.tmpPatchNum[0]
                rect, tempVector = self.serializePatch(x,y)
                self.wQueue.put(((function, rect), tempVector))
            else:
                self.sTimer.stop()


    def collectPatch(self):
        # collects the processed patches from the process queue
        if self.pQueue.qsize() > 0:
            for i in range(0, self.pQueue.qsize()):
                # self.pLock.acquire()
                message = self.pQueue.get()
                # self.pLock.release()
                self.deserializePatch(message[0], message[1])
            self.updateImage()

    def startProcess(self):
        # randomly organizes the patches
        self.perms = list(np.random.permutation(self.numPatches))

        # or simply orders the patches
        # self.perms = range(0,self.numPatches)
        # self.perms.reverse()

        # start scheduler's timer
        self.sTimer.start()

    def stopProcess(self):
        # stops the timer and thus the processing
        self.sTimer.stop()

    def run(self):
        self.show()
        self.qt_app.exec_()


def main():
    # the queue should contain no more than maxSize elements
    global UPDATE_INTERVAL
    global numThreads
    global maxSize
    global exitFlag
    exitFlag = 0
    UPDATE_INTERVAL = 60*10
    numThreads = 4
    maxSize = numThreads * 25
    QUEUENUM = 20
    
    workQueue = Queue.Queue(QUEUENUM)
    processedQueue = Queue.Queue(maxSize)
    pLock = threading.Lock()
    iPort = []
    if len(sys.argv) == 3:
        iPort.append(str(sys.argv[1]))
        iPort.append(int(sys.argv[2]))
    else:
        print "usage : <filename> <Peer IP> <Peer Port> "
        sys.exit()
        
    mainThread = MainThread(workQueue,processedQueue,pLock,iPort)
    mainThread.start()
    #app = imGui(workQueue,processedQueue, pLock)
    #app.run()
    
if __name__ == '__main__':
    main()

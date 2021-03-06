import sys
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time
class ReadThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue, app, exitFlag):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.nickname = ""
        self.threadQueue = threadQueue
        self.app = app
        self.exitFlag = exitFlag
    def incoming_parser(self, data):
        print "incomingdeyim, datam : ",data
        if len(data) == 0:
            return
        if len(data) > 3 and not data[3] == " ":
            response = "ERR"
            self.csoc.send(response)
            return
        rest = data[4:]
        print "message itself : ",data
        if data[0:3] == "BYE":
            self.exitFlag = 1
            self.csoc.close()
            return
        if data[0:3] == "ERL":
            response = "-Server- Nick not registered"
            self.app.cprint(response)
            return
        if data[0:3] == "HEL":
            response = "-Server- Registered as <"+data[4:]+">"
            self.app.cprint(response)
            self.nickname = data[4:]
            return
        if data[0:3] == "REJ":
            response = "-Server- Nickname already taken"
            self.app.cprint(response)
            return
        if data[0:3] == "MNO":
            response = "-Server- No user called " + data[4:]+" in chat"
            self.app.cprint(response)
            return
        if data[0:3] == "MSG":
            print rest
            usrName = str(rest.split(":",1)[0])
            restMessage = str(rest.split(":",1)[1])
            response = "<"+usrName+"> : "+restMessage
            #response = rest TEK harfli nickname lerde sikinti cikarttiginda direk response olarak rest 
            self.app.cprint(response)
            return
        if data[0:3] == "SAY":
            usrName = str(rest.split(":",1)[0])
            restMessage = str(rest.split(":",1)[1])
            response = "<"+usrName+"> : "+restMessage
            #response = rest TEK harfli nickname lerde sikinti cikarttiginda direk response
            self.app.cprint(response)
            return 
        if data[0:3] == "TIC":
            response = "TOC"
            self.csoc.send(response)
            return
        if data[0:3] == "SYS":
            response = "-Server- " + data[4:]
            self.app.cprint(response)
            return
        if data[0:3] == "LSA":
            rest = data[4:]
            splitted = rest.split(":")
            msg = "-Server- Registered nicks: "
            for i in splitted:
                msg += i + ","
            msg = msg[:-1]
            self.app.cprint(msg)
            return
    def run(self):
        while not self.exitFlag:
            try:
                data = self.csoc.recv(1024)
                print "gelen data:", data
                self.incoming_parser(data)
            except:
                pass
class WriteThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue = threadQueue
    def run(self):
        exitFlag = 0
        while True:
            if self.threadQueue.qsize() > 0:
                queue_message = self.threadQueue.get()
                try:
                    print "servera gonderilecek : " , queue_message
                    self.csoc.send(queue_message)
                except socket.error:
                    self.csoc.close()
                    break
                if queue_message == "QUI":
                    break
class ClientDialog(QDialog):
    ''' An example application for PyQt. Instantiate
    and call the run method to run. '''
    def __init__(self, threadQueue):
        self.threadQueue = threadQueue
        # create a Qt application --- every PyQt app needs one
        self.qt_app = QApplication(sys.argv)
        # Call the parent constructor on the current object
        QDialog.__init__(self, None)
        # Set up the window
        self.setWindowTitle('IRC Client')
        self.setMinimumSize(500, 200)
        # Add a vertical layout
        self.vbox = QVBoxLayout()
        # The sender textbox
        self.sender = QLineEdit("", self)
        # The channel region
        self.channel = QTextBrowser()
        # The send button
        self.send_button = QPushButton('&Send')
        # Connect the Go button to its callback
        self.send_button.clicked.connect(self.outgoing_parser)
        # Add the controls to the vertical layout
        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)
        # A very stretchy spacer to force the button to the bottom
        # self.vbox.addStretch(100)
        # Use the vertical layout for the current window
        self.setLayout(self.vbox)
    def cprint(self, data):
        self.channel.append(data)
    def outgoing_parser(self):
        data = self.sender.text()
        if len(data) == 0:
            return
        self.cprint("-Local-: " + data)
        if data[0] == "/":
            command = data[1:5]
            if command == "list":
                self.threadQueue.put("LSQ")
            elif command == "quit":
                self.threadQueue.put("QUI")
            elif command == "msg ":
                data = str(data)
                source = data.split(" ",2)
                message = None
                to_nick = source[1]
                if len(source)>2:
                    message = source[2] # Burada bosluksuz yazi cikaracak, a faire
                else:
                    message = " "
                myMsg = "MSG " + str(to_nick)+":"+str(message)
                self.threadQueue.put(myMsg)
            elif command == "nick":
                myMsg = "USR "+str(data.split(" ",1)[1])
                print data.split(" ",1)[1]," USR GONDERISI"
                self.threadQueue.put(myMsg)
            else:
                self.cprint("Local: Command Error.")
        else:
            response = str("SAY "+data)
            self.threadQueue.put(response)
            print data, "soyledim"
        self.sender.clear()
    def run(self):
        '''Run the app and show the main form. '''
        self.show()
        self.qt_app.exec_()
def main():
    host = None
    port = None
    if len(sys.argv) == 3:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        print host, type(host),port,type(port)
    else:
        print "usage : <filename> <Host IP> <Host Port> "
        sys.exit()
    # connect to the server
    try:
        print host,port
        s = socket.socket()
        s.connect((host,port))
        sendQueue = Queue.Queue()
        app = ClientDialog(sendQueue)
        # start threads
        rt = ReadThread("ReadThread", s, sendQueue, app,0)
        rt.setDaemon(True)
        rt.start()
        wt = WriteThread("WriteThread", s, sendQueue)
        wt.setDaemon(True)
        wt.start()
        app.run()
        
        rt.join()
        wt.join()
        
        s.close()
    except:
        print "patladin"
if __name__ == '__main__':
    main()

import sys
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time
class ReadThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue, app):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.nickname = ""
        self.threadQueue = threadQueue
        self.app = app
    def incoming_parser(self, data):
        pass
    def run(self):
        while True:
            data = self.csoc.recv(1024)
            pass
class WriteThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue = threadQueue
    def run(self):
        pass
        if self.threadQueue.qsize() > 0:
            queue_message = self.threadQueue.get()
            pass
            try:
                self.csoc.send(queue_message)
            except socket.error:
                self.csoc.close()
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
        pass
        self.channel.append(data)
    def outgoing_parser(self):
        pass
    def run(self):
        '''Run the app and show the main form. '''
        self.show()
        self.qt_app.exec_()
def main():
    host = None
    port = None
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
    else:
        print "usage : <filename> <Host IP> <Host Port> "
        sys.exit()        
    # connect to the server
    s = socket.socket()
    s.connect((host,port))
    sendQueue = ...
    app = ClientDialog(sendQueue)
    # start threads
    rt = ReadThread("ReadThread", s, sendQueue, app)
    rt.start()
    wt = WriteThread("WriteThread", s, sendQueue)
    wt.start()
    app.run()
    rt.join()
    wt.join()
    s.close()
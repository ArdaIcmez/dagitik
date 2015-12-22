# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyGraphics.ui'
#
# Created: Thu Dec 17 18:23:19 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ImageProcessor(object):
    def setupUi(self, ImageProcessor):
        ImageProcessor.setObjectName(_fromUtf8("ImageProcessor"))
        ImageProcessor.resize(820, 504)
        self.imageView = QtGui.QGraphicsView(ImageProcessor)
        self.imageView.setGeometry(QtCore.QRect(10, 10, 800, 450))
        self.imageView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imageView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imageView.setObjectName(_fromUtf8("imageView"))
        self.buttonLoadImage = QtGui.QPushButton(ImageProcessor)
        self.buttonLoadImage.setGeometry(QtCore.QRect(10, 470, 75, 23))
        self.buttonLoadImage.setObjectName(_fromUtf8("buttonLoadImage"))
        self.buttonStartProcess = QtGui.QPushButton(ImageProcessor)
        self.buttonStartProcess.setGeometry(QtCore.QRect(630, 470, 83, 21))
        self.buttonStartProcess.setObjectName(_fromUtf8("buttonStartProcess"))
        self.boxFunction = QtGui.QComboBox(ImageProcessor)
        self.boxFunction.setGeometry(QtCore.QRect(500, 470, 121, 21))
        self.boxFunction.setObjectName(_fromUtf8("boxFunction"))
        self.buttonStopProcess = QtGui.QPushButton(ImageProcessor)
        self.buttonStopProcess.setGeometry(QtCore.QRect(720, 470, 83, 21))
        self.buttonStopProcess.setObjectName(_fromUtf8("buttonStopProcess"))
        self.buttonResetImage = QtGui.QPushButton(ImageProcessor)
        self.buttonResetImage.setGeometry(QtCore.QRect(100, 470, 75, 23))
        self.buttonResetImage.setObjectName(_fromUtf8("buttonResetImage"))

        self.retranslateUi(ImageProcessor)
        QtCore.QMetaObject.connectSlotsByName(ImageProcessor)

    def retranslateUi(self, ImageProcessor):
        ImageProcessor.setWindowTitle(_translate("ImageProcessor", "Image Processor", None))
        self.buttonLoadImage.setText(_translate("ImageProcessor", "Load", None))
        self.buttonStartProcess.setText(_translate("ImageProcessor", "Start", None))
        self.buttonStopProcess.setText(_translate("ImageProcessor", "Stop", None))
        self.buttonResetImage.setText(_translate("ImageProcessor", "Reset", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 529)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 60, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 71, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(250, 60, 71, 19))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(250, 30, 60, 19))
        self.label_4.setObjectName("label_4")
        self.sendChat = QtWidgets.QPushButton(self.centralwidget)
        self.sendChat.setGeometry(QtCore.QRect(450, 440, 51, 31))
        self.sendChat.setObjectName("sendChat")
        self.ipserv = QtWidgets.QLineEdit(self.centralwidget)
        self.ipserv.setGeometry(QtCore.QRect(110, 30, 113, 21))
        self.ipserv.setObjectName("ipserv")
        self.yourname = QtWidgets.QLineEdit(self.centralwidget)
        self.yourname.setGeometry(QtCore.QRect(110, 60, 113, 21))
        self.yourname.setObjectName("yourname")
        self.startServer = QtWidgets.QPushButton(self.centralwidget)
        self.startServer.setGeometry(QtCore.QRect(250, 30, 51, 51))
        self.startServer.setObjectName("startServer")
        self.textChat = QtWidgets.QLineEdit(self.centralwidget)
        self.textChat.setGeometry(QtCore.QRect(10, 440, 421, 31))
        self.textChat.setObjectName("textChat")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 140, 461, 281))
        self.tabWidget.setObjectName("tabWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 510, 30))
        self.menubar.setObjectName("menubar")
        self.menuChat_Sederhana = QtWidgets.QMenu(self.menubar)
        self.menuChat_Sederhana.setObjectName("menuChat_Sederhana")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuChat_Sederhana.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat Sederhana"))
        self.label.setText(_translate("MainWindow", "IP Server"))
        self.label_2.setText(_translate("MainWindow", "Your name"))
        self.sendChat.setText(_translate("MainWindow", "Send"))
        self.startServer.setText(_translate("MainWindow", "Start"))
        self.menuChat_Sederhana.setTitle(_translate("MainWindow", "Chat Sederhana"))

        self.tabWidget.currentChanged.connect(self.on_tab_change)
        self.sendChat.clicked.connect(self.on_send)
        self.startServer.clicked.connect(self.on_start)
        self.textChat.returnPressed.connect(self.on_send)
        self.ip_server = None
        self.signal = MySignal()
        self.signal.sig_with_str.connect(self.new_tab_client)

    def add_tab(self, tabname, tabtext):
        _translate = QtCore.QCoreApplication.translate
        tab = QtWidgets.QWidget()
        tab.setObjectName(tabname)
        listWidget = QtWidgets.QListWidget(tab)
        listWidget.setGeometry(QtCore.QRect(0, 0, 451, 241))
        listWidget.setObjectName("list_{}".format(tabname))
        setattr(self, "list_{}".format(tabname), listWidget)
        self.tabWidget.addTab(tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(tab), _translate("MainWindow", tabtext))

    def new_tab_client(self, tups):
        ip, name = tups
        self.add_tab("tab{}".format(ip2int(ip)), name)

import struct
import socket
def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

class MySignal(QtCore.QObject):
    sig_with_str = QtCore.pyqtSignal(tuple)

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from window import Ui_MainWindow
from threading import Thread
import struct
import socket
import time
import sys

ui = None
serverThread = None
clientList = []
currentTab = -1
display_name = dict()

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def on_send(self):
    send_text = self.textChat.text()
    print(currentTab)
    print(clientList)
    if send_text and currentTab >= 0:
        ip = clientList[currentTab]
        client(self.ip_server, ip, 4444, send_text)
        listtab = getattr(self, 'list_tab{}'.format(ip2int(ip)).format())
        listtab.addItem("you> {}".format(send_text))
        self.textChat.setText("")

def on_start(self):
    global serverThread
    if self.ip_server:
        return
    self.ip_server = self.ipserv.text()
    self.port_server = 4444
    serverThread = ServerThread(self.ip_server, self.port_server, self)
    serverThread.start()
    udp_serverThread = UdpServerThread(self.ip_server, self.port_server, self)
    udp_serverThread.start()
    udp_clientThread = UdpClientThread(self.ip_server, self.port_server, self)
    udp_clientThread.start()

def on_tab_change(self, i):
    global currentTab
    print("ganti tab ke-{}".format(i))
    currentTab = i

Ui_MainWindow.on_send = on_send
Ui_MainWindow.on_start = on_start
Ui_MainWindow.on_tab_change = on_tab_change

class Client():
    def setIP(self, ip):
        self.ip = ip

    def setName(self, name):
        self.name = name

    def getIP(self):
        return self.ip

    def getName(self):
        return self.name

class UdpServerThread(Thread):
    def __init__(self,ip,port,window):
        Thread.__init__(self)
        self.window=window
        self.ip = ip
        self.port = port


    def run(self):
        UDP_IP = self.ip
        UDP_PORT = 12345
        BUFFER_SIZE = 20
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpServer.bind(('0.0.0.0', UDP_PORT))
        threads = []
        print("start")
        window = self.window
        while True:
            (msg, (ip,port)) = udpServer.recvfrom(2048)
            if ip == self.ip or ip in clientList:
                continue
            clientList.append(ip)
            print("masuk {} {} {}".format(msg, ip, port))
            name = str(msg, 'utf-8')
            window.signal.sig_with_str.emit((ip,name))
            display_name[ip] = name

class UdpClientThread(Thread):
    def __init__(self,ip,port,window):
        Thread.__init__(self)
        self.window=window
        self.ip = ip
        self.port = port


    def run(self):
        UDP_IP = self.ip
        UDP_PORT = 0
        BUFFER_SIZE = 20
        udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpClient.bind((UDP_IP, UDP_PORT))
        threads = []
        print("start")
        window = self.window
        while True:
            time.sleep(1)
            name = bytes(window.yourname.text(), 'utf-8')
            udpClient.sendto(name, ('255.255.255.255', 12345))

class ServerThread(Thread):
    def __init__(self,ip,port,window):
        Thread.__init__(self)
        self.window=window
        self.ip = ip
        self.port = port


    def run(self):
        TCP_IP = self.ip
        TCP_PORT = self.port
        BUFFER_SIZE = 20
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))

        tcpServer.listen(4)
        while True:
            (conn, (ip,port)) = tcpServer.accept()
            print("dapat {}".format(ip))
            if ip not in clientList:
                continue
            newthread = ClientThread(conn, ip,port,self.window)
            newthread.start()

class ClientThread(Thread):

    def __init__(self,conn,ip,port,window):
        Thread.__init__(self)
        self.window=window
        self.ip = ip
        self.port = port
        self.conn = conn

    def run(self):
        conn = self.conn
        data = conn.recv(2048)
        self.window.textChat.setText("")
        tampil = "{}> {}".format(display_name[self.ip], data.decode("utf-8"))
        print(tampil)
        listtab = getattr(self.window, 'list_tab{}'.format(ip2int(self.ip)).format())
        listtab.addItem(tampil)
        conn.close()

def client(bind_ip, ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((bind_ip, 0))
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        sock.close()

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        global ui
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.setObjectName("Dialog")
        self.resize(239, 133)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(17, 20, 81, 31))
        self.label.setObjectName("label")
        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setGeometry(QtCore.QRect(90, 20, 137, 28))
        self.textName.setObjectName("textName")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 81, 31))
        self.label_2.setObjectName("label_2")
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setGeometry(QtCore.QRect(90, 50, 137, 28))
        self.textPass.setObjectName("textPass")
        self.buttonLogin = QtWidgets.QPushButton(self)
        self.buttonLogin.setGeometry(QtCore.QRect(90, 80, 84, 24))
        self.buttonLogin.setObjectName("buttonLogin")
        self.buttonLogin.clicked.connect(self.handleLogin)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Please enter username and password first"))
        self.label.setText(_translate("Dialog", "Username"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.buttonLogin.setText(_translate("Dialog", "Login"))

    def handleLogin(self):
        if (self.textName.text() == 'guest' and
            self.textPass.text() == 'guest'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

def main():
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        application = ApplicationWindow()
        application.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()

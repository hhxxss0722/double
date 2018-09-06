from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore,QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore as Qt
import sys
from ctypes import *
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication)

class CanCfg(Structure):
    _fields_ = [("AccCode", c_ulong),
                ("AccMask", c_ulong),
                ("Reserved ", c_ulong),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)]
class Canobj(Structure):
    _fields_ =[
                ("ID",c_uint),
                ("TimeStamp",c_uint),
                ("TimeFlag",c_byte),
                ("SendType",c_byte),
                ("RemoteFlag",c_byte),
                ("ExternFlag",c_byte),
                ("DataLen",c_byte),
                ("Data",c_byte*8),
                ("Reserved",c_byte*3)]

class Errobj(Structure):
    _fields_ = [
        ("ErrCode", c_ulong),
        ("Passive_ErrData", c_byte * 3),
        ("ArLost_ErrData", c_byte)]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(657, 677)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = PyQt5.QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.tableWidget = PyQt5.QtWidgets.QTableWidget(self.centralwidget)
        # self.tableWidget.setGeometry(PyQt5.QtCore.QRect(60, 80, 601, 192))
        # self.tableWidget.setShowGrid(True)
        # self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(6)

        self.btn_enterqc = QtWidgets.QPushButton(self.centralwidget)
        self.btn_enterqc.setGeometry(QtCore.QRect(400, 21, 75, 23))
        self.btn_enterqc.setObjectName("btn_enterqc")

        self.btn_sqc = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sqc.setGeometry(QtCore.QRect(480, 21, 75, 23))
        self.btn_sqc.setObjectName("btn_sqc")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 82, 24, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 82, 18, 16))
        self.label_3.setObjectName("label_3")

        self.btn_port = QtWidgets.QPushButton(self.centralwidget)
        self.btn_port.setGeometry(QtCore.QRect(610, 260, 41, 23))
        self.btn_port.setObjectName("btn_port")
        self.btn_usb = QtWidgets.QPushButton(self.centralwidget)
        self.btn_usb.setGeometry(QtCore.QRect(560, 290, 41, 23))
        self.btn_usb.setObjectName("btn_usb")

        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(100, 134, 24, 16))
        self.label_16.setObjectName("label_16")

        # self.txt_app = QtWidgets.QLineEdit(self.centralwidget)
        # self.txt_app.setGeometry(QtCore.QRect(136, 82, 30, 20))

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")

        self.com_open = QtWidgets.QPushButton(self.centralwidget)
        self.com_open.setGeometry(QtCore.QRect(230, 21, 75, 23))
        self.com_open.setObjectName("com_open")

        self.cb_com = QtWidgets.QComboBox(self.centralwidget)
        self.cb_com.setGeometry(QtCore.QRect(51, 22, 90, 20))
        self.cb_com.setObjectName("cb_com")

        MainWindow.setMenuBar(self.menubar)

        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.wifisetm = QtWidgets.QAction(MainWindow)
        # self.wifisetm.setObjectName("wifisetm")
        # self.action = QtWidgets.QAction(MainWindow)
        # self.action.setObjectName("action")
        # self.action_2 = QtWidgets.QAction(MainWindow)
        # self.action_2.setObjectName("action_2")
        # self.m_sv = QtWidgets.QAction(MainWindow)
        # self.m_sv.setObjectName("m_sv")
        # self.action_3 = QtWidgets.QAction(MainWindow)
        # self.action_3.setObjectName("action_3")
        # self.action_4 = QtWidgets.QAction(MainWindow)
        # self.action_4.setObjectName("action_4")
        # self.action_5 = QtWidgets.QAction(MainWindow)
        # self.action_5.setObjectName("action_5")
        # self.action_6 = QtWidgets.QAction(MainWindow)
        # self.action_6.setObjectName("action_6")
        # self.action_7 = QtWidgets.QAction(MainWindow)
        # self.action_7.setObjectName("action_7")
        #
        # self.menu.addAction(self.action)
        # self.menu.addAction(self.wifisetm)
        # self.menu.addAction(self.m_sv)
        # self.menu.addAction(self.action_2)
        # self.menu_2.addAction(self.action_3)
        # self.menu_2.addAction(self.action_4)
        # self.menu_2.addAction(self.action_5)
        # self.menu_3.addAction(self.action_6)
        # self.menu_4.addAction(self.action_7)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Linux管理工具"))
        self.label_2.setText(_translate("MainWindow", "端口:"))
        self.label_16.setText(_translate("MainWindow", "ssid"))
        self.menu.setTitle(_translate("MainWindow", "打开"))
        self.menu_2.setTitle(_translate("MainWindow", "打印"))
        self.menu_3.setTitle(_translate("MainWindow", "查询"))
        self.menu_4.setTitle(_translate("MainWindow", "关于"))
        self.com_open.setText(_translate("MainWindow", "打开"))
        self.com_open.clicked.connect(self.port_open)

    def port_open(self):
        self.dll = 'ControlCAN.dll'
        self.lib = windll.LoadLibrary(self.dll)
        self.opendev = self.lib.VCI_OpenDevice
        self.initcan = self.lib.VCI_InitCAN
        self.startcan = self.lib.VCI_StartCAN
        self.senddata = self.lib.VCI_Transmit
        self.closedev = self.lib.VCI_CloseDevice
        self.receivenum = self.lib.VCI_GetReceiveNum
        self.receivedata = self.lib.VCI_Receive
        self.readerrinfo = self.lib.VCI_ReadErrInfo
        self.resetcan = self.lib.VCI_ResetCAN
        self.GetSet = self.lib.VCI_GetReference2

        self.cancfg = CanCfg()
        # self.InitDefaultCanData()
        self.cancfg.AccCode = 1 << 21
        self.cancfg.AccMask = 3 << 21
        self.cancfg.Filter = 1
        self.cancfg.Timing0 = 0
        self.cancfg.Timing1 = 28
        self.cancfg.Mode = 0

        self.cobj = Canobj()
        self.errobj = Errobj()
        self.devtype = 4
        self.devindex = 0
        self.canindex = 0
        self.devopen = False

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        item = self.tableWidget.verticalHeaderItem(0)
        # item.setText("MainWindow")
        item = self.tableWidget.horizontalHeaderItem(0)
        # item.setText("MainWindow")
        item = self.tableWidget.horizontalHeaderItem(1)
        # item.setText("MainWindow")


# class myprog(Ui_MainWindow):
#     def __init__(self, dialog):
#         Ui_MainWindow.__init__(self)
#         self.setupUi(dialog)
#         self.retranslateUi(dialog)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = PyQt5.QtWidgets.QMainWindow()

    coll=Ui_MainWindow()
    coll.setupUi(dialog)
    # tbox = myprog(dialog)
    dialog.show()

    sys.exit(app.exec_())
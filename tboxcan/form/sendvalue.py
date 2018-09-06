# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sendvalue.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QMessageBox 

class Ui_SendValueForm(object):
    def setupUi(self, SendValueForm):
        SendValueForm.setObjectName("SendValueForm")
        SendValueForm.resize(250, 277)
        self.layoutWidget = QtWidgets.QWidget(SendValueForm)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 210, 158, 54))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.btn_gpsoff = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_gpsoff.setObjectName("btn_gpsoff")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.btn_gpsoff)
        self.btn_login = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_login.setObjectName("btn_login")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.btn_login)
        self.btn_lpm = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_lpm.setObjectName("btn_lpm")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.btn_lpm)
        self.btn_readupgrade = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_readupgrade.setObjectName("btn_readupgrade")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btn_readupgrade)
        self.widget = QtWidgets.QWidget(SendValueForm)
        self.widget.setGeometry(QtCore.QRect(10, 16, 204, 186))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.cb_l99m = QtWidgets.QComboBox(self.widget)
        self.cb_l99m.setObjectName("cb_l99m")
        self.horizontalLayout.addWidget(self.cb_l99m)
        self.btn_l99m = QtWidgets.QPushButton(self.widget)
        self.btn_l99m.setObjectName("btn_l99m")
        self.horizontalLayout.addWidget(self.btn_l99m)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cb_power = QtWidgets.QComboBox(self.widget)
        self.cb_power.setObjectName("cb_power")
        self.horizontalLayout_2.addWidget(self.cb_power)
        self.btn_power = QtWidgets.QPushButton(self.widget)
        self.btn_power.setObjectName("btn_power")
        self.horizontalLayout_2.addWidget(self.btn_power)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.cb_sim = QtWidgets.QComboBox(self.widget)
        self.cb_sim.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.cb_sim.setObjectName("cb_sim")
        self.horizontalLayout_3.addWidget(self.cb_sim)
        self.btn_sim = QtWidgets.QPushButton(self.widget)
        self.btn_sim.setObjectName("btn_sim")
        self.horizontalLayout_3.addWidget(self.btn_sim)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.cb_emc = QtWidgets.QComboBox(self.widget)
        self.cb_emc.setObjectName("cb_emc")
        self.horizontalLayout_6.addWidget(self.cb_emc)
        self.btn_emc = QtWidgets.QPushButton(self.widget)
        self.btn_emc.setObjectName("btn_emc")
        self.horizontalLayout_6.addWidget(self.btn_emc)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.cb_log = QtWidgets.QComboBox(self.widget)
        self.cb_log.setObjectName("cb_log")
        self.horizontalLayout_4.addWidget(self.cb_log)
        self.btn_log = QtWidgets.QPushButton(self.widget)
        self.btn_log.setObjectName("btn_log")
        self.horizontalLayout_4.addWidget(self.btn_log)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.cb_upgrade = QtWidgets.QComboBox(self.widget)
        self.cb_upgrade.setObjectName("cb_upgrade")
        self.horizontalLayout_5.addWidget(self.cb_upgrade)
        self.btn_upgrade = QtWidgets.QPushButton(self.widget)
        self.btn_upgrade.setObjectName("btn_upgrade")
        self.horizontalLayout_5.addWidget(self.btn_upgrade)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(SendValueForm)
        QtCore.QMetaObject.connectSlotsByName(SendValueForm)

    def retranslateUi(self, SendValueForm):
        _translate = QtCore.QCoreApplication.translate
        SendValueForm.setWindowTitle(_translate("SendValueForm", "下发指令"))
        self.btn_gpsoff.setText(_translate("SendValueForm", "gps off"))
        self.btn_login.setText(_translate("SendValueForm", "Login"))
        self.btn_lpm.setText(_translate("SendValueForm", "lpm"))
        self.btn_readupgrade.setText(_translate("SendValueForm", "读取版本"))
        self.label.setText(_translate("SendValueForm", "L99M"))
        self.btn_l99m.setText(_translate("SendValueForm", "L99m"))
        self.label_2.setText(_translate("SendValueForm", "Power"))
        self.btn_power.setText(_translate("SendValueForm", "power"))
        self.label_3.setText(_translate("SendValueForm", "Sim"))
        self.btn_sim.setText(_translate("SendValueForm", "Sim"))
        self.label_6.setText(_translate("SendValueForm", "EMC"))
        self.btn_emc.setText(_translate("SendValueForm", "emc"))
        self.label_4.setText(_translate("SendValueForm", "Log"))
        self.btn_log.setText(_translate("SendValueForm", "log"))
        self.label_5.setText(_translate("SendValueForm", "Upgrade"))
        self.btn_upgrade.setText(_translate("SendValueForm", "upgrade"))

class SendValuewindow(QtWidgets.QWidget):
    _signal = pyqtSignal(str)
    def __init__(self):  
        super(SendValuewindow,self).__init__()  
        self.new=Ui_SendValueForm()  
        self.new.setupUi(self)
        self.new.cb_sim.setEditable(True)
        self.InitCb()
        #按钮功能
        self.new.btn_l99m.clicked.connect(self.l99m)
        self.new.btn_power.clicked.connect(self.power)
        self.new.btn_log.clicked.connect(self.log)
        self.new.btn_emc.clicked.connect(self.emc)
        self.new.btn_login.clicked.connect(self.login)
        self.new.btn_sim.clicked.connect(self.sim)
        self.new.btn_lpm.clicked.connect(self.lpm)
        self.new.btn_readupgrade.clicked.connect(self.readupgrade)
        self.new.btn_upgrade.clicked.connect(self.upgrade)
        self.new.btn_gpsoff.clicked.connect(self.gpsoff)

    def InitCb(self):
        setlist=['0,0','0,1','1,0','1,1','2,0','2,1','3,0','3,1','4,0','4,1','5,0','5,1','6,0','6,1']
        self.new.cb_l99m.addItems(setlist)
        setlist=['1,0','1,1','2,0','2,1','3,0','3,1','4,0','4,1','5,0','5,1','6,0','6,1']
        self.new.cb_power.addItems(setlist)
        setlist=['0,0','1,1','1,5','1,10','1,20','1,30']
        self.new.cb_sim.addItems(setlist)
        setlist=['1,0','1,1','2,0','2,1','3,0','3,1','4,0','4,1','5,0','5,1','6,0','6,1','7,0','7,1','8,0','8,1']
        self.new.cb_emc.addItems(setlist)
        setlist=['1','0']
        self.new.cb_log.addItems(setlist)
        setlist=['1,0','2,0','2,1','2,2','2,3','2,4']
        self.new.cb_upgrade.addItems(setlist)

    def l99m(self):
        self.GetSendVlaue(self.new.btn_l99m)

    def power(self):
        self.GetSendVlaue(self.new.btn_power)

    def sim(self):
        self.GetSendVlaue(self.new.btn_sim)

    def emc(self):
        self.GetSendVlaue(self.new.btn_emc)

    def log(self):
        self.GetSendVlaue(self.new.btn_log)

    def upgrade(self):
        self.GetSendVlaue(self.new.btn_upgrade)

    def gpsoff(self):
        self.GetSendVlaue(self.new.btn_gpsoff)

    def login(self):
        self.GetSendVlaue(self.new.btn_login)

    def lpm(self):
        self.GetSendVlaue(self.new.btn_lpm)
    
    def readupgrade(self):
        self.GetSendVlaue(self.new.btn_readupgrade)

    def GetSendVlaue(self,t):
        name=t.text()
        cstr=''
        if name=="L99m":
            cstr+="l99m,"+self.new.cb_l99m.currentText()
        elif name=="power":
            cstr+="power,"+self.new.cb_power.currentText()
        elif name=="Sim":
            cstr+="sim,"+self.new.cb_sim.currentText()
        elif name=="emc":
            cstr+="emc,"+self.new.cb_emc.currentText()
        elif name=="log":
            cstr+="log,"+self.new.cb_log.currentText()
        elif name=="upgrade":
            cstr+="upgrade,"+self.new.cb_upgrade.currentText()
        elif name=="gps off":
            cstr+="gpsoff,1"
        elif name=="Login":
            cstr+="login,1"
        elif name=="lpm":
            cstr+="lpm,1"
        elif name=="读取版本":
            cstr+="readupgrade,1"
        self.SendData(cstr)

    def ShowBox(self,s):
        reply = QMessageBox.information(self, "发送数据", s,QMessageBox.Yes)

    def SendData(self,s):
        self._signal.emit(s)
			
    def closewindow(self):
        self._signal.emit("close")


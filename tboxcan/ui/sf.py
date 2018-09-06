# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sf.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SendDialog(object):
    def setupUi(self, SendDialog):
        SendDialog.setObjectName("SendDialog")
        SendDialog.resize(625, 243)
        self.txt_send = QtWidgets.QTextBrowser(SendDialog)
        self.txt_send.setGeometry(QtCore.QRect(10, 11, 611, 181))
        self.txt_send.setObjectName("txt_send")
        self.btn_send = QtWidgets.QPushButton(SendDialog)
        self.btn_send.setGeometry(QtCore.QRect(10, 210, 75, 23))
        self.btn_send.setObjectName("btn_send")
        self.btn_clear = QtWidgets.QPushButton(SendDialog)
        self.btn_clear.setGeometry(QtCore.QRect(90, 210, 75, 23))
        self.btn_clear.setObjectName("btn_clear")
        self.btn_close = QtWidgets.QPushButton(SendDialog)
        self.btn_close.setGeometry(QtCore.QRect(170, 210, 75, 23))
        self.btn_close.setObjectName("btn_close")
        self.cb_16 = QtWidgets.QCheckBox(SendDialog)
        self.cb_16.setGeometry(QtCore.QRect(270, 215, 71, 16))
        self.cb_16.setObjectName("cb_16")

        self.retranslateUi(SendDialog)
        QtCore.QMetaObject.connectSlotsByName(SendDialog)

    def retranslateUi(self, SendDialog):
        _translate = QtCore.QCoreApplication.translate
        SendDialog.setWindowTitle(_translate("SendDialog", "发送数据"))
        self.btn_send.setText(_translate("SendDialog", "发送"))
        self.btn_clear.setText(_translate("SendDialog", "清除"))
        self.btn_close.setText(_translate("SendDialog", "关闭"))
        self.cb_16.setText(_translate("SendDialog", "HEX"))


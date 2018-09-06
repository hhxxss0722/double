# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imeiprint.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(221, 267)
        self.txt_print = QtWidgets.QLineEdit(Dialog)
        self.txt_print.setGeometry(QtCore.QRect(10, 10, 201, 20))
        self.txt_print.setObjectName("txt_print")
        self.btn_ok = QtWidgets.QPushButton(Dialog)
        self.btn_ok.setGeometry(QtCore.QRect(10, 240, 75, 23))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_reset = QtWidgets.QPushButton(Dialog)
        self.btn_reset.setGeometry(QtCore.QRect(140, 240, 75, 23))
        self.btn_reset.setObjectName("btn_reset")
        self.list_print = QtWidgets.QListWidget(Dialog)
        self.list_print.setGeometry(QtCore.QRect(10, 40, 201, 192))
        self.list_print.setObjectName("list_print")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_ok.setText(_translate("Dialog", "打印"))
        self.btn_reset.setText(_translate("Dialog", "重新打印"))


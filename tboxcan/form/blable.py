# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blable.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(220, 128)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 169, 101))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txt_imei = QtWidgets.QLineEdit(self.widget)
        self.txt_imei.setObjectName("txt_imei")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_imei)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_batch = QtWidgets.QLineEdit(self.widget)
        self.txt_batch.setObjectName("txt_batch")
        self.txt_batch.setReadOnly(True)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_batch)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_print = QtWidgets.QPushButton(self.widget)
        self.btn_print.setObjectName("btn_print")
        self.horizontalLayout.addWidget(self.btn_print)
        self.btn_read = QtWidgets.QPushButton(self.widget)
        self.btn_read.setObjectName("btn_read")
        self.horizontalLayout.addWidget(self.btn_read)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.lab_pcount = QtWidgets.QLabel(self.widget)
        self.lab_pcount.setObjectName("lab_pcount")
        self.verticalLayout_2.addWidget(self.lab_pcount)
        Dialog.setFixedSize(Dialog.width(), Dialog.height())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "背面标签打印"))
        self.label.setText(_translate("Dialog", "IMEI"))
        self.label_2.setText(_translate("Dialog", "批次"))
        self.btn_print.setText(_translate("Dialog", "打印"))
        self.btn_read.setText(_translate("Dialog", "读取配置"))
        self.lab_pcount.setText(_translate("Dialog", "打印个数："))
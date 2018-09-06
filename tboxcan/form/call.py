# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'call.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 

class Ui_CallForm(object):
    def setupUi(self, CallForm):
        CallForm.setObjectName("CallForm")
        CallForm.resize(249, 204)
        self.widget = QtWidgets.QWidget(CallForm)
        self.widget.setGeometry(QtCore.QRect(20, 20, 199, 172))
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
        self.txt_cn = QtWidgets.QLineEdit(self.widget)
        self.txt_cn.setObjectName("txt_cn")
        self.horizontalLayout.addWidget(self.txt_cn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.txt_ln = QtWidgets.QLineEdit(self.widget)
        self.txt_ln.setObjectName("txt_ln")
        self.horizontalLayout_2.addWidget(self.txt_ln)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_call = QtWidgets.QPushButton(self.widget)
        self.btn_call.setObjectName("btn_call")
        self.verticalLayout_2.addWidget(self.btn_call)
        self.btn_calla = QtWidgets.QPushButton(self.widget)
        self.btn_calla.setObjectName("btn_calla")
        self.verticalLayout_2.addWidget(self.btn_calla)
        self.btn_callh = QtWidgets.QPushButton(self.widget)
        self.btn_callh.setObjectName("btn_callh")
        self.verticalLayout_2.addWidget(self.btn_callh)
        self.btn_close = QtWidgets.QPushButton(self.widget)
        self.btn_close.setObjectName("btn_close")
        self.verticalLayout_2.addWidget(self.btn_close)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.btn_callh.raise_()
        self.btn_calla.raise_()
        self.btn_call.raise_()
        self.btn_close.raise_()
        self.label.raise_()
        self.txt_cn.raise_()
        self.label_2.raise_()
        self.txt_ln.raise_()

        self.retranslateUi(CallForm)
        QtCore.QMetaObject.connectSlotsByName(CallForm)

    def retranslateUi(self, CallForm):
        _translate = QtCore.QCoreApplication.translate
        CallForm.setWindowTitle(_translate("CallForm", "电话界面"))
        self.label.setText(_translate("CallForm", "电话号码"))
        self.label_2.setText(_translate("CallForm", "本机号码"))
        self.btn_call.setText(_translate("CallForm", "打电话"))
        self.btn_calla.setText(_translate("CallForm", "接电话"))
        self.btn_callh.setText(_translate("CallForm", "挂电话"))
        self.btn_close.setText(_translate("CallForm", "关闭"))
		
class Callwindow(QtWidgets.QWidget):
    _signal = pyqtSignal(str)
    def __init__(self,pn):  
        super(Callwindow,self).__init__()  
        self.new=Ui_CallForm()  
        self.new.setupUi(self)
        self.new.btn_call.clicked.connect(self.call)
        self.new.btn_calla.clicked.connect(self.calla)
        self.new.btn_callh.clicked.connect(self.callh)
        self.new.btn_close.clicked.connect(self.closewindow)
        self.new.txt_cn.setText(pn)
		
    def call(self):
        text=self.new.txt_cn.text()
        if text:
            text="call,"+text
            self._signal.emit(text)
		
    def calla(self):
        text="calla,a"
        self._signal.emit(text)
		
    def callh(self):
        text="callh,h"
        self._signal.emit(text)
			
    def ShowBox(self,s):
        reply = QMessageBox.information(self, "电话拨号错误", s)
			
    def closewindow(self):
        self._signal.emit("close")
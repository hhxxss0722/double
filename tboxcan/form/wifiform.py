# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wificomset.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QMessageBox

class Ui_wcomsetform(object):
    def setupUi(self, wcomsetform):
        wcomsetform.setObjectName("wcomsetform")
        wcomsetform.resize(213, 193)
        self.label = QtWidgets.QLabel(wcomsetform)
        self.label.setGeometry(QtCore.QRect(24, 26, 54, 16))
        self.label.setObjectName("label")
        self.cb_com = QtWidgets.QComboBox(wcomsetform)
        self.cb_com.setGeometry(QtCore.QRect(90, 26, 101, 20))
        self.cb_com.setObjectName("cb_com")
        self.cb_bsp = QtWidgets.QComboBox(wcomsetform)
        self.cb_bsp.setGeometry(QtCore.QRect(90, 52, 101, 20))
        self.cb_bsp.setObjectName("cb_bsp")
        self.cb_bsp.addItem("")
        self.cb_bsp.addItem("")
        self.cb_bsp.addItem("")
        self.cb_bsp.addItem("")
        self.cb_bsp.addItem("")
        self.cb_bsp.addItem("")
        self.label_2 = QtWidgets.QLabel(wcomsetform)
        self.label_2.setGeometry(QtCore.QRect(24, 52, 54, 16))
        self.label_2.setObjectName("label_2")
        self.cb_data = QtWidgets.QComboBox(wcomsetform)
        self.cb_data.setGeometry(QtCore.QRect(90, 78, 101, 20))
        self.cb_data.setObjectName("cb_data")
        self.cb_data.addItem("")
        self.cb_data.addItem("")
        self.label_3 = QtWidgets.QLabel(wcomsetform)
        self.label_3.setGeometry(QtCore.QRect(24, 78, 54, 16))
        self.label_3.setObjectName("label_3")
        self.cb_stop = QtWidgets.QComboBox(wcomsetform)
        self.cb_stop.setGeometry(QtCore.QRect(90, 130, 101, 20))
        self.cb_stop.setObjectName("cb_stop")
        self.cb_stop.addItem("")
        self.cb_stop.addItem("")
        self.cb_stop.addItem("")
        self.label_4 = QtWidgets.QLabel(wcomsetform)
        self.label_4.setGeometry(QtCore.QRect(24, 130, 54, 16))
        self.label_4.setObjectName("label_4")
        self.cb_p = QtWidgets.QComboBox(wcomsetform)
        self.cb_p.setGeometry(QtCore.QRect(90, 104, 101, 20))
        self.cb_p.setObjectName("cb_p")
        self.cb_p.addItem("")
        self.cb_p.addItem("")
        self.cb_p.addItem("")
        self.label_5 = QtWidgets.QLabel(wcomsetform)
        self.label_5.setGeometry(QtCore.QRect(24, 104, 54, 16))
        self.label_5.setObjectName("label_5")
        self.btn_default = QtWidgets.QPushButton(wcomsetform)
        self.btn_default.setGeometry(QtCore.QRect(84, 160, 50, 23))
        self.btn_default.setObjectName("btn_default")
        self.btn_save = QtWidgets.QPushButton(wcomsetform)
        self.btn_save.setGeometry(QtCore.QRect(24, 160, 50, 23))
        self.btn_save.setObjectName("btn_save")
        self.btn_esc = QtWidgets.QPushButton(wcomsetform)
        self.btn_esc.setGeometry(QtCore.QRect(144, 160, 50, 23))
        self.btn_esc.setObjectName("btn_esc")

        self.retranslateUi(wcomsetform)
        QtCore.QMetaObject.connectSlotsByName(wcomsetform)

    def retranslateUi(self, wcomsetform):
        _translate = QtCore.QCoreApplication.translate
        wcomsetform.setWindowTitle(_translate("wcomsetform", "wifi串口设置"))
        self.label.setText(_translate("wcomsetform", "串口"))
        self.cb_bsp.setItemText(0, _translate("wcomsetform", "115200"))
        self.cb_bsp.setItemText(1, _translate("wcomsetform", "4800"))
        self.cb_bsp.setItemText(2, _translate("wcomsetform", "9600"))
        self.cb_bsp.setItemText(3, _translate("wcomsetform", "19200"))
        self.cb_bsp.setItemText(4, _translate("wcomsetform", "38400"))
        self.cb_bsp.setItemText(5, _translate("wcomsetform", "57600"))
        self.label_2.setText(_translate("wcomsetform", "波特率"))
        self.cb_data.setItemText(0, _translate("wcomsetform", "8"))
        self.cb_data.setItemText(1, _translate("wcomsetform", "7"))
        self.label_3.setText(_translate("wcomsetform", "数据位"))
        self.cb_stop.setItemText(0, _translate("wcomsetform", "1"))
        self.cb_stop.setItemText(1, _translate("wcomsetform", "1.5"))
        self.cb_stop.setItemText(2, _translate("wcomsetform", "2"))
        self.label_4.setText(_translate("wcomsetform", "停止位"))
        self.cb_p.setItemText(0, _translate("wcomsetform", "NONE"))
        self.cb_p.setItemText(1, _translate("wcomsetform", "ODD"))
        self.cb_p.setItemText(2, _translate("wcomsetform", "EVEN"))
        self.label_5.setText(_translate("wcomsetform", "校验位"))
        self.btn_default.setText(_translate("wcomsetform", "默认"))
        self.btn_save.setText(_translate("wcomsetform", "确定"))
        self.btn_esc.setText(_translate("wcomsetform", "取消"))
		
class wifisetwindow(QtWidgets.QWidget):
	_signal = pyqtSignal(str)
	def __init__(self,slist,clist):  
		super(wifisetwindow,self).__init__()  
		self.new=Ui_wcomsetform()  
		self.new.setupUi(self)
		self.new.btn_save.clicked.connect(self.saveset)
		self.new.btn_default.clicked.connect(self.defaultset)
		self.new.btn_esc.clicked.connect(self.closeform)
		self.slist=slist
		self.clist=clist
		self.initform()
		
	def initform(self):
		self.new.cb_com.addItems(self.clist)
		c=self.new.cb_com.findText(self.slist['com'])
		self.new.cb_com.setCurrentIndex(c)
		b=self.new.cb_bsp.findText(self.slist['bsp'])
		self.new.cb_bsp.setCurrentIndex(b)
		d=self.new.cb_data.findText(self.slist['data'])
		self.new.cb_data.setCurrentIndex(d)
		p=self.new.cb_p.findText(self.slist['p'])
		self.new.cb_p.setCurrentIndex(p)
		s=self.new.cb_stop.findText(self.slist['stop'])
		self.new.cb_stop.setCurrentIndex(s)
		
	def closeform(self):
		self.closewindow()
		
	def defaultset(self):
		self.initform()
			
	def saveset(self):
		c=self.new.cb_com.currentText()
		b=self.new.cb_bsp.currentText()
		d=self.new.cb_data.currentText()
		p=self.new.cb_p.currentText()
		s=self.new.cb_stop.currentText()
		setlist={}
		setlist['com']=c
		setlist['bsp']=b 
		setlist['data']=d 
		setlist['p']=p 
		setlist['s']=s 
		setstr=str(setlist).replace('\'','"')
		self._signal.emit('json@'+setstr)
			
	def ShowBox(self,s):
		reply = QMessageBox.information(self, "发送错误", s)
			
	def closewindow(self):
		self._signal.emit("event@close")
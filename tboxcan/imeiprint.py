# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imeiprint.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QMessageBox
from pyprint.pyprint import pyprint as lprint
from readxml import CheckImei,GetTbox2LablePath,GetTbox2SetPath,ReadXml
from covert62.covert62 import GetTboxNumber
import time

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
        Dialog.setWindowTitle(_translate("Dialog", "Imei打印程序"))
        self.btn_ok.setText(_translate("Dialog", "打印"))
        self.btn_reset.setText(_translate("Dialog", "重新打印"))

class Imeiwindow(QtWidgets.QWidget):
    def __init__(self):  
        super(Imeiwindow,self).__init__()  
        self.new=Ui_Dialog()
        self.new.setupUi(self)
        self.ReadSetXml()
        self.gt=GetTboxNumber()
        self.path=GetTbox2LablePath()
        print(self.path)
        self.printlable=lprint(self.path,self.batch)
        self.new.btn_ok.clicked.connect(self.startprint)

    def InitList(self,slist):
        self.new.list_print.clear()
        self.new.list_print.addItems(slist)

    def ReadSetXml(self):
        self.setpath=GetTbox2SetPath()
        self.readset=ReadXml(self.setpath)
        #print(self.readset)
        self.batch=self.readset['batch']
        self.lcount=self.readset['count']
        istr=self.readset['imei']
        self.sw=self.readset['sw']
        self.hw=self.readset['hw']
        self.pn=self.readset['pn']
        ilist=istr.split(',')
        self.imeilist=[]
        for e in ilist:
            self.imeilist.append(e.replace('\r','').replace('\n',''))
        self.InitList(self.imeilist)
        

    def GetSn(self,imei):
        simei=imei[2:11]
        lcode=imei[11:]
        icode=int(simei)
        c4=int(lcode)
        sn=self.gt.GetTboxFullCode(icode,c4)
        return sn

    def startprint(self):
        ilen=len(self.imeilist)
        c=int(self.lcount)
        self.new.btn_ok.setVisible(False)
        for i in range(0,ilen):
            time.sleep(1.5)
            imei=self.imeilist[i]
            for j in range(0,c):
                self.printimei(imei)
            self.new.list_print.takeItem(i)
            Item=QtWidgets.QListWidgetItem()
            Item.setText(imei+" ok")
            self.new.list_print.insertItem(i,Item)
        self.new.btn_ok.setVisible(True)

    def printimei(self,imei):
        if CheckImei(imei):
            try:
                slist={}
                sn=self.GetSn(imei)
                slist['imei']=imei
                slist['hw']="CS-TBOX2-V1.3"
                slist['sn']=sn
                self.printlable.printtbox2(slist)
            except Exception as e:
                print(e)

    def ShowBox(self,msg):
        reply = QMessageBox.information(self, "IMEI打印", msg, QMessageBox.Yes)
			
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "IMEI打印测试", "您确定要退出吗？", QMessageBox.Yes |
                                        QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

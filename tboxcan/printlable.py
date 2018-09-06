#coding:utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QCoreApplication,pyqtSignal
from pyprint.pyprint import pyprint as lprint
from readxml import CheckImei,GetLablePath
from form.blable import Ui_Dialog
class Printwindow(QtWidgets.QWidget):
    _signal = pyqtSignal(str)
    def __init__(self,readset):  
        super(Printwindow,self).__init__()  
        self.new=Ui_Dialog()  
        self.new.setupUi(self)
        self.readset=readset
        self.new.btn_print.clicked.connect(self.printlable)
        self.new.btn_read.clicked.connect(self.readsetxml)
        self.new.txt_imei.textChanged.connect(self.printlable)
        self.readsetxml()
        self.lableprint=lprint(self.path,self.batch)
        self.pcount=0

    def readsetxml(self):
        self.batch=self.readset['batch']
        self.path=GetLablePath()
        self.new.txt_batch.setText(self.batch)

    def printlable(self):
        imei=self.new.txt_imei.text()
        if CheckImei(imei):
            try:
                self.lableprint.printimei(imei)
                self.pcount+=1
                self.new.lab_pcount.setText(str(self.pcount))
                self.new.txt_imei.setText('')
            except Exception as e:
                self.ShowBox(str(e))
        else:
            pass

    def ShowBox(self,msg):
        reply = QMessageBox.information(self, "背壳打印", msg, QMessageBox.Yes)

    def closeEvent(self, event):
        #self.lableprint.closeprint()
        self._signal.emit('closeprint')
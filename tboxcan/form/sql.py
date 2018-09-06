# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sql.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem,QFileDialog
from emcdatabase import *
from excel.csvhelp import SaveExcel

class Ui_sqlform(object):
    def setupUi(self, sqlform):
        sqlform.setObjectName("sqlform")
        sqlform.resize(584, 308)
        self.tb_data = QtWidgets.QTableWidget(sqlform)
        self.tb_data.setGeometry(QtCore.QRect(5, 10, 571, 261))
        self.tb_data.setObjectName("tb_data")
        self.tb_data.setColumnCount(0)
        self.tb_data.setRowCount(0)
        self.widget = QtWidgets.QWidget(sqlform)
        self.widget.setGeometry(QtCore.QRect(10, 280, 395, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_head = QtWidgets.QComboBox(self.widget)
        self.cb_head.setObjectName("cb_head")
        self.horizontalLayout.addWidget(self.cb_head)
        self.btn_s = QtWidgets.QPushButton(self.widget)
        self.btn_s.setObjectName("btn_s")
        self.horizontalLayout.addWidget(self.btn_s)
        self.btn_next = QtWidgets.QPushButton(self.widget)
        self.btn_next.setObjectName("btn_next")
        self.horizontalLayout.addWidget(self.btn_next)
        self.btn_outc = QtWidgets.QPushButton(self.widget)
        self.btn_outc.setObjectName("btn_outc")
        self.horizontalLayout.addWidget(self.btn_outc)
        self.btn_uotall = QtWidgets.QPushButton(self.widget)
        self.btn_uotall.setObjectName("btn_uotall")
        self.horizontalLayout.addWidget(self.btn_uotall)

        self.retranslateUi(sqlform)
        QtCore.QMetaObject.connectSlotsByName(sqlform)

    def retranslateUi(self, sqlform):
        _translate = QtCore.QCoreApplication.translate
        sqlform.setFixedSize(sqlform.width(), sqlform.height())
        sqlform.setWindowTitle(_translate("sqlform", "数据查看"))
        self.btn_s.setText(_translate("sqlform", "上一页"))
        self.btn_next.setText(_translate("sqlform", "下一页"))
        self.btn_outc.setText(_translate("sqlform", "导出异常"))
        self.btn_uotall.setText(_translate("sqlform", "导出所有"))
#sqlform.setFixedSize(sqlform.width(), sqlform.height())
class Sqlwindow(QtWidgets.QWidget):
    _signal = pyqtSignal(str)
    def __init__(self,db):  
        super(Sqlwindow,self).__init__()  
        self.new=Ui_sqlform()  
        self.new.setupUi(self)
        self.db=db
        self.new.cb_head.activated[str].connect(self.Showdata)
        self.page=0
        self.InitTable()
        self.new.btn_s.clicked.connect(self.uppage)
        self.new.btn_next.clicked.connect(self.nextpage)
        self.new.btn_outc.clicked.connect(self.OutExC)
        self.new.btn_uotall.clicked.connect(self.OutExA)

    def InitTable(self):
        col=['id','imei','指令头','状态','数据','时间']
        self.new.tb_data.setColumnCount(6)
        self.new.tb_data.setRowCount(10)
        self.new.tb_data.setHorizontalHeaderLabels(col)
        clist=['dtu','login','l99m','emmc','eeprom','port','can0','can1','can2','qc','power']
        self.new.cb_head.addItems(clist)
        self.Showdata()

    def AddItem(self,t):
        sl=len(t)
        for i in range(0,sl):
            e=t[i]
            self.new.tb_data.setItem(i,0, QTableWidgetItem(str(e.id)))
            self.new.tb_data.setItem(i,1, QTableWidgetItem(str(e.imei)))
            self.new.tb_data.setItem(i,2, QTableWidgetItem(str(e.head)))
            self.new.tb_data.setItem(i,3, QTableWidgetItem(str(e.state)))
            self.new.tb_data.setItem(i,4, QTableWidgetItem(str(e.xml)))
            self.new.tb_data.setItem(i,5, QTableWidgetItem(str(e.date)))

    def Showdata(self):
        head=self.new.cb_head.currentText()
        sl=QueryHead(self.db,head,self.page)
        self.AddItem(sl)
    
    def uppage(self):
        if self.page>1:
            self.page-=1
            self.Showdata()
        else:
            self.ShowBox("没有更多数据了")

    def OutExC(self):
        filename=QFileDialog.getSaveFileName(self,'save file','/异常.xls')
        path=filename[0]
        if path:
            t=QueryC(self.db)
            i=SaveExcel(path,t)
            if i==1:
                self.ShowBox("文件保存成功！")
            else:
                self.ShowBox("文件保存异常，异常代码："+str(i))

    def OutExA(self):
        filename=QFileDialog.getSaveFileName(self,'save file','/all.xls')
        path=filename[0]
        if path:
            t=QueryAll(self.db)
            i=SaveExcel(path,t)
            if i==1:
                self.ShowBox("文件保存成功！")
            else:
                self.ShowBox("文件保存异常，异常代码："+str(i))

    def nextpage(self):
        self.page+=1
        self.Showdata()

    def ShowBox(self,msg):
        reply = QMessageBox.information(self, "查看数据", msg, QMessageBox.Yes)
			
    def closewindow(self):
        self._signal.emit("close")

"""
from PyQt5 import QtWidgets
import sys
def main():
	app = QtWidgets.QApplication(sys.argv)
	#dialog = QtWidgets.QMainWindow()
	tbox = Sqlwindow()
	tbox.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
"""
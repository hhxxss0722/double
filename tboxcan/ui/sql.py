# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sql.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

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
        sqlform.setWindowTitle(_translate("sqlform", "数据查看"))
        self.btn_s.setText(_translate("sqlform", "上一页"))
        self.btn_next.setText(_translate("sqlform", "下一页"))
        self.btn_outc.setText(_translate("sqlform", "导出异常"))
        self.btn_uotall.setText(_translate("sqlform", "导出所有"))


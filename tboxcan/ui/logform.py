# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'err.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_logform(object):
    def setupUi(self, logform):
        logform.setObjectName("logform")
        logform.resize(400, 300)
        self.txt_log = QtWidgets.QTextBrowser(logform)
        self.txt_log.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.txt_log.setObjectName("txt_log")

        self.retranslateUi(logform)
        QtCore.QMetaObject.connectSlotsByName(logform)

    def retranslateUi(self, logform):
        _translate = QtCore.QCoreApplication.translate
        logform.setWindowTitle(_translate("logform", "异常LOG显示"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'webprint.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_webprintForm(object):
    def setupUi(self, webprintForm):
        webprintForm.setObjectName("webprintForm")
        webprintForm.resize(219, 307)
        self.txt_show = QtWidgets.QTextEdit(webprintForm)
        self.txt_show.setGeometry(QtCore.QRect(10, 240, 191, 61))
        self.txt_show.setObjectName("txt_show")
        self.widget = QtWidgets.QWidget(webprintForm)
        self.widget.setGeometry(QtCore.QRect(10, 22, 195, 152))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
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
        self.txt_sbatch = QtWidgets.QLineEdit(self.widget)
        self.txt_sbatch.setObjectName("txt_sbatch")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_sbatch)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txt_wbatch = QtWidgets.QLineEdit(self.widget)
        self.txt_wbatch.setObjectName("txt_wbatch")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_wbatch)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txt_web = QtWidgets.QLineEdit(self.widget)
        self.txt_web.setObjectName("txt_web")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_web)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txt_tok = QtWidgets.QLineEdit(self.widget)
        self.txt_tok.setObjectName("txt_tok")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txt_tok)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.txt_total = QtWidgets.QLineEdit(self.widget)
        self.txt_total.setObjectName("txt_total")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.txt_total)
        self.widget1 = QtWidgets.QWidget(webprintForm)
        self.widget1.setGeometry(QtCore.QRect(10, 180, 158, 54))
        self.widget1.setObjectName("widget1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget1)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.btn_print = QtWidgets.QPushButton(self.widget1)
        self.btn_print.setObjectName("btn_print")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.btn_print)
        self.btn_clear = QtWidgets.QPushButton(self.widget1)
        self.btn_clear.setObjectName("btn_clear")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.btn_clear)
        self.btn_read = QtWidgets.QPushButton(self.widget1)
        self.btn_read.setObjectName("btn_read")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.btn_read)
        self.btn_web = QtWidgets.QPushButton(self.widget1)
        self.btn_web.setObjectName("btn_web")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btn_web)

        self.retranslateUi(webprintForm)
        QtCore.QMetaObject.connectSlotsByName(webprintForm)

    def retranslateUi(self, webprintForm):
        _translate = QtCore.QCoreApplication.translate
        webprintForm.setWindowTitle(_translate("webprintForm", "WEB打印界面"))
        self.label.setText(_translate("webprintForm", "IMEI"))
        self.label_2.setText(_translate("webprintForm", "设置批次"))
        self.label_3.setText(_translate("webprintForm", "网络批次"))
        self.label_4.setText(_translate("webprintForm", "测试结果"))
        self.label_5.setText(_translate("webprintForm", "已包装"))
        self.label_6.setText(_translate("webprintForm", "总抱装"))
        self.btn_print.setText(_translate("webprintForm", "打印"))
        self.btn_clear.setText(_translate("webprintForm", "清除"))
        self.btn_read.setText(_translate("webprintForm", "读取配置"))
        self.btn_web.setText(_translate("webprintForm", "web测试"))


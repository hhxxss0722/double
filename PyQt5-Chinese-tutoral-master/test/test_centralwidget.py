from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(382, 500)
        MainWindow.setMinimumSize(QtCore.QSize(382, 500))
        MainWindow.setMaximumSize(QtCore.QSize(382, 500))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 40, 18, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 30, 51, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 30, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 70, 51, 31))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 430, 71, 41))
        self.pushButton.setObjectName("pushButton")
        self.rz = QtWidgets.QTextEdit(self.centralwidget)
        self.rz.setGeometry(QtCore.QRect(10, 290, 200, 191))
        self.rz.setObjectName("rz")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(110, 120, 81, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(110, 190, 81, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(110, 240, 81, 31))
        self.label_7.setObjectName("label_7")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 110, 91, 161))
        self.groupBox.setObjectName("groupBox")
        self.xz = QtWidgets.QRadioButton(self.groupBox)
        self.xz.setGeometry(QtCore.QRect(10, 120, 89, 16))
        self.xz.setObjectName("xz")
        self.sc = QtWidgets.QRadioButton(self.groupBox)
        self.sc.setGeometry(QtCore.QRect(10, 70, 89, 16))
        self.sc.setObjectName("sc")
        self.zx = QtWidgets.QRadioButton(self.groupBox)
        self.zx.setGeometry(QtCore.QRect(10, 20, 89, 16))
        self.zx.setObjectName("zx")
        self.IP = QtWidgets.QLineEdit(self.centralwidget)
        self.IP.setGeometry(QtCore.QRect(60, 29, 131, 31))
        self.IP.setObjectName("IP")
        self.dk = QtWidgets.QLineEdit(self.centralwidget)
        self.dk.setGeometry(QtCore.QRect(230, 30, 61, 31))
        self.dk.setObjectName("dk")
        self.zh = QtWidgets.QLineEdit(self.centralwidget)
        self.zh.setGeometry(QtCore.QRect(60, 70, 131, 31))
        self.zh.setObjectName("zh")
        self.mm = QtWidgets.QLineEdit(self.centralwidget)
        self.mm.setGeometry(QtCore.QRect(230, 70, 131, 31))
        self.mm.setObjectName("mm")
        self.mm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ml = QtWidgets.QTextEdit(self.centralwidget)
        self.ml.setGeometry(QtCore.QRect(180, 120, 181, 61))
        self.ml.setObjectName("ml")
        self.bd = QtWidgets.QLineEdit(self.centralwidget)
        self.bd.setGeometry(QtCore.QRect(180, 190, 181, 31))
        self.bd.setObjectName("bd")
        self.yc = QtWidgets.QLineEdit(self.centralwidget)
        self.yc.setGeometry(QtCore.QRect(180, 240, 181, 31))
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(280, 380, 81, 21))
        self.label_8.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_8.setObjectName("label_8")
        self.yc.setObjectName("yc")
        self.zx.setChecked(True)
        self.dk.setText("22")
        self.zh.setText("root")
        self.bd.setEnabled(False)
        self.yc.setEnabled(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.zx.clicked.connect(self.zxml)
        self.sc.clicked.connect(self.sx)
        self.xz.clicked.connect(self.sx)
        self.pushButton.clicked.connect(self.linux)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def zxml(self):
        self.bd.setEnabled(False)
        self.yc.setEnabled(False)
        self.ml.setEnabled(True)

    def sx(self):
        self.bd.setEnabled(True)
        self.yc.setEnabled(True)
        self.ml.setEnabled(False)

    def linux(self):
        import os
        import sys
        aa = os.path.split(os.path.realpath(sys.argv[0]))
        self.rz.setText("")
        dk = int(self.dk.text())
        zh = self.zh.text()
        mm = self.mm.text()
        ml = self.ml.toPlainText()
        if os.path.exists(aa[0] + "/log.txt"):
            os.remove(aa[0] + "/log.txt")
        if self.mm.text() == "" and self.IP.text() == "":
            self.label_8.setText("密码不能为空！")
        elif self.IP.text() == "":
            self.label_8.setText("IP不能为空！")
        else:
            a = self.IP.text()
            self.label_8.setText("")

            def hanshu(b):
                import paramiko
                # paramiko.util.log_to_file("c:/paramiko.log")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(b, dk, zh, mm, timeout=3)
                    QApplication.processEvents()
                    if self.zx.isChecked() == True:
                        stdin, stdout, stderr = ssh.exec_command(ml)  # 执行命令行
                        self.rz.setText(self.rz.toPlainText() + b + "执行成功" + "\n")  ###多线程时这条执行不了，报错。。
                        print("a")
                        with open(aa[0] + "/log.txt", 'a') as f:
                            f.write(stdout.read().decode('utf-8') + "\n")
                        ssh.close()
                    elif self.sc.isChecked() == True:
                        ftp = ssh.open_sftp()
                        ftp.put(self.bd.text(), self.yc.text())  # 上传文件
                        self.rz.setText(self.rz.toPlainText() + b + "执行成功" + "\n")  ###多线程时这条执行不了，报错。。
                        with open(aa[0] + "/log.txt", 'a') as f:
                            f.write("执行成功\n")
                        ftp.close()
                        ssh.close()
                    elif self.xz.isChecked() == True:
                        ftp = ssh.open_sftp()
                        ftp.get(self.yc.text(), self.bd.text())  # 下载文件
                        self.rz.setText(self.rz.toPlainText() + b + "执行成功" + "\n")  ###多线程时这条执行不了，报错。。
                        with open(aa[0] + "/log.txt", 'a') as f:
                            f.write("执行成功\n")
                        ftp.close()
                        ssh.close()
                except:
                    print(b + "无法连接" + "\n")
                    self.rz.setText(self.rz.toPlainText() + b + "无法连接" + "\n")  ###多线程时这条执行不了，报错。。
                    with open(aa[0] + "/log.txt", 'a') as f:
                        f.write(b + "无法连接" + "\n" + "\n")

            sz = []
            for ip in a.split(','):
                if '-' in ip:
                    s1, s2 = ip.rsplit('.', 1)
                    start, end = map(int, s2.split('-'))
                    for num in range(start, end + 1):
                        r = s1 + '.' + str(num)
                        sz.append(r)
                        # aa=threading.Thread(target=hanshu,args=(b,))
                        # aa.start()
                        # hanshu(b)
                else:
                    sz.append(r)
                    # hanshu(ip)
            import threading
            for b in sz:
                print(b)
                t = threading.Thread(target=hanshu, args=(b,))
                t.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Linux管理工具"))
        self.label.setText(_translate("MainWindow", "IP:"))
        self.label_2.setText(_translate("MainWindow", "端口:"))
        self.label_3.setText(_translate("MainWindow", "账号:"))
        self.label_4.setText(_translate("MainWindow", "密码:"))
        self.pushButton.setText(_translate("MainWindow", "执行"))
        self.label_5.setText(_translate("MainWindow", "输入命令:"))
        self.label_6.setText(_translate("MainWindow", "本地路径:"))
        self.label_7.setText(_translate("MainWindow", "远程路径:"))
        self.groupBox.setTitle(_translate("MainWindow", "操作:"))
        self.xz.setText(_translate("MainWindow", "下载文件"))
        self.sc.setText(_translate("MainWindow", "上传文件"))
        self.zx.setText(_translate("MainWindow", "执行命令"))


from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

#coding:utf-8
#运行程序
from PyQt5 import QtWidgets
from uart import myprog
import sys
def main():
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()
	tbox = myprog(dialog)
	dialog.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
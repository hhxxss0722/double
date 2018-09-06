#coding:utf-8
#运行程序
from PyQt5 import QtWidgets
from imeiprint import Imeiwindow
import sys
def main():
	app = QtWidgets.QApplication(sys.argv)
	tbox = Imeiwindow()
	tbox.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
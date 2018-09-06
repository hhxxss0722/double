#coding:utf-8
#运行程序
from PyQt5 import QtWidgets
from emc import Emcwindow
import sys
def main():
	app = QtWidgets.QApplication(sys.argv)
	#dialog = QtWidgets.QMainWindow()
	tbox = Emcwindow()
	tbox.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
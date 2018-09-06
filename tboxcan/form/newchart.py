# coding=utf-8

import numpy as np
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation, FuncAnimation
from matplotlib.lines import Line2D
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
import time,re
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class starchart(FigureCanvas):

	def __init__(self):
		# The window
		self.fig = Figure()
		#柱形图初始化
		self.ind=np.linspace(1,12,12)
		self.ax = self.fig.add_subplot(111)
		starlist=['0',]
		self.ax.set_xticklabels(starlist)
		self.ax.set_ylabel(u'db')
		self.ax.set_ylim(0,70)
		# ax1 settings
		self.ax.set_xlabel('star')
		#画柱形图的数组
		self.x=[]
		self.xlable=[]
		self.y=[]

		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

	def init(self):
		xlable=[]
		for i in range(1,12):
			x=i
			y=i*4
			if i%2==0:
				self.ax.bar(x,y,0.9,color='green',label=str(y))
			else:
				self.ax.bar(x,y,0.9,color='blue',label=str(y))
			xlable.append(str(x))
			#print(xlable)
			self.ax.text(x,y+1,str(y),ha='center')
		self.ax.set_xticklabels(xlable)
		self.ax.set_xticks(self.ind)

	def ClearData(self):
		self.ax.clear()
		starlist=['0',]
		#self.ax.set_xticks(self.ind)
		self.ax.set_xticklabels(starlist)
		self.ax.set_ylabel(u'db')
		self.ax.set_ylim(0,70)
		self.ax.figure.canvas.draw()
		
	def ClearSet(self):
		self.xlable=[]
		self.y=[]
		self.x=[]
		
	def isnum(self,s):
		match=re.findall(r'\d+',s, re.I)
		isok=False
		if match:
			isok=True
		return isok
		
	def ShowGpsData(self,slist,startable):
		ylen=len(self.y)
		for star in slist:
			if self.isnum(star[1]):
				x=str(star[0])
				y=int(star[1])
				if ylen>=11:
					self.xlable=self.xlable[1:11]+[x]
					self.y=self.y[1:11]+[y]
					ylen=len(self.y)
				else:
					self.xlable.append(x)
					self.y.append(y)
		for i in range(1,ylen+1):
			if self.xlable[i-1] in startable:
				self.ax.bar(i,self.y[i-1],0.4,color='green',label=str(self.y[i-1]))
			else:
				self.ax.bar(i,self.y[i-1],0.4,color='blue',label=str(self.y[i-1]))
			self.ax.text(i,self.y[i-1]+1,str(self.y[i-1]),ha='center')
		self.ax.set_xticklabels(self.xlable)
		self.ax.set_ylabel(u'db')
		self.ax.set_xticks(self.ind)
		self.ax.set_ylim(0,70)
		self.ax.figure.canvas.draw()

	def Update(self):
		self.ax.clear()
		starlist=['0',]
		#self.ax.set_xticks(self.ind)
		self.ax.set_xticklabels(starlist)
		self.ax.set_ylabel(u'db')
		self.ax.set_ylim(0,70)
		self.ax.figure.canvas.draw()
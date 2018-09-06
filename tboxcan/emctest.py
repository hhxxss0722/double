# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uart.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox  
import sys
import serial.tools.list_ports as getport
import threading
import serial
from PyQt5.QtCore import * 
import time 
from form.sf import Sendwindow
from form.mainform import Ui_MainWindow
from form.call import Callwindow
from wifiset import ShowWifiSetForm,ReadSet
#from form.set import Setwindow
#from form.blable import Printwindow
#from form.webprint import WebPrintwindow
from readxml import GetPath,GetTqc,CheckImei,CheckImsi,ReadXml,GetXml,SaveXml,encodewifixml,GetWifiPath,CheckSSID
from getgps import GetGpsClass
from tfunction import CheckGps
from gps import GpsClass
from contextlib import contextmanager
from u import BackUpBin
from getssid import getssid
import json
from testclass import testclass

# 继承QThread  用于串口接收数据
class Runthread(QtCore.QThread):   
	_signal = pyqtSignal(str)  
  
	def __init__(self, parent=None):  
		super(Runthread, self).__init__()

	def init(self,com,a):
		self.com=com
		self.alive=a
  
	def __del__(self):  
		self.wait()  
  
	def run(self):  
		while self.alive.isSet():
			try:
				slen=self.com.in_waiting
				if slen>0:
					b = self.com.read(slen)
					sdata=''
					if b:
						try:
							sdata=str(b.decode('utf-8', 'replace'))
						except Exception as e:
							print(e)
							break
						self._signal.emit(sdata)
			except Exception as e:
				self._signal.emit(str(e))
				break
  
	def callback(self, msg):  
		self._signal.emit(msg)
		
#主控运行界面		
class myprog(Ui_MainWindow):

	def __init__ (self, dialog):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
		dialog.closeEvent=self.closeEvent
		self.d=dialog
		self.InitChart()
		self.ShowPorts()
		self.cominit()
		try:
			self.wificominit()
		except Exception as e:
			self.ShowBox(str(e))
			self.cb_wifi.setChecked(False)
			self.cb_wifi.setStyleSheet("background-color:red")
			self.ShowMsg("wifi串口打开失败")
		self.InitValue()
		self.HideS()
		#self.InitForm()
		#事件绑定
		self.comserch.clicked.connect(self.btn_serch)
		self.com_open.clicked.connect(self.port_open)
		self.send.clicked.connect(self.write_form)
		self.pushButton_8.clicked.connect(self.callh)
		self.pushButton_7.clicked.connect(self.calla)
		self.pushButton_6.clicked.connect(self.call_window)
		self.btn_call.clicked.connect(self.call)
		self.btn_wifi.clicked.connect(self.wifi)
		self.btn_soft.clicked.connect(self.readsoft)
		self.btn_enterqc.clicked.connect(self.enterqc)
		self.btn_lm99.clicked.connect(self.l99m)
		self.btn_adc.clicked.connect(self.adc)
		self.btn_e2r.clicked.connect(self.e2r)
		self.btn_emmc.clicked.connect(self.emmc)
		self.btn_can.clicked.connect(self.can)
		self.btn_btl.clicked.connect(self.bsp)
		self.btn_battery.clicked.connect(self.battery)
		self.btn_jz.clicked.connect(self.csystal)
		self.btn_port.clicked.connect(self.port)
		self.btn_dtu.clicked.connect(self.dtu)
		self.btn_gps.clicked.connect(self.btn_opengps)
		self.btn_agps.clicked.connect(self.btn_openagps)
		self.btn_log.clicked.connect(self.btn_opengpslog)
		self.btn_status.clicked.connect(self.btn_gpsstatus)
		self.btn_usb.clicked.connect(self.usb_backup)
		self.btn_update.clicked.connect(self.updatedata)
		self.btn_readxml.clicked.connect(self.readsetxml)
		self.action_2.triggered.connect(QCoreApplication.quit)
		self.txt_simei.textChanged.connect(self.onSimei)
		self.btn_wifiap.clicked.connect(self.btn_wifiapopen)
		self.pushButton_24.clicked.connect(self.ClearAll)
		self.cb_hd1.stateChanged.connect(self.cb_hd1check)
		self.cb_hd2.stateChanged.connect(self.cb_hd2check)
		self.cb_ecall.stateChanged.connect(self.cb_ecallcheck)
		self.cb_bcall.stateChanged.connect(self.cb_bcallcheck)
		self.cb_icall.stateChanged.connect(self.cb_icallcheck)
		self.cb_led.stateChanged.connect(self.cb_ledcheck)
		self.cb_call.stateChanged.connect(self.cb_callcheck)
		self.wifisetm.triggered.connect(self.ShowWifiSetForm)
		self.btn_wifiimei.clicked.connect(self.SetWifissid)
		self.btn_httpget.clicked.connect(self.Whttpget)
		"""
		self.action.triggered.connect(self.ShowSetForm)
		self.action_3.triggered.connect(self.ShowPrintForm)
		self.action_4.triggered.connect(self.ShowWebPrintForm)
		"""

	#上传数据
	def updatedata(self):
		if self.testtype==0:
			s=self.test.GetUrl()
			state=s['state']
			if state=='1':
				saveurl=s['saveurl']
				if saveurl=='aok':
					self.ShowMsg("数据存储数据库成功！")
				url=s['url']
				self.ShowMsg("数据上传路径:"+url)
				urlcode=s['statecode']
				try:
					ws=urlcode[200].decode('utf-8')
					if ws=='1':
						self.ShowTestInfoGreen(self.txt_update,ws)
					else:
						self.ShowTestInfoRed(self.txt_update,ws)
				except Exception as e:
					self.ShowMsg(str(e)+":"+str(urlcode))
			else:
				self.ShowTestInfoRed(self.txt_update,'state')
		else:
			pass
	#wifi串口部分
	def ShowWifiSetForm(self):
		self.ws.show()
		self.ws._signal.connect(self.callws)
		
	def callws(self,msg):
		setlist=msg.split('@')
		if len(setlist)>1:
			head=setlist[0]
			code=setlist[1]
			if head=="json":
				setdict=json.loads(code)
				self.ws.close()
				xstr=encodewifixml(setdict)
				spath=GetWifiPath()
				SaveXml(spath,xstr)
				self.wificominit()
			elif head=="event":
				if code=="close":
					self.ws.close()
					
	def wificominit(self):
		self.wthread = None
		self.walive = threading.Event()
		self.wreaddata=''
		slist=ReadSet()
		c=slist['com']
		b=slist['bsp']
		d=slist['data']
		p=slist['p']
		s=slist['stop']
		self.wcom=serial.Serial()
		self.wcom.port = c
		self.wcom.baudrate = int(b)
		self.wcom.bytesize = int(d) 
		self.wcom.stopbits = int(s)
		if p=="NONE":
			self.wcom.parity = serial.PARITY_NONE
		elif p=="ODD":
			self.wcom.parity = serial.PARITY_ODD
		elif p=="EVEN":
			self.wcom.parity = serial.PARIT_EVEN
		self.wcom.open()
		if(self.wcom.isOpen()):
			self.cb_wifi.setChecked(True)
			self.cb_wifi.setStyleSheet("background-color:yellowgreen")
			self.ShowMsg("wifi串口打开ok")
			self.StartWThread()
		else:
			self.cb_wifi.setChecked(False)
			self.cb_wifi.setStyleSheet("background-color:red")
			self.ShowMsg("wifi串口打开失败")
	#创建wifi串口线程		
	def StartWThread(self):
		# 创建线程  
		self.wthread = Runthread()  
		# 连接信号
		self.walive.set()
		self.wthread.init(self.wcom,self.walive)		
		self.wthread._signal.connect(self.wcallback)		
		# 开始线程  
		self.wthread.start()  
	#停止串口线程
	def StopWThread(self):
		if self.wthread is not None:
			self.walive.clear() 			# clear alive event for thread
			self.wthread.quit()
			self.wthread.wait()
			self.wthread.exit()
			self.wthread = None
	#关闭串口，退出线程	
	def wport_close(self):
		self.walive.clear()              # stop reader thread
		self.wthread.quit()
		self.wthread.wait()
		self.wthread.exit()
		self.wthread=None
		self.wcom.close()             # cleanup
			
	def wcallback(self,msg):
		self.wreaddata+=msg
		print(msg)
		cstr=GetTqc(self.wreaddata)
		if cstr:
			for e in cstr:
				estr=str(e)
				try:
					t=GetXml(estr)
					self.txt_show.append(u'验证数据：'+str(estr)+'\r\n')
					self.txt_show.moveCursor(QtGui.QTextCursor.End)
					for gx in t:
						self.GetTbox(gx)
				except Exception as e:
					self.ShowMsg(str(e))
				self.wreaddata=''
		self.txt_show.moveCursor(QtGui.QTextCursor.End)
		
	def wport_write(self,oid):
		if self.wcom.isOpen():
			for e in oid:
				slen=self.wcom.write(e.encode('utf-8'))
				#self.ShowMsg("wifi串口写入数据："+str(slen))
				time.sleep(0.3)
			self.ShowMsg("wifi下发数据："+oid)
			
	def SendWdata(self,id):
		if id ==0:
			self.wport_write('@861234567890123#')
		elif id ==1:
			if CheckImei(self.imei):
				ssid=getssid(self.imei)
				if self.pwd:
					self.wport_write('@'+ssid+':'+self.pwd.replace('"','')+'#')
				else:
					self.wport_write('@'+ssid+':1234567890#')
		elif id==2:
			self.wport_write('@httpget#')
			
	def SetWifissid(self):
		self.SendWdata(1)
		
	def Whttpget(self):
		self.SendWdata(2)
	#end wifi串口
		
	def cb_ledcheck(self):
		self.GetCbValue(self.cb_led)
		
	def cb_ecallcheck(self):
		self.GetCbValue(self.cb_ecall)
		
	def cb_bcallcheck(self):
		self.GetCbValue(self.cb_bcall)
		
	def cb_icallcheck(self):
		self.GetCbValue(self.cb_icall)
	
	def cb_hd1check(self):
		self.GetCbValue(self.cb_hd1)
		
	def cb_callcheck(self):
		self.GetCbValue(self.cb_call)
		
	def cb_hd2check(self):
		self.GetCbValue(self.cb_hd2)
			
	def GetCbValue(self,t):
		ck=t.checkState()
		name=t.text()
		s="0"
		if ck:
			s="1"
			t.setStyleSheet("background-color:yellowgreen")
		else:
			t.setStyleSheet("background-color:red")
		if name=="HD1":
			self.hd1=s
			self.glist['hd1']=s
			self.test.SetValues(22,self.glist)
		elif name=="HD2":
			self.hd2=s
			self.glist['hd2']=s
			self.test.SetValues(23,self.glist)
		elif name=="ELED":
			self.lecall=s
			self.glist['eled']=s
			self.test.SetValues(21,self.glist)
		elif name=="BLED":
			self.lbcall=s
			self.glist['bled']=s
			self.test.SetValues(20,self.glist)
		elif name=="ILED":
			self.licall=s
			self.glist['iled']=s 
			self.test.SetValues(19,self.glist)
		elif name=="LED":
			self.led=s
			self.glist['led']=s 
			self.test.SetValues(18,self.glist)
		elif name=="pn":
			self.callok=s
			self.glist['call']=s
			self.test.SetValues(29,self.glist)
		
	def ClearAll(self):
		self.txt_show.setText("")
		self.InitForm()
		self.InitValue()
		
	def HideS(self):
		self.txt_x.setVisible(False)
		self.txt_y.setVisible(False)
		self.txt_z.setVisible(False)
		self.txt_gid.setVisible(False)
		#self.txt_gz1.setVisible(False)
		#self.txt_gz2.setVisible(False)
		self.txt_b1.setVisible(False)
		self.txt_b2.setVisible(False)
		self.txt_b3.setVisible(False)
		self.txt_calld.setVisible(False)
		#self.txt_calla.setVisible(False)
		#self.txt_callh.setVisible(False)
		self.txt_call.setVisible(False)
		self.txt_agps.setVisible(False)
		#--------label--------#
		self.label_5.setVisible(False)
		self.label_6.setVisible(False)
		self.label_7.setVisible(False)
		self.label_8.setVisible(False)
		self.label_9.setVisible(False)
		self.label_10.setVisible(False)
		self.label_36.setVisible(False)
		self.label_37.setVisible(False)
		self.label_38.setVisible(False)
		self.label_54.setVisible(False)
		#-----------btn------#
		self.btn_gsensor.setVisible(False)
		self.btn_btl.setVisible(False)
		self.pushButton_7.setVisible(False)
		self.pushButton_8.setVisible(False)
		
	def onSimei(self):
		text=self.txt_simei.text()
		if CheckImei(text):
			self.simei=text
			self.gpson()
		
	def usb_backup(self):
		try:
			self.SendData(30)
			time.sleep(0.5)
			self.SendData(30)
			time.sleep(3)
			path="TBOX_EC20_GPS.bin"
			spath="upgrade/"
			name="dupgrade.bin"
			md5=self.md5.upper()
			s=BackUpBin(path,spath,name,md5)
			self.ShowMsg(s)
			if s=="<backup ok>":
				self.glist['backup']='1'
				self.test.SetValues(24,self.glist)
				self.ShowTestInfoGreen(self.txt_usb,s)
			else:
				self.ShowTestInfoRed(self.txt_usb,s)
			#self.SendData(31)
			#time.sleep(3)
			self.SendData(35)
		except Exception as e:
			self.ShowMsg("ERR:"+str(e))
		

	#初始化串口，发送界面	
	def cominit(self):
		self.thread = None
		self.alive = threading.Event()
		self.com=serial.Serial()
		self.sf= Sendwindow(self.com)#定义发送界面
		self.cf=Callwindow()#定义打电话界面
		self.ws=ShowWifiSetForm()#WIFI串口设置界面
		self.readdata=""#接收的数据
		#初始化checkbox
		self.cb_hd1.setStyleSheet("background-color:red")
		self.cb_hd2.setStyleSheet("background-color:red")
		self.cb_ecall.setStyleSheet("background-color:red")
		self.cb_icall.setStyleSheet("background-color:red")
		self.cb_bcall.setStyleSheet("background-color:red")
		self.cb_led.setStyleSheet("background-color:red")
		self.cb_call.setStyleSheet("background-color:red")
		#初始化定时器
		self.gpstimer = QTimer()      
		self.gpstimer.setInterval(1000)       
		#self.gpstimer.start()
		self.gpstimer.timeout.connect(self.ongpsTimerOut)
		
	def ongpsTimerOut(self):
		if self.testtype==0:
			if self.gpsint==30:
				self.gpsoff()
				self.gpsint=0
				self.ShowTestInfoRed(self.txt_gps,"Fail")
			else:
				self.gpsint+=1
		elif self.testtype==1:
			if self.gpsint==int(self.gpstime):
				self.gpsoff()
				self.gpsint=0
				self.ShowTestInfoRed(self.txt_gps,"Fail")
			else:
				self.gpsint+=1
		self.jgps.SetGpsMiao(self.gpsint)
		self.lcd.display(self.gpsint)
		
	def ShowPorts(self):
		port_list = list(serial.tools.list_ports.comports())
		if len(port_list)> 0:
			clist=[]
			for e in port_list:
				port_list_0 =list(e)
				port_serial = port_list_0[0]
				clist.append(port_serial)
			self.cb_com.addItems(clist)
			
	def write_form(self):
		self.sf.show()
		self.sf._signal.connect(self.callsf)
		
	def call_window(self):
		self.cf.show()
		self.cf._signal.connect(self.callcf)
		
	def callcf(self,msg):
		if msg:
			if msg=="close":
				self.cf.close()
			else:
				slist=msg.split(',')
				if len(slist)>1:
					head=slist[0]
					code=slist[1]
					if head=="call":
						self.ShowMsg("执行打电话！")
					elif head=="calla":
						self.ShowMsg("执行接电话！")
					elif head=="callh":
						self.ShowMsg("执行接电话！")
					self.port_write(code)
					
		
	def callsf(self,msg):
		if msg:
			if msg=="close":
				self.sf.close()
			
	def port(self):
		self.SendData(29)
		
	def ShowSetForm(self):
		self.setf.show()
		self.setf._signal.connect(self.Showsetxml)
		
	def ShowPrintForm(self):
		self.pf.show()
		self.d.hide()
		self.pf._signal.connect(self.ShowMainWindow)
		
	def ShowWebPrintForm(self):
		self.wpf.show()
		self.d.hide()
		self.wpf._signal.connect(self.ShowMainWindow)
		
	def ShowMainWindow(self,msg):
		if msg=="closeprint":
			self.d.show()
		elif msg=="closewebprint":
			self.d.show()
		
	def Showsetxml(self,msg):
		if msg=="close":
			self.setf.close()
		else:
			slist=msg.split(",")
			self.setf.close()
			if len(slist)==2:
				head=slist[0]
				if head=="save":
					sxml=slist[1]
					savexml('tboxset.xml',sxml)
					self.readsetxml()
					self.ShowBox("XML文件保存成功！")
		
	def InitValue(self):
		#初检/全检标志
		self.setpath=''
		self.readset={}
		self.testtype=0#0初检，1全检
		#读取配置参数
		self.emmcsize=''
		self.mina=''
		self.maxa=''
		self.appname=''
		self.gsmcsq=''
		self.hardware=''
		self.gpsStrength=''
		self.noboot=''
		self.minadc=''
		self.maxadc=''
		self.pcbatest=''
		self.alltest=''
		self.bootname=''
		self.communication=''
		self.noweb=''
		self.baudrate=''
		self.gsmsoft=''
		self.fram=''
		self.getstar=''
		self.serchstar=''
		self.gpstime=''
		self.batch=''
		self.qcname=''
		self.outlable=''
		self.model=''
		self.gpsonly=''
		self.readsetxml()
		#Gps判断标志
		self.isgps=False#gps判断标志
		self.isgsa=False
		self.isgsv=False
		self.isgll=False
		self.isrmc=False
		self.isgga=False
		self.gpsint=0#gps定位时间
		#END
		#上传数据
		self.upgpsS=''#gps最大信号强度值
		self.hd1=""
		self.hd2=""
		self.lecall=""
		self.lbcall=""
		self.licall=""
		self.led=""
		self.imei=""
		self.callok=""
		self.simei=""
		#测试保存类，包括上传、存储到数据库
		self.test=testclass(self.testtype,self.batch,self.model)
		self.glist={}#存储测试值
		
	def InitForm(self):
		#edittext 初始化
		self.SetEditRed(self.txt_boot)
		self.SetEditRed(self.txt_app)
		self.SetEditRed(self.txt_qc)
		self.SetEditRed(self.txt_gid)
		self.SetEditRed(self.txt_x)
		self.SetEditRed(self.txt_y)
		self.SetEditRed(self.txt_z)
		self.SetEditRed(self.txt_dtu)
		self.SetEditRed(self.txt_imei)
		self.SetEditRed(self.txt_imsi)
		self.SetEditRed(self.txt_csq1)
		self.SetEditRed(self.txt_csq2)
		self.SetEditRed(self.txt_csq3)
		self.SetEditRed(self.txt_gz1)
		self.SetEditRed(self.txt_gz2)
		self.SetEditRed(self.txt_wifis)
		self.SetEditRed(self.txt_ssid)
		self.SetEditRed(self.txt_pwd)
		self.SetEditRed(self.txt_call)
		self.SetEditRed(self.txt_calld)
		self.SetEditRed(self.txt_callh)
		self.SetEditRed(self.txt_calla)
		self.SetEditRed(self.txt_eppromr)
		self.SetEditRed(self.txt_eppromw)
		self.SetEditRed(self.txt_eppromid)
		self.SetEditRed(self.txt_eppromsize)
		self.SetEditRed(self.txt_adc1)
		self.SetEditRed(self.txt_adc2)
		self.SetEditRed(self.txt_lm99)
		self.SetEditRed(self.txt_emmcid)
		self.SetEditRed(self.txt_emmcr)
		self.SetEditRed(self.txt_emmcw)
		self.SetEditRed(self.txt_emmcc)
		self.SetEditRed(self.txt_emmcclk)
		self.SetEditRed(self.txt_c1)
		self.SetEditRed(self.txt_c2)
		self.SetEditRed(self.txt_c3)
		self.SetEditRed(self.txt_b1)
		self.SetEditRed(self.txt_b2)
		self.SetEditRed(self.txt_b3)
		self.SetEditRed(self.txt_adcc)
		self.SetEditRed(self.txt_scc)
		self.SetEditRed(self.txt_scf)
		self.SetEditRed(self.txt_usb)
		self.SetEditRed(self.txt_jz)
		self.SetEditRed(self.txt_rtc)
		self.SetEditRed(self.txt_fchrg)
		self.SetEditRed(self.txt_schrg)
		self.SetEditRed(self.txt_kl15)
		self.SetEditRed(self.txt_sbs)
		self.SetEditRed(self.txt_ecall)
		self.SetEditRed(self.txt_bcall)
		self.SetEditRed(self.txt_icall)
		self.SetEditRed(self.txt_gps)
		self.SetEditRed(self.txt_agps)
		self.SetEditRed(self.txt_end)
		self.SetEditRed(self.txt_simei)
		self.SetEditRed(self.txt_update)
		self.SetCbRed(self.cb_hd1)
		self.SetCbRed(self.cb_hd2)
		self.SetCbRed(self.cb_ecall)
		self.SetCbRed(self.cb_bcall)
		self.SetCbRed(self.cb_icall)
		self.SetCbRed(self.cb_led)
		self.SetCbRed(self.cb_call)
		
	def SetEditRed(self,s):
		s.setText("")
		s.setStyleSheet("background-color:red")
		
	def SetCbRed(self,s):
		s.setChecked(False)
		s.setStyleSheet('background-color:red')
		
	def readsetxml(self):
		try:
			self.ReadValue()
		except Exception as e:
			self.cb_read.setStyleSheet("background-color:red")
			self.ShowMsg(str(e))
			
	def ReadValue(self):
		self.setpath=GetPath()
		self.readset=ReadXml(self.setpath)
		self.md5=self.readset['md5']
		self.emmcid=self.readset['emmcid']
		self.emmcsize=self.readset['emmcsize']
		self.emmcclk=self.readset['emmcclk']
		self.mina=self.readset['mina']
		self.maxa=self.readset['maxa']
		self.appname=self.readset['app']
		self.gsmcsq=self.readset['gsmcsq']
		self.hardware=self.readset['hardware']
		self.gpsStrength=self.readset['gpsStrength']
		self.minadc=self.readset['minadc']
		self.maxadc=self.readset['maxadc']
		self.minbadc=self.readset['minbadc']
		self.maxbadc=self.readset['maxbadc']
		self.gid=self.readset['gid']
		self.pcbatest=self.readset['pcbatest']
		self.alltest=self.readset['alltest']
		self.bootname=self.readset['boot']
		self.communication=self.readset['communication']
		self.noweb=self.readset['noweb']
		self.baudrate=self.readset['BaudRate']
		self.gsmsoft=self.readset['gsmsoft']
		self.fram=self.readset['fram']
		self.getstar=self.readset['getstar']
		self.serchstar=self.readset['serchstar']
		self.gpstime=self.readset['gpstime']
		self.batch=self.readset['batch']
		self.qcname=self.readset['qc']
		self.outlable=self.readset['outlable']
		self.model=self.readset['model']
		self.e2rid=self.readset['e2rid']
		self.e2rsize=self.readset['e2rsize']
		self.ssid=self.readset['ssid']
		self.pwd=self.readset['pwd']
		self.txt_simei.setVisible(False)
		if self.alltest=='1':
			self.testtype=1
			self.txt_simei.setVisible(True)
		else:
			self.testtype=0
		self.cb_batch.clear()
		self.cb_batch.addItem(str(self.batch))
		setstr='md5:'+self.md5+'\r\n'
		setstr='emmcsize:'+self.emmcsize+'\r\n'
		setstr='emmcid:'+self.emmcid+'\r\n'
		setstr+='mina:'+self.mina+'\r\n'
		setstr+='maxa:'+self.maxa+'\r\n'
		setstr+='minbadc:'+self.minbadc+'\r\n'
		setstr+='maxbadc:'+self.maxbadc+'\r\n'
		setstr+='app:'+self.appname+'\r\n'
		setstr+='gid:'+self.gid+'\r\n'
		setstr+='gsmcsq:'+self.gsmcsq+'\r\n'
		setstr+='hardware:'+self.hardware+'\r\n'
		setstr+='gpsStrength:'+self.gpsStrength+'\r\n'
		setstr+='noboot:'+self.noboot+'\r\n'
		setstr+='minadc:'+self.minadc+'\r\n'
		setstr+='maxadc:'+self.maxadc+'\r\n'
		setstr+='pcbatest:'+self.pcbatest+'\r\n'
		setstr+='alltest:'+self.alltest+'\r\n'
		setstr+='bootname:'+self.bootname+'\r\n'
		setstr+='communication:'+self.communication+'\r\n'
		setstr+='noweb:'+self.noweb+'\r\n'
		setstr+='baudrate:'+self.baudrate+'\r\n'
		setstr+='gsmsoft:'+self.gsmsoft+'\r\n'
		setstr+='fram:'+self.fram+'\r\n'
		setstr+='getstar:'+self.getstar+'\r\n'
		setstr+='serchstar:'+self.serchstar+'\r\n'
		setstr+='gpstime:'+self.gpstime+'\r\n'
		setstr+='batch:'+self.batch+'\r\n'
		setstr+='qcname:'+self.qcname+'\r\n'
		self.outlable=''
		setstr+='model:'+self.model+'\r\n'
		setstr+='e2rid:'+self.e2rid+'\r\n'
		setstr+='e2rsize:'+self.e2rsize+'\r\n'
		setstr+='ssid:'+self.ssid+'\r\n'
		setstr+='pwd:'+self.pwd+'\r\n'
		self.jgps=GetGpsClass(self.gpsStrength,self.serchstar,self.getstar,True,False)
		self.getgps=GpsClass()
		self.cb_pcba.setChecked(True)
		self.cb_pcba.setStyleSheet("background-color:yellowgreen")
		self.cb_all.setChecked(False)
		if self.testtype==1:
			self.jgps=GetGpsClass(self.gpsStrength,self.serchstar,self.getstar,False,True)	
			self.cb_pcba.setChecked(False)
			self.cb_all.setChecked(True)
			self.cb_all.setStyleSheet("background-color:yellowgreen")
			self.cb_pcba.setStyleSheet("")
		self.cb_pcba.setEnabled(False)
		self.cb_all.setEnabled(False)
		self.ShowMsg(u'读取配置参数：\r\n'+setstr)
		self.cb_read.setStyleSheet("background-color:yellowgreen")
		self.cb_read.setChecked(True)
		#self.setf=Setwindow(self.readset)
		#self.pf=Printwindow(self.readset)
		#self.wpf=WebPrintwindow(self.readset)
			
	#初始化柱形图	
	def InitChart(self):
		self.chart.Update()
	#开始串口接收线程	
	def StartThread(self):
		# 创建线程  
		self.thread = Runthread()  
		# 连接信号
		self.alive.set()
		self.thread.init(self.com,self.alive)		
		self.thread._signal.connect(self.callbacklog)		
		# 开始线程  
		self.thread.start()  
	#停止串口线程
	def StopThread(self):
		if self.thread is not None:
			self.alive.clear() 			# clear alive event for thread
			self.thread.quit()
			self.thread.wait()
			self.thread.exit()
			self.thread = None
	#关闭串口，退出线程	
	def port_close(self):
		self.alive.clear()              # stop reader thread
		self.thread.quit()
		self.thread.wait()
		self.thread.exit()
		self.thread=None
		self.com.close()             # cleanup
	#串口接收线程绑定回调函数	
	def callbacklog(self, msg):  
		# 回调数据输出到文本框  
		self.txt_show.append(msg)
		if msg:
			self.readdata+=msg
			if self.isgps:
				cstr=CheckGps(self.readdata)
				self.ShowMsg(str(cstr))
				if cstr:
					for e in cstr:
						if self.getgps.CheckGpsBuff(e):
							self.ShowMsg(u'验证数据：'+e)
							sdata=e.split(',')
							#print("buff:",sdata)
							rdata=self.getgps.GetGpsDataList(sdata[0],sdata)
							#print("jbuff:",rdata)
							if len(rdata)>0:
								xdata=self.jgps.GetGps(rdata)
								#print(xdata)
								self.ShowGps(xdata)
						self.readdata=''
			else:
				cstr=GetTqc(self.readdata)
				if cstr:
						for e in cstr:
							estr=str(e)
							try:
								t=GetXml(estr)
								self.txt_show.append(u'验证数据：'+str(estr)+'\r\n')
								self.txt_show.moveCursor(QtGui.QTextCursor.End)
								for gx in t:
									self.GetTbox(gx)
							except Exception as e:
								self.ShowMsg(str(e))
						self.readdata=''
		self.txt_show.moveCursor(QtGui.QTextCursor.End)
		
	def ShowTest(self,s,v):
		if v=='1':
			s.setStyleSheet("background-color:yellowgreen")
		elif v=='0':
			s.setStyleSheet("background-color:red")
		s.setText(v)
		
	def ShowTestInfoGreen(self,s,v):
		s.setText(v)
		s.setStyleSheet("background-color:yellowgreen")
		
	def ShowTestInfoRed(self,s,v):
		s.setText(v)
		s.setStyleSheet("background-color:red")
	@contextmanager	
	def GetTbox(self,t):
		head=t.GetTag()
		dlist=t.GetVlist()
		if head=="dtu":#<tqc><dtu><version>EC20CFAR02A08M4G</version><imei>863010032425667</imei><imsi>460060009076264</imsi><csq>20,20,20</csq></dtu></tqc>
			dv=dlist['version']
			imei=dlist['imei']
			imsi=dlist['imsi']
			csq=dlist['csq']
			csqlist=csq.split(',')
			c1=csqlist[0]
			c2=csqlist[1]
			c3=csqlist[2]
			c=0
			if CheckImei(str(imei)):
				self.imei=imei
				self.ssid=getssid(self.imei)
				self.glist['imei']=self.imei
				self.test.SetValues(0,self.glist)
				if self.testtype==0:
					self.ShowTestInfoGreen(self.txt_imei,imei)
				elif self.testtype==1:
					if self.imei==self.simei:
						self.ShowTestInfoGreen(self.txt_imei,self.imei)
						self.ShowTestInfoGreen(self.txt_simei,self.simei)
					else:
						self.ShowTestInfoRed(self.txt_imei,imei)
			else:
				self.ShowTestInfoRed(self.txt_imei,imei)
			if CheckImsi(str(imsi)):
				self.ShowTestInfoGreen(self.txt_imsi,imsi)
				self.glist['imsi']='1'
				self.test.SetValues(30,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_imsi,imsi)
			if int(str(c1))>=int(self.gsmcsq) and int(str(c1))<=31:
				self.ShowTestInfoGreen(self.txt_csq1,c1)
				c=int(str(c1))
			else:
				self.ShowTestInfoRed(self.txt_csq1,c1)
			if int(str(c2))>=int(self.gsmcsq) and int(str(c2))<=31:
				self.ShowTestInfoGreen(self.txt_csq2,c2)
				c+=int(str(c2))
			else:
				self.ShowTestInfoRed(self.txt_csq2,c2)
			if int(str(c3))>=int(self.gsmcsq) and int(str(c3))<=31:
				self.ShowTestInfoGreen(self.txt_csq3,c3)
				c+=int(str(c3))
				self.glist['csq']=str(c//3)
				self.test.SetValues(7,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_csq3,c3)
			if str(dv)==self.gsmsoft:
				self.ShowTestInfoGreen(self.txt_dtu,dv)
				self.glist['gsoft']=dv
				self.test.SetValues(31,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_dtu,dv)
		elif head=="wifiap":
			ws=dlist['status']
			ssid=dlist['ssid']
			pwd=dlist['pass']
			self.ShowTest(self.txt_wifis,ws)
			self.glist['ws']=ws
			if str(ssid)==self.ssid:
				self.ShowTestInfoGreen(self.txt_ssid,ssid)
				self.glist['ssid']='1'
			else:
				self.ShowTestInfoRed(self.txt_ssid,ssid)
				self.glist['ssid']='0'
			if str(pwd)==self.pwd:
				self.glist['pwd']='1'
				self.ShowTestInfoGreen(self.txt_pwd,pwd)
				self.test.SetValues(5,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_pwd,pwd)
				self.glist['pwd']='0'
		elif head=="eeprom":
			w=dlist['write']
			r=dlist['read']
			eid=dlist['mid']
			esize=dlist['size']
			i=0
			self.ShowTest(self.txt_eppromw,w)
			self.ShowTest(self.txt_eppromr,r)
			if str(eid)==self.e2rid:
				self.ShowTestInfoGreen(self.txt_eppromid,eid)
				i+=1
			else:
				self.ShowTestInfoRed(self.txt_eppromid,eid)
			if str(esize)==self.e2rsize:
				self.ShowTestInfoGreen(self.txt_eppromsize,esize)
				i+=1
			else:
				self.ShowTestInfoRed(self.txt_eppromsize,esize)
			if i==2 and w=='1' and r=='1':
				self.glist['eeprom']='1'
				self.test.SetValues(28,self.glist)
		elif head=="adc":
			chl=dlist['chl']
			v=dlist['voltage']
			if chl=="1":
				v=float(v)/100
				if v>=float(self.minadc) and v<=float(self.maxadc):
					self.ShowTestInfoGreen(self.txt_adc1,str(v))
					self.glist['adc1']=str(v)
					self.test.SetValues(25,self.glist)
				else:
					self.ShowTestInfoRed(self.txt_adc1,str(v))
			elif chl=="2":
				if len(v)>2:
					v=float(v)/100
				else:
					v=int(v)
				if v>=float(self.minbadc) and v<=float(self.maxbadc):
					self.ShowTestInfoGreen(self.txt_adc2,str(v))
					self.glist['adc3']=str(v)
					self.test.SetValues(27,self.glist)
				else:
					self.ShowTestInfoRed(self.txt_adc2,str(v))
			elif chl=="3":
				v=float(v)/100
				if v>=float(self.minadc) and v<=float(self.maxadc):
					self.ShowTestInfoGreen(self.txt_calla,str(v))
					self.glist['adc2']=str(v)
					self.test.SetValues(26,self.glist)
				else:
					self.ShowTestInfoRed(self.txt_calla,str(v))
		elif head=="emmc":
			eid=dlist['id']
			ew=dlist['write']
			er=dlist['read']
			es=dlist['erase']
			clk=dlist['clk']
			i=0
			if eid == self.emmcid:
				self.ShowTestInfoGreen(self.txt_emmcid,eid)
				i+=1
			else:
				self.ShowTestInfoRed(self.txt_emmcid,eid)
			self.ShowTest(self.txt_emmcr,er)
			self.ShowTest(self.txt_emmcw,ew)
			self.ShowTest(self.txt_emmcc,es)
			if clk==self.emmcclk:
				self.ShowTestInfoGreen(self.txt_emmcclk,clk)
				i+=1
			else:
				self.ShowTestInfoRed(self.txt_emmcclk,clk)
			if i==2 and er=='1' and ew=='1' and es=='1':
				self.glist['emmc']='1'
				self.test.SetValues(14,self.glist)
		elif head=="l99m":
			all=dlist['all']
			self.ShowTest(self.txt_lm99,all)
		elif head=="can":
			chl=dlist['chl']
			sta=dlist['sta']
			if chl=="0":
				self.ShowTest(self.txt_c1,sta)
				self.glist['c1']=sta
			elif chl=="1":
				self.ShowTest(self.txt_c2,sta)
				self.glist['c2']=sta
			elif chl=="2":
				self.ShowTest(self.txt_c3,sta)
				self.glist['c3']=sta
				if self.glist['c1']=='1' and self.glist['c2']=='1' and self.glist['c3']=='1':
					self.glist['can']='1'
					self.test.SetValues(6,self.glist)
				else:
					self.glist['can']='0'
					self.test.SetValues(6,self.glist)

		elif head=="battery":
			adcc=dlist['adcc']
			scc=dlist['scc']
			scf=dlist['scf']
			sa='0'
			sc='0'
			sf='0'
			if adcc=='0':
				sa='1'
			if scc=='0':
				sc='1'
			if scf=='1':
				sf='1'
			self.glist['adcc']=adcc
			self.glist['scc']=scc
			self.glist['scf']=scf
			self.test.SetValues(35,self.glist)
			self.ShowTest(self.txt_adcc,sa)
			self.ShowTest(self.txt_scc,sc)
			self.ShowTest(self.txt_scf,sf)
		elif head=="crystal":
			m=dlist['m']
			c=dlist['c']
			self.ShowTest(self.txt_jz,m)
			self.ShowTest(self.txt_rtc,c)
			self.glist['crym']=m
			self.glist['cryc']=c
			self.test.SetValues(12,self.glist)
			self.test.SetValues(13,self.glist)
		elif head=="port":
			fchrg=dlist['fchrg']
			schrg=dlist['schrg']
			kl15=dlist['kl15']
			sbs=dlist['sbs']
			ecall=dlist['ecall']
			icall=dlist['icall']
			bcall=dlist['bcall']
			self.glist['fchrg']=fchrg
			self.glist['schrg']=schrg
			self.glist['kl15']=kl15
			self.glist['sbs']=sbs
			self.glist['esw']=ecall
			self.glist['isw']=icall
			self.glist['bsw']=bcall
			self.test.SetValues(38,self.glist)
			self.ShowTest(self.txt_fchrg,fchrg)
			self.ShowTest(self.txt_schrg,schrg)
			self.ShowTest(self.txt_kl15,kl15)
			self.ShowTest(self.txt_sbs,sbs)
			self.ShowTest(self.txt_ecall,ecall)
			self.ShowTest(self.txt_icall,icall)
			self.ShowTest(self.txt_bcall,bcall)
		elif head=="gps":
			svalue=t.GetValue()
			if svalue=="1":
				self.ShowMsg("开始GPS测试")
			elif svalue=="0":
				self.ShowMsg("退出GPS测试")
			else:
				logstate=''
				state=''
				try:
					logstate=dlist['logstate']
				except Exception as e:
					pass
				try:
					state=dlist['state']
				except Exception as e:
					pass
				if logstate=="on":
					self.ShowMsg("打开GPS LOG打印")
				elif logstate=="off":
					self.ShowMsg("关闭GPS LOG打印")
				if state=="1":
					self.ShowMsg("冷启动成功！")
		elif head=="software":
			boot=dlist['boot']
			qc=dlist['qc']
			app=dlist['app']
			if boot == self.bootname:
				self.ShowTestInfoGreen(self.txt_boot,boot)
				self.glist['boot']=boot
				self.test.SetValues(34,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_boot,boot)
			if app == self.appname:
				self.ShowTestInfoGreen(self.txt_app,app)
				self.glist['app']=app
				self.test.SetValues(33,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_app,app)
			if qc == self.qcname:
				self.ShowTestInfoGreen(self.txt_qc,qc)
				self.glist['qc']=qc
				self.test.SetValues(32,self.glist)
			else:
				self.ShowTestInfoRed(self.txt_qc,qc)
		elif head=="qc":
			qdata=t.GetValue()
			if qdata=="1":
				self.ShowMsg("------------进入QC-------------")
				if self.testtype==1:
					pass
				else:
					self.gpson()
		elif head=="setwifissid":
			qdata=t.GetValue()
			if CheckSSID(qdata):
				self.ShowMsg("-------------设置SSID-----------------")
				self.ShowTestInfoGreen(self.txt_gz1,qdata)
				self.glist['wimei']='1'
		elif head=="wifiapconnect":
			qdata=t.GetValue()
			self.glist['connect']='1'
			self.ShowTest(self.txt_gz2,qdata)
		elif head=="httpget":
			qdata=t.GetValue()
			self.ShowMsg('WIFI访问数据：'+qdata)
			if qdata:
				self.glist['hget']='1'
				self.test.SetValues(36,self.glist)
				self.ShowTestInfoGreen(self.txt_callh,qdata)
			
				
 	#打开串口	
	def port_open(self):
		try:
			t=self.com_open.text()
			if t=="打开":
				self.com.port = self.cb_com.currentText()
				self.com.baudrate = 115200
				self.com.bytesize = 8 
				self.com.stopbits = 1
				self.com.parity = serial.PARITY_NONE
				self.com.open()
				if(self.com.isOpen()):
					self.com_open.setText("关闭")
					self.com_open.setStyleSheet("background-color:gold")
					self.ShowMsg("串口打开成功")
					self.StartThread()
				else:
					self.ShowMsg("打开失败")
			elif t=="关闭":
				self.port_close()
				if(self.com.isOpen()):
					self.ShowMsg("关闭失败！")
				else:
					self.com_open.setText("打开")
					self.com_open.setStyleSheet("")
		except Exception as e:
			self.ShowBox(str(e))
				
	#call
	def call(self):
		self.SendData(8)
	def calla(self):
		self.SendData(9)
	def callh(self):
		self.SendData(10)
	#end call
	#software
	def readsoft(self):
		self.SendData(2)
	#endsoftware
	#enterqc
	def enterqc(self):
		self.SendData(1)
	#endenterqc
	#wifi
	def wifi(self):
		self.SendData(7)
	#enndwifi
	#dtu
	def dtu(self):
		self.SendData(6)
	#enddtu
	#csystal
	def csystal(self):
		self.SendData(25)
	#end csystal
	#GPS
	def ClearGps(self):
		self.isgsa=False
		self.isgsv=False
		self.isgll=False
		self.isrmc=False
		self.isgga=False
		self.gpsint=0#gps定位时间
		self.jgps.SetGpsMiao(self.gpsint)
	#显示gps数据信息
	def ShowGps(self,buff):
		if self.isrmc and self.isgsv and self.isgga and self.isgsa and self.gpsint>=11:
			self.ShowTestInfoGreen(self.txt_gps,"pass")
			self.isgps=False
			self.gpsoff()
			self.glist['gpst']=str(self.gpsint)
			self.glist['gpss']=self.upgpsS
			self.test.SetValues(3,self.glist)
			self.test.SetValues(4,self.glist)
		elif self.isrmc and self.isgsv and self.isgga and self.isgsa and self.gpsint<=11:
			self.getgps.cleardata()
			self.jgps.ClearBooL()
			self.isgsa=False
			self.isgsv=False
			self.isgll=False
			self.isrmc=False
			self.isgga=False
		else:
			if len(buff)>1:
				#print("x:",buff)
				if buff[0]=='RMC':#['RMC', '', '', '0']
					if buff[3]=="1":
						self.isrmc=True
						self.ShowMsg("#############ISRMC###########")
				elif buff[0]=='GSV':#['GSV', '00', '0', '0', '0', ['', ''], ['', ''], ['', ''], ['', '']]
					#print("gsv:",buff)
					if buff[1]=='00':
						pass
					elif buff[1]=='11':#初检
						if buff[4]=='1':
							if self.testtype==0:
								print("初检完成！！！！！！")
								self.gpsoff()
								self.glist['gpst']=str(self.gpsint)
								self.test.SetValues(4,self.glist)
								self.ShowTestInfoGreen(self.txt_gps,"Pass")
					elif buff[1]=='10':#全检
						if buff[4]=='1':
							self.isgsv=True
							self.ShowMsg("#############ISGSV###########")
					self.upgpsS=buff[2]
					self.glist['gpss']=self.upgpsS
					self.test.SetValues(3,self.glist)
					slist=[]
					slist.append(buff[5])
					slist.append(buff[6])
					slist.append(buff[7])
					slist.append(buff[8])
					self.cla(slist)
				elif buff[0]=='GGA':#['GGA', '0']
					if buff[1]=='1':
						self.isgga=True
						self.ShowMsg("#############ISGGA###########")
				elif buff[0]=='GSA':#['GSA', '0', {}]
					if buff[1]=='1':
						self.isgsa=True
						self.ShowMsg("#############ISGSA###########")
				elif buff[0]=='GLL':
					pass
				
	def cla(self,slist):
		self.chart.ClearData()
		startable=self.jgps.GetStarTable()
		self.chart.ShowGpsData(slist,startable)
		self.jgps.ClearStarTable()
		
	def btn_opengps(self):
		t=self.btn_gps.text()
		if t=="GPS":
			self.gpson()
		else:
			self.gpsoff()
			
	def btn_openagps(self):
		t=self.btn_agps.text()
		if t=="AGPS":
			self.agpson()
			self.btn_agps.setText("关闭")
			self.btn_agps.setStyleSheet("background-color:yellowgreen")
		else:
			self.agpsoff()
			self.btn_agps.setText("AGPS")
			self.btn_agps.setStyleSheet("")
			
	def btn_opengpslog(self):
		t=self.btn_log.text()
		if t=="LOG":
			self.gpslogon()
			self.btn_log.setText("关闭")
			self.btn_log.setStyleSheet("background-color:yellowgreen")
		else:
			self.gpslogoff()
			self.btn_log.setText("LOG")
			self.btn_log.setStyleSheet("")
			
	def btn_wifiapopen(self):
		t=self.btn_wifiap.text()
		if t=="WIAP":
			self.SendData(33)
			self.btn_wifiap.setText("打开")
			self.btn_wifiap.setStyleSheet("background-color:yellowgreen")
		else:
			self.SendData(34)
			self.btn_wifiap.setText("WIAP")
			self.btn_wifiap.setStyleSheet("")
			
	def btn_gpsstatus(self):
		self.gpsstatus()
		
	def gpson(self):
		self.chart.ClearData()
		self.chart.ClearSet()
		self.gpsint=0
		self.jgps.SetGpsMiao(self.gpsint)
		#self.SendData(11)
		self.SendData(32)
		time.sleep(0.5)
		#self.SendData(11)
		self.gpslogon()
		self.isgps=True
		self.gpstimer.start()
		self.btn_gps.setText("关闭")
		self.btn_gps.setStyleSheet("background-color:yellowgreen")
		
	def gpsoff(self):
		self.SendData(12)
		time.sleep(0.5)
		self.SendData(14)
		self.isgps=False
		self.gpstimer.stop()
		self.btn_gps.setText("GPS")
		self.btn_gps.setStyleSheet("")
		
	def agpson(self):
		self.SendData(15)
	
	def agpsoff(self):
		self.SendData(16)
		
	def gpslogon(self):
		self.SendData(13)
		
	def gpslogoff(self):
		self.SendData(14)
		
	def gpsstatus(self):
		self.port_write("gps -t 32 -s 38 -p 1")
		
	#END GPS
	#battery
	def battery(self):
		self.SendData(37)
		time.sleep(0.5)
		self.SendData(26)
	#end bettery
	#can
	def can(self):
		self.SendData(22)
		time.sleep(0.5)
		self.SendData(23)
		time.sleep(0.5)
		self.SendData(24)
		
	def bsp(self):
		pass
	#endcan
	#emmd
	def emmc(self):
		self.SendData(18)
	#end emmc
	#l99m
	def l99m(self):
		self.SendData(27)
	#end l99m
	#adc
	def adc(self):
		self.SendData(20)
		time.sleep(0.5)
		self.SendData(21)
		time.sleep(0.5)
		self.SendData(36)
	#end adc
	#e2r 
	def e2r(self):
		self.SendData(17)
	#end e2r
	
	#串口写数据
	def port_write(self,oid):
		if self.com.isOpen():
			slen=self.com.write(oid.encode('utf-8'))
			self.ShowMsg("写入数据长度"+str(slen))
			self.ShowMsg("下发数据："+oid)
	#发送指令	
	def SendData(self,id):
		if id == 0:
			self.port_write("Carsmartf\ntbox\r\n")
		elif id == 1:
			self.port_write("qc\r\n")
		elif id == 2:
			self.port_write("software\r\n")
		elif id == 3:
			self.port_write("led -all 1\r\n")
		elif id == 4:
			self.port_write("led -all 0\r\n")
		elif id == 5:
			self.port_write("gsensor\r\n")
		elif id == 6:
			self.port_write("dtu\r\n")
		elif id == 7:
			self.port_write("wifiap\r\n")
		elif id == 8:
			self.port_write("call\r\n")
		elif id == 9:
			self.port_write("call -a\r\n")
		elif id == 10:
			self.port_write("call -h\r\n")
		elif id == 11:
			self.port_write("gps -on\r\n")
		elif id == 12:
			self.port_write("gps -off\r\n")
		elif id == 13:
			self.port_write("gps -log on\r\n")
		elif id == 14:
			self.port_write("gps -log off\r\n")
		elif id == 15:
			self.port_write("agps -on\r\n")
		elif id == 16:
			self.port_write("agps -off\r\n")
		elif id == 17:
			self.port_write("eeprom\r\n")
		elif id == 18:
			self.port_write("emmc\r\n")
		elif id == 19:
			self.port_write("emmc -reset\r\n")
		elif id == 20:
			self.port_write("adc -chl 1\r\n")
		elif id == 21:
			self.port_write("adc -chl 2\r\n")
		elif id == 22:
			self.port_write("can -chl 0\r\n")
		elif id == 23:
			self.port_write("can -chl 1\r\n")
		elif id == 24:
			self.port_write("can -chl 2\r\n")
		elif id == 25:
			self.port_write("crystal\r\n")
		elif id == 26:
			self.port_write("battery\r\n")
		elif id == 27:
			self.port_write("l99m -all 1\r\n")
		elif id == 28:
			self.port_write("l99m -all 0\r\n")
		elif id == 29:
			self.port_write("port\r\n")
		elif id== 30:
			self.port_write("usb_detect -s 1\r\n")
		elif id == 31:
			self.port_write("usb_detect -s 0\r\n")
		elif id == 32:
			self.port_write("gps -cold\r\n")
		elif id == 33:
			self.port_write("wifiap -close\r\n")
		elif id == 34:
			self.port_write("wifiap -open\r\n")
		elif id== 35:
			self.port_write("upgrade -s 4\r\n")
		elif id == 36:
			self.port_write("adc -chl 3\r\n")
		elif id == 37:
			self.port_write("power -chl 2 -sta 1\r\n")
			
	def ShowMsg(self,c):
		self.txt_show.append(c)
		self.txt_show.moveCursor(QtGui.QTextCursor.End)
		
	def btn_serch(self):
		self.cb_com.clear()
		self.ShowPorts()
		
	def ShowBox(self,msg):
		reply = QMessageBox.information(self.d, "Tbox测试终端", msg, QMessageBox.Yes)
			
	def closeEvent(self, event):
		try:
			self.sf.close()
			self.cf.close()
			self.ws.close()
			self.wport_close()
		except Exception as e:
			self.ShowMsg(str(e))
		reply = QMessageBox.question(self.d, "Tbox测试终端", "您确定要退出吗？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()
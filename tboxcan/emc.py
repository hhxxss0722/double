# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'emc.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QMessageBox
import serial.tools.list_ports as getport
import threading
import serial
from form.sf import Sendwindow
from form.emcform import Ui_emcform
from form.sql import Sqlwindow
from uart import Runthread
from getssid import getssid
from readxml import GetPath,GetTqc,CheckImei,CheckImsi,ReadXml,GetXml,SaveXml,encodewifixml,GetWifiPath,CheckSSID,GetEMCPath,encodeemcxml,encodeemcclearxml
from emcdatabase import *
import json,time

class Emcwindow(QtWidgets.QWidget):
    def __init__(self):  
        super(Emcwindow,self).__init__()  
        self.new=Ui_emcform()  
        self.new.setupUi(self)
        self.cominit()
        self.ShowPorts()
        self.init()
		#按钮绑定
        self.new.btn_serch.clicked.connect(self.ShowPorts)
        self.new.btn_open.clicked.connect(self.port_open)
        self.new.btn_send.clicked.connect(self.write_form)
        self.new.btn_emmc.clicked.connect(self.emmc_open)
        self.new.btn_c0.clicked.connect(self.can0_open)
        self.new.btn_can1.clicked.connect(self.can1_open)
        self.new.btn_can2.clicked.connect(self.can2_open)
        self.new.btn_dtu.clicked.connect(self.ec20_open)
        self.new.btn_login.clicked.connect(self.login_open)
        self.new.btn_l99m.clicked.connect(self.l99m_open)
        self.new.btn_port.clicked.connect(self.port_all)
        self.new.btn_fill.clicked.connect(self.fill_open)
        self.new.btn_gf.clicked.connect(self.gf_open)
        self.new.btn_epprom.clicked.connect(self.eeprom_open)
        self.new.btn_sql.clicked.connect(self.query_form)
        self.new.btn_clear.clicked.connect(self.ClearXml)

    def cleardata(self):
        self.new.txt_all.setText("")

    def init(self):
        self.imei=""
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
        self.emmcid=''
        self.readsetxml()

    def readsetxml(self):
        try:
            self.ReadValue()
        except Exception as e:
            self.ShowMsg(str(e))
			
    def ReadValue(self):
        self.sqlpath="sqlite:///emcdb//emc.db"
        self.db=InitDb(self.sqlpath)
        self.sqlf= Sqlwindow(self.db)
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
        setstr+='model:'+self.model+'\r\n'
        setstr+='e2rid:'+self.e2rid+'\r\n'
        setstr+='e2rsize:'+self.e2rsize+'\r\n'
        setstr+='ssid:'+self.ssid+'\r\n'
        setstr+='pwd:'+self.pwd+'\r\n'
        self.ShowMsg(u'读取配置参数：\r\n'+setstr)
        #计数
        self.isqc=0
        self.emcpath=GetEMCPath()
        self.emcset=ReadXml(self.emcpath)
        try:
            self.emmctimes=int(self.emcset['emmc'])
            self.ShowTestInfoGreen(self.new.txt_emmc,str(self.emmctimes))
            self.emmcfailtimes=int(self.emcset['emmcf'])
            self.ShowTestInfoRed(self.new.rb_emmc,str(self.emmcfailtimes))
            self.mcutimes=int(self.emcset['mcu'])
            self.ShowTestInfoRed(self.new.txt_mcu,str(self.mcutimes))
            self.can0times=int(self.emcset['c0'])
            self.ShowTestInfoGreen(self.new.txt_c0,str(self.can0times))
            self.can0failtimes=int(self.emcset['c0f'])
            self.ShowTestInfoRed(self.new.rb_c0,str(self.can0failtimes))
            self.can1times=int(self.emcset['c1'])
            self.ShowTestInfoGreen(self.new.txt_c1,str(self.can1times))
            self.can1failtimes=int(self.emcset['c1f'])
            self.ShowTestInfoRed(self.new.rb_c1,str(self.can1failtimes))
            self.can2times=int(self.emcset['c2'])
            self.can2failtimes=int(self.emcset['c2f'])
            self.ShowTestInfoGreen(self.new.txt_c2,str(self.can2times))
            self.ShowTestInfoRed(self.new.rb_c2,str(self.can2failtimes))
            self.e2rtimes=int(self.emcset['e2r'])
            self.ShowTestInfoGreen(self.new.txt_epprom,str(self.e2rtimes))
            self.e2rfailtimes=int(self.emcset['e2rf'])
            self.ShowTestInfoRed(self.new.rb_e2r,str(self.e2rfailtimes))
            self.l99mtimes=int(self.emcset['l99m'])
            self.ShowTestInfoGreen(self.new.txt_l99m,str(self.l99mtimes))
            self.l99mfailtimes=int(self.emcset['l99mf'])
            self.ShowTestInfoRed(self.new.rb_l99m,str(self.l99mfailtimes))
            self.logintimes=int(self.emcset['login'])
            self.ShowTestInfoGreen(self.new.txt_login,str(self.logintimes))
            self.loginfailtimes=int(self.emcset['loginf'])
            self.ShowTestInfoRed(self.new.rb_login,str(self.loginfailtimes))
            self.ec20times=int(self.emcset['ec20'])
            self.ShowTestInfoGreen(self.new.txt_ec20,str(self.ec20times))
            self.ec20failtimes=int(self.emcset['ec20f'])
            self.ShowTestInfoRed(self.new.rb_ec20,str(self.ec20failtimes))
            self.porttimes=int(self.emcset['p1'])
            self.ShowTestInfoGreen(self.new.txt_port,str(self.porttimes))
            self.porttimes2=int(self.emcset['p2'])
            self.ShowTestInfoGreen(self.new.rb_port,str(self.porttimes2))
            self.ShowMsg("实验配置数据读取成功！")
        except Exception  as e:
            self.emmctimes=0#EMMC读取成功
            self.emmcfailtimes=0#emmc读取失败
            self.mcutimes=0#reset次数
            self.can0times=0
            self.can0failtimes=0
            self.can1times=0
            self.can1failtimes=0
            self.can2times=0
            self.can2failtimes=0
            self.e2rtimes=0
            self.e2rfailtimes=0
            self.l99mtimes=0
            self.l99mfailtimes=0
            self.logintimes=0
            self.loginfailtimes=0
            self.ec20times=0
            self.ec20failtimes=0
            self.porttimes=0
            self.porttimes2=0

    def ClearXml(self):
        xml=encodeemcclearxml()
        SaveXml(self.emcpath,xml)
        self.readsetxml()
    #初始化串口，发送界面	
    def cominit(self):
        self.thread = None
        self.alive = threading.Event()
        self.com=serial.Serial()
        self.sf= Sendwindow(self.com)#定义发送界面
        self.readdata=""#接收的数据
        self.ishead=False#判定是否<tqc>开头
        self.head=""#存储头内容
        self.headstart=False#判断头开始

    def ShowPorts(self):
        port_list = list(serial.tools.list_ports.comports())
        self.new.cb_com.clear()
        if len(port_list)> 0:
            clist=[]
            for e in port_list:
                port_list_0 =list(e)
                port_serial = port_list_0[0]
                clist.append(port_serial)
            self.new.cb_com.addItems(clist)

    def write_form(self):
        self.sf.show()
        self.sf._signal.connect(self.callsf)

    def callsf(self,msg):
        if msg:
            if msg=="close":
                self.sf.close()

    def query_form(self):
        self.sqlf.show()
        self.sqlf._signal.connect(self.callsqlf)

    def callsqlf(self,msg):
        if msg:
            if msg=='close':
                self.sqlf.close()

    def SaveTable(self,h,s,j):
        itime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jstr=json.dumps(j)  
        imeicode=ImeiRecord(imei=self.imei,head=h,state=s,xml=jstr,date=itime)
        s=AddImei(imeicode,self.db)
        if s=='aok':
            self.ShowMsg('Sql Add Ok')
        else:
            self.ShowMsg("Sql Add Err")

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
    def callbacklog(self,msg):
        self.new.txt_all.append(msg)
        if msg:
            self.readdata+=msg
            cstr=GetTqc(self.readdata)
            if cstr:
                for e in cstr:
                    estr=str(e)
                    try:
                        t=GetXml(estr)
                        self.new.txt_all.append(u'验证数据：'+str(estr)+'\r\n')
                        self.new.txt_all.moveCursor(QtGui.QTextCursor.End)
                        for gx in t:
                            self.GetTbox(gx)
                    except Exception as e:
                        self.ShowMsg(str(e))
                slist=self.readdata.split('\n')
                slen=len(slist)
                if slen>0:
                    self.readdata=slist[slen-1]
                else:
                    self.readdata=''
        self.new.txt_all.moveCursor(QtGui.QTextCursor.End)

    def ShowTest(self,s,v):
        if v=='1':
            s.setStyleSheet("background-color:yellowgreen")
        elif v=='0':
            s.setStyleSheet("background-color:red")
        s.setText(v)

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
            i=0
            if CheckImei(str(imei)):
                self.imei=imei
                self.ssid=getssid(self.imei)
                i+=1
            else:
                self.ShowMsg("IMEI 异常！！！")
            if CheckImsi(str(imsi)):
               i+=1
            else:
                self.ShowMsg("IMSI 异常！！！")
            if int(str(c1))>=int(self.gsmcsq) and int(str(c1))<=31:
                i+=1
            else:
                self.ShowMsg("CSQ1 异常！！！")
            if int(str(c2))>=int(self.gsmcsq) and int(str(c2))<=31:
                i+=1
            else:
                self.ShowMsg("CSQ2 异常！！！")
            if int(str(c3))>=int(self.gsmcsq) and int(str(c3))<=31:
                i+=1
            else:
                self.ShowMsg("CSQ3 异常！！！")
            if str(dv)==self.gsmsoft:
                i+=1
            else:
                self.ShowMsg("DTU软件版本 异常！！！")
            if i==6:
                self.ec20times+=1
                self.SaveTable(head,"1",dlist)
                self.emcset['ec20']=str(self.ec20times)
                self.ShowTestInfoGreen(self.new.txt_ec20,str(self.ec20times))
            else:
                self.ec20failtimes+=1
                self.SaveTable(head,"0",dlist)
                self.emcset['ec20f']=str(self.ec20failtimes)
                self.ShowTestInfoRed(self.new.rb_ec20,str(self.ec20failtimes))
        elif head=="eeprom":
            w=dlist['write']
            r=dlist['read']
            eid=dlist['mid']
            esize=dlist['size']
            i=0
            if str(eid)==self.e2rid:
                i+=1
            else:
                self.ShowMsg("EEPROM ID 异常！！！")
            if str(esize)==self.e2rsize:
                i+=1
            else:
                self.ShowMsg("EEPROM SIZE 异常！！！")
            if i==2 and w=='1' and r=='1':
                self.e2rtimes+=1
                self.SaveTable(head,"1",dlist)
                self.emcset['e2r']=str(self.e2rtimes)
                self.ShowTestInfoGreen(self.new.txt_epprom,str(self.e2rtimes))
            else:
                self.e2rfailtimes+=1
                self.SaveTable(head,"0",dlist)
                self.emcset['e2rf']=str(self.e2rfailtimes)
                self.ShowTestInfoRed(self.new.rb_e2r,str(self.e2rfailtimes))
        elif head=="adc":
            chl=dlist['chl']
            v=dlist['voltage']
            if chl=="1":
                v=float(v)/100
                if v>=float(self.minadc) and v<=float(self.maxadc):
                    self.ShowTestInfoGreen(self.txt_adc1,str(v))
                else:
                    self.ShowTestInfoRed(self.txt_adc1,str(v))
            elif chl=="2":
                if len(v)>2:
                    v=float(v)/100
                else:
                    v=int(v)
                if v>=float(self.minbadc) and v<=float(self.maxbadc):
                    self.ShowTestInfoGreen(self.txt_adc2,str(v))
                else:
                    self.ShowTestInfoRed(self.txt_adc2,str(v))
            elif chl=="3":
                v=float(v)/100
                if v>=float(self.minadc) and v<=float(self.maxadc):
                    self.ShowTestInfoGreen(self.txt_calla,str(v))
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
                i+=1
                #self.ShowTestInfoGreen(self.new.txt_emmc,eid)
            else:
                #self.ShowTestInfoRed(self.new.txt_emmc,eid)
                self.ShowMsg("EMMC ID异常！！！！")
            #self.ShowTest(self.new.txt_emmc,er)
            #self.ShowTest(self.new.txt_emmc,ew)
            #self.ShowTest(self.new.txt_emmc,es)
            if clk==self.emmcclk:
                i+=1
                #self.ShowTestInfoGreen(self.new.txt_emmc,clk)
            else:
                #self.ShowTestInfoRed(self.new.txt_emmc,clk)
                self.ShowMsg("EMMC 时钟异常！！！！")
            if i==2 and ew=='1' and er=='1' and es=='1':
                self.emmctimes+=1
                self.SaveTable(head,"1",dlist)
                self.emcset['emmc']=str(self.emmctimes)
                self.ShowTestInfoGreen(self.new.txt_emmc,str(self.emmctimes))
            else:
                self.emmcfailtimes+=1
                self.SaveTable(head,"0",dlist)
                self.emcset['emmcf']=str(self.emmcfailtimes)
                self.ShowTestInfoRed(self.new.rb_emmc,str(self.emmcfailtimes))
        elif head=="l99m":
            al=dlist['all']
            if al=='1':
                self.l99mtimes+=1
                self.SaveTable(head,"1",dlist)
                self.emcset['l99m']=str(self.l99mtimes)
                self.ShowTestInfoGreen(self.new.txt_l99m,str(self.l99mtimes))
            else:
                self.l99mfailtimes+=1
                self.SaveTable(head,"0",dlist)
                self.emcset['l99mf']=str(self.l99mfailtimes)
                self.ShowTestInfoRed(self.new.rb_l99m,str(self.l99mfailtimes))
        elif head=="can":
            chl=dlist['chl']
            sta=dlist['sta']
            if chl=="0":
                if sta=='1':
                    self.can0times+=1
                    self.SaveTable(head+"0","1",dlist)
                    self.emcset['c0']=str(self.can0times)
                    self.ShowTestInfoGreen(self.new.txt_c0,str(self.can0times))
                else:
                    self.can0failtimes+=1
                    self.SaveTable(head+"0","0",dlist)
                    self.emcset['c0f']=str(self.can0failtimes)
                    self.ShowTestInfoRed(self.new.rb_c0,str(self.can0failtimes))
            elif chl=="1":
                if sta=='1':
                    self.can1times+=1
                    self.SaveTable(head+"1","1",dlist)
                    self.emcset['c1']=str(self.can1times)
                    self.ShowTestInfoGreen(self.new.txt_c1,str(self.can1times))
                else:
                    self.can1failtimes+=1
                    self.SaveTable(head+"1","0",dlist)
                    self.emcset['c1f']=str(self.can1failtimes)
                    self.ShowTestInfoRed(self.new.rb_c1,str(self.can1failtimes))
            elif chl=="2":
                if sta=='1':
                    self.can2times+=1
                    self.SaveTable(head+"2","1",dlist)
                    self.emcset['c2']=str(self.can2times)
                    self.ShowTestInfoGreen(self.new.txt_c2,str(self.can2times))
                else:
                    self.can2failtimes+=1
                    self.SaveTable(head+"2","0",dlist)
                    self.emcset['c2f']=str(self.can2failtimes)
                    self.ShowTestInfoRed(self.new.rb_c2,str(self.can2failtimes))
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
            self.ShowTest(self.txt_adcc,sa)
            self.ShowTest(self.txt_scc,sc)
            self.ShowTest(self.txt_scf,sf)
        elif head=="port":
            fchrg=dlist['fchrg']
            schrg=dlist['schrg']
            kl15=dlist['kl15']
            sbs=dlist['sbs']
            ecall=dlist['ecall']
            icall=dlist['icall']
            bcall=dlist['bcall']
            self.ShowTest(self.new.cb_fchrg,fchrg)
            self.ShowTest(self.new.cb_chrg,schrg)
            self.ShowTest(self.new.cb_kl15,kl15)
            self.ShowTest(self.new.cb_sbs,sbs)
            self.ShowTest(self.new.cb_ecall,ecall)
            self.ShowTest(self.new.cb_icall,icall)
            self.ShowTest(self.new.cb_bcall,bcall)
            if fchrg=='1' and schrg=='1' and kl15=='0' and sbs=='1' and ecall=='1' and bcall=='1' and icall=='1':
                self.porttimes+=1
                self.SaveTable(head,"1",dlist)
                self.emcset['p1']=str(self.porttimes)
                self.ShowTestInfoGreen(self.new.txt_port,str(self.porttimes))
            else:
                self.porttimes2+=1
                self.SaveTable(head,"0",dlist)
                self.emcset['p2']=str(self.porttimes2)
                self.ShowTestInfoGreen(self.new.rb_port,str(self.porttimes2))
        elif head=="login":
            r=dlist['ret']
            if r=='1':
                self.logintimes+=1
                self.SaveTable(head,"1",dlist)
                self.emcset['login']=str(self.logintimes)
                self.ShowTestInfoGreen(self.new.txt_login,str(self.logintimes))
            else:
                self.loginfailtimes+=1
                self.SaveTable(head,"0",dlist)
                self.emcset['loginf']=str(self.loginfailtimes)
                self.ShowTestInfoRed(self.new.rb_login,str(self.loginfailtimes))
        elif head=="qc":#<tqc><qc>QC_READY</qc></tqc>
            qdata=t.GetValue()
            if qdata=="1":
                self.ShowMsg("------------进入QC-------------")
                self.isqc+=1
                if self.isqc==3:
                    self.mcutimes+=1
                    self.isqc=0
                    dlist="{\"qc\":\"1\"}"
                    self.emcset['mcu']=str(self.mcutimes)
                    self.SaveTable(head,"1",dlist)
                    self.ShowTestInfoRed(self.new.txt_mcu,str(self.mcutimes))
            elif qdata=="QC_READY":
                self.ShowMsg("____________系统启动__________________")
                #self.mcutimes+=1
                #self.emcset['mcu']=str(self.mcutimes)
                #self.ShowTestInfoGreen(self.new.txt_mcu,str(self.mcutimes))
        elif head=="power":
            chl=dlist['chl']
            sta=dlist['sta']
            if chl=="7":
                if sta=="1":
                    self.SaveTable(head,"1",dlist)
                    self.ShowTestInfoGreen(self.new.txt_gf,"开")
                elif sta=="0":
                    self.SaveTable(head,"0",dlist)
                    self.ShowTestInfoRed(self.new.txt_gf,"关")
            elif chl=="2":
                self.SaveTable(head,"1",dlist)
                self.ShowMsg("充放电开关！")
            else:
                self.ShowTestInfoRed(self.new.rb_gf,'ERR')
        SaveXml(self.emcpath,encodeemcxml(self.emcset))
		
    def ShowTestInfoGreen(self,s,v):
        s.setText(v)
        s.setStyleSheet("background-color:yellowgreen")
		
    def ShowTestInfoRed(self,s,v):
        s.setText(v)
        s.setStyleSheet("background-color:red")

    #打开串口	
    def port_open(self):
        try:
            t=self.new.btn_open.text()
            if t=="打开":
                self.com.port = self.new.cb_com.currentText()
                self.com.baudrate = 115200
                self.com.bytesize = 8 
                self.com.stopbits = 1
                self.com.parity = serial.PARITY_NONE
                self.com.open()
                if(self.com.isOpen()):
                    self.new.btn_open.setText("关闭")
                    self.new.btn_open.setStyleSheet("background-color:gold")
                    self.ShowMsg("串口打开成功")
                    self.StartThread()
                else:
                    self.ShowMsg("打开失败")
            elif t=="关闭":
                self.port_close()
                if(self.com.isOpen()):
                    self.ShowMsg("关闭失败！")
                else:
                    self.new.btn_open.setText("打开")
                    self.new.btn_open.setStyleSheet("")
        except Exception as e:
            self.ShowBox(str(e))

    def emmc_open(self):
        t=self.new.btn_emmc.text()
        if t=="emmc":
            self.SendData(0)
            self.new.btn_emmc.setText("关闭")
            self.new.btn_emmc.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(1)
            self.new.btn_emmc.setText("emmc")
            self.new.btn_emmc.setStyleSheet("")

    def port_write(self,oid):
        if self.com.isOpen():
            slen=self.com.write(oid.encode('utf-8'))
            self.ShowMsg("写入数据长度"+str(slen))
            self.ShowMsg("下发数据："+oid)

    def eeprom_open(self):
        t=self.new.btn_epprom.text()
        if t=="epprom":
            self.SendData(2)
            self.new.btn_epprom.setText("关闭")
            self.new.btn_epprom.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(3)
            self.new.btn_epprom.setText("epprom")
            self.new.btn_epprom.setStyleSheet("")

    def can0_open(self):
        t=self.new.btn_c0.text()
        if t=="CAN0":
            self.SendData(4)
            self.new.btn_c0.setText("关闭")
            self.new.btn_c0.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(5)
            self.new.btn_c0.setText("CAN0")
            self.new.btn_c0.setStyleSheet("")

    def can1_open(self):
        t=self.new.btn_can1.text()
        if t=="CAN1":
            self.SendData(6)
            self.new.btn_can1.setText("关闭")
            self.new.btn_can1.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(7)
            self.new.btn_can1.setText("CAN1")
            self.new.btn_can1.setStyleSheet("")

    def can2_open(self):
        t=self.new.btn_can2.text()
        if t=="CAN2":
            self.SendData(8)
            self.new.btn_can2.setText("关闭")
            self.new.btn_can2.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(9)
            self.new.btn_can2.setText("CAN2")
            self.new.btn_can2.setStyleSheet("")

    def ec20_open(self):
        t=self.new.btn_dtu.text()
        if t=="DTU":
            self.SendData(10)
            self.new.btn_dtu.setText("关闭")
            self.new.btn_dtu.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(11)
            self.new.btn_dtu.setText("DTU")
            self.new.btn_dtu.setStyleSheet("")

    def login_open(self):
        t=self.new.btn_login.text()
        if t=="login":
            self.SendData(12)
            self.new.btn_login.setText("关闭")
            self.new.btn_login.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(13)
            self.new.btn_login.setText("login")
            self.new.btn_login.setStyleSheet("")

    def l99m_open(self):
        t=self.new.btn_l99m.text()
        if t=="L99M":
            self.SendData(16)
            self.new.btn_l99m.setText("关闭")
            self.new.btn_l99m.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(17)
            self.new.btn_l99m.setText("L99M")
            self.new.btn_l99m.setStyleSheet("")

    def port_all(self):
        t=self.new.btn_port.text()
        if t=="PORT":
            self.SendData(14)
            self.new.btn_port.setText("关闭")
            self.new.btn_port.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(15)
            self.new.btn_port.setText("PORT")
            self.new.btn_port.setStyleSheet("")

    def fill_open(self):
        t=self.new.btn_fill.text()
        if t=="充电":
            self.SendData(20)
            self.new.btn_fill.setText("关闭")
            self.new.btn_fill.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(21)
            self.new.btn_fill.setText("充电")
            self.new.btn_fill.setStyleSheet("")

    def gf_open(self):
        t=self.new.btn_gf.text()
        if t=="功放":
            self.SendData(18)
            self.new.btn_gf.setText("关闭")
            self.new.btn_gf.setStyleSheet("background-color:gold")
        elif t=="关闭":
            self.SendData(19)
            self.new.btn_gf.setText("功放")
            self.new.btn_gf.setStyleSheet("")

    #发送指令	
    def SendData(self,id):
        if id == 0:
            self.port_write("emmc -on\r\n")
        elif id==1:
            self.port_write("emmc -off\r\n")
        elif id==2:
            self.port_write("eeprom -on\r\n")
        elif id==3:
            self.port_write("eeprom -off\r\n")
        elif id==4:
            self.port_write("can -ch0 -on\r\n")
        elif id==5:
            self.port_write("can -ch0 -off\r\n")
        elif id==6:
            self.port_write("can -ch1 -on\r\n")
        elif id==7:
            self.port_write("can -ch1 -off\r\n")
        elif id==8:
            self.port_write("can -ch2 -on\r\n")
        elif id==9:
            self.port_write("can -ch2 -off\r\n")
        elif id==10:
            self.port_write("dtu -on\r\n")
        elif id==11:
            self.port_write("dtu -off\r\n")
        elif id==12:
            self.port_write("login -on\r\n")
        elif id==13:
            self.port_write("login -off\r\n")
        elif id==14:
            self.port_write("port -on\r\n")
        elif id==15:
            self.port_write("port -off\r\n")
        elif id==16:
            self.port_write("l99m -on\r\n")
        elif id==17:
            self.port_write("l99m -off\r\n")
        elif id==18:
            self.port_write("power -chl 7 -sta 1\r\n")
        elif id==19:
            self.port_write("power -chl 7 -sta 0\r\n")
        elif id==20:
            self.port_write("power -chl 2 -sta 1\r\n")
        elif id==21:
            self.port_write("power -chl 2 -sta 0\r\n")
			
    def ShowMsg(self,c):
        self.new.txt_all.append(c)
        self.new.txt_all.moveCursor(QtGui.QTextCursor.End)

    def btn_serch(self):
        self.new.cb_com.clear()
        self.ShowPorts()

    def ShowBox(self,msg):
        reply = QMessageBox.information(self, "EMC测试", msg, QMessageBox.Yes)
			
    def closeEvent(self, event):
        try:
            self.sf.close()
        except Exception as e:
            self.ShowMsg(str(e))
        reply = QMessageBox.question(self, "EMC测试", "您确定要退出吗？", QMessageBox.Yes |
                                QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

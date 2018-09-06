#coding:utf-8
from readxml import GetWifiPath,ReadXml
from form.wifiform import wifisetwindow
import serial.tools.list_ports as getport

def ShowPorts():
	port_list = list(getport.comports())
	clist=[]
	if len(port_list)> 0:
		for e in port_list:
			port_list_0 =list(e)
			port_serial = port_list_0[0]
			clist.append(port_serial)
	return clist
	
def ReadSet():
	spath=GetWifiPath()
	slist=ReadXml(spath)
	return slist
	
def ShowWifiSetForm():
	clist=ShowPorts()
	slist=ReadSet()
	ws=wifisetwindow(slist,clist)
	return ws
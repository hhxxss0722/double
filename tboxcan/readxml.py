#coding:utf-8
import os
import re
import xml.etree.ElementTree as et
import codecs,re

class TboxSet():
    def __init__(self,tag,text):
        self.tag=tag
        self.text=text
        
    def GetTag(self):
        return self.tag
    
    def GetText(self):
        return self.text
    
class TboxValue():
    def __init__(self,tag,value):
        self.tag=tag
        self.value=value
        self.vlist={}
        
    def GetTag(self):
        return self.tag
		
    def GetValue(self):
        return self.value
    
    def GetVlist(self):
        return self.vlist
		
    def SetVlist(self,tag,text):
        self.vlist[tag]=text
        

def GetPath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\tboxset.xml'
	return rpath

def GetEMCPath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\emcset.xml'
	return rpath
	
def GetWifiPath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\wifiset.xml'
	return rpath
	
def GetLablePath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\pyprint\\IMEI2.btw'
	return rpath
	
def GetMainLablePath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\pyprint\\IMEI.btw'
	return rpath

def GetTbox2LablePath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\pyprint\\tbox2.btw'
	return rpath

def GetTbox2SetPath():
	dir=os.path.dirname(os.path.realpath(__file__))
	rpath=str(dir)+'\\pyprint\\setlabel.xml'
	return rpath

def GetDllPath():
    dir=os.path.dirname(os.path.realpath(__file__))
    rpath=str(dir)+'\\pydll\\ControlCAN.dll'
    return rpath

def GetTqc(s):
    pattern = re.compile(r'<tqc>.*?</tqc>')
    slist=re.findall(pattern, s)
    return slist

def ReadXml(spath):
    root=et.parse(spath)
    p=root.findall('.')
    xmllist={}
    for oneper in p:
        for child in oneper.getchildren():
            t=TboxSet(child.tag,child.text)
            xmllist[child.tag]=t.GetText()
    return xmllist

def GetXml(xmlstr):
    #print(xmlstr)
    root = et.fromstring(xmlstr)
    p=root.findall('.')
    xlist=[]
    for e in p:
        for child in e.getchildren():
            #print("value:",child.text)
            try:
                t=TboxValue(child.tag,child.text)
            except Exception as e:
                #print(str(e))
                t=TboxValue(child.tag,"")
            for x in child.getchildren():
                #print(x.tag,x.text)
                t.SetVlist(x.tag,x.text)
        xlist.append(t)
    return xlist

def SaveXml(path,s):
    file = codecs.open(path,'w','utf-8')
    file.write(s)
    file.close()
    
def CheckImei(s):
    isok=False
    s= re.match("86\d{13}",s)
    if str(s)=='None':
        pass
    else:
        isok=True
    return isok
	
def CheckSSID(s):
	isok=False
	if len(s)==12:
		s= re.match("CS-TBOX_[0-9A-F]{4}",s)
		if str(s)=='None':
			pass
		else:
			isok=True
	return isok

def CheckImsi(s):
    isok=False
    s= re.match("\d{15}",s)
    if str(s)=='None':
        pass
    else:
        isok=True
    return isok
	
def encodewifixml(setdict):
	c=setdict['com']
	b=setdict['bsp']
	d=setdict['data']
	p=setdict['p']
	s=setdict['s']
	xml='<?xml version="1.0" encoding="utf-8"?>\r\n'
	xml+='<carsmart>\r\n'
	xml+='<com>'+c+'</com>\r\n'
	xml+='<bsp>'+b+'</bsp>\r\n'
	xml+='<data>'+d+'</data>\r\n'
	xml+='<p>'+p+'</p>\r\n'
	xml+='<stop>'+s+'</stop>\r\n'
	xml+='</carsmart>'
	return xml

def encodeemcxml(emcset):
    emmctimes=emcset['emmc']
    emmcfailtimes=emcset['emmcf']
    mcutimes=emcset['mcu']
    can0times=emcset['c0']
    can0failtimes=emcset['c0f']
    can1times=emcset['c1']
    can1failtimes=emcset['c1f']
    can2times=emcset['c2']
    can2failtimes=emcset['c2f']
    e2rtimes=emcset['e2r']
    e2rfailtimes=emcset['e2rf']
    l99mtimes=emcset['l99m']
    l99mfailtimes=emcset['l99mf']
    logintimes=emcset['login']
    loginfailtimes=emcset['loginf']
    ec20times=emcset['ec20']
    ec20failtimes=emcset['ec20f']
    porttimes=emcset['p1']
    porttimes2=emcset['p2']
    xml='<?xml version="1.0" encoding="utf-8"?>\r\n'
    xml+='<carsmart>\r\n'
    xml+='<emmc>'+emmctimes+'</emmc>\r\n'
    xml+='<emmcf>'+emmcfailtimes+'</emmcf>\r\n'
    xml+='<mcu>'+mcutimes+'</mcu>\r\n'
    xml+='<c0>'+can0times+'</c0>\r\n'
    xml+='<c0f>'+can0failtimes+'</c0f>\r\n'
    xml+='<c1>'+can1times+'</c1>\r\n'
    xml+='<c1f>'+can1failtimes+'</c1f>\r\n'
    xml+='<c2>'+can2times+'</c2>\r\n'
    xml+='<c2f>'+can2failtimes+'</c2f>\r\n'
    xml+='<e2r>'+e2rtimes+'</e2r>\r\n'
    xml+='<e2rf>'+e2rfailtimes+'</e2rf>\r\n'
    xml+='<l99m>'+l99mtimes+'</l99m>\r\n'
    xml+='<l99mf>'+l99mfailtimes+'</l99mf>\r\n'
    xml+='<login>'+logintimes+'</login>\r\n'
    xml+='<loginf>'+loginfailtimes+'</loginf>\r\n'
    xml+='<ec20>'+ec20times+'</ec20>\r\n'
    xml+='<ec20f>'+ec20failtimes+'</ec20f>\r\n'
    xml+='<p1>'+porttimes+'</p1>\r\n'
    xml+='<p2>'+porttimes2+'</p2>\r\n'
    xml+='</carsmart>'
    return xml

def encodeemcclearxml():
    xml='<?xml version="1.0" encoding="utf-8"?>\r\n'
    xml+='<carsmart>\r\n'
    xml+='<emmc>0</emmc>\r\n'
    xml+='<emmcf>0</emmcf>\r\n'
    xml+='<mcu>0</mcu>\r\n'
    xml+='<c0>0</c0>\r\n'
    xml+='<c0f>0</c0f>\r\n'
    xml+='<c1>0</c1>\r\n'
    xml+='<c1f>0</c1f>\r\n'
    xml+='<c2>0</c2>\r\n'
    xml+='<c2f>0</c2f>\r\n'
    xml+='<e2r>0</e2r>\r\n'
    xml+='<e2rf>0</e2rf>\r\n'
    xml+='<l99m>0</l99m>\r\n'
    xml+='<l99mf>0</l99mf>\r\n'
    xml+='<login>0</login>\r\n'
    xml+='<loginf>0</loginf>\r\n'
    xml+='<ec20>0</ec20>\r\n'
    xml+='<ec20f>0</ec20f>\r\n'
    xml+='<p1>0</p1>\r\n'
    xml+='<p2>0</p2>\r\n'
    xml+='</carsmart>'
    return xml
    

"""
xmltext="<tqc><imei>123456789</imei><csq>25,26,27</csq></tqc>"
GetXml(xmltext)
spath=GetPath()
xl=ReadXml(spath)
print(xl)
"""
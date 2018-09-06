#coding:utf-8
from database import *
import time
from tfunction import GetC_TboxPcbaUrl,httpgetdata
class testclass():
	def __init__(self,testtype,batch,model):
		#上传项目
		self.imei=''
		self.model=model
		self.batch=batch
		self.gpsStrength=''
		self.gpsPosiTime=''
		self.ws=''
		self.can=''
		self.csq=''
		self.isw=''
		self.bsw=''
		self.esw=''
		self.sbs=''
		self.crym=''
		self.cryc=''
		self.emmc=''
		self.kl15=''
		self.schrg=''
		self.fcharg=''
		self.led=''
		self.iled=''
		self.bled=''
		self.eled=''
		self.hd1=''
		self.hd2=''
		self.backup=''
		self.adc1=''
		self.adc2=''
		self.adc3=''
		self.eeprom=''
		self.wifiap=''
		self.call=''
		self.imsi=''
		self.gsoft=''
		self.qc=''
		self.app=''
		self.boot=''
		self.battery=''
		#判断项目
		self.wimei=''
		self.hget=''
		self.hconnect=''
		self.adcc=''
		self.scc=''
		self.scf=''
		self.ssid=''
		self.pwd=''
		self.wifistate=''
		self.testtype=testtype
		#数据库项目
		if testtype==0:
			self.path="sqlite:///pcbadb//test.db"
		elif testtype==1:
			self.path="sqlite:///alldb//test.db"
		self.db=InitDb(self.path)
		#生成链接
		self.url=''

	def ClearAll(self):
		self.imei=''
		self.gpsStrength=''
		self.gpsPosiTime=''
		self.ws=''
		self.can=''
		self.csq=''
		self.isw=''
		self.bsw=''
		self.esw=''
		self.sbs=''
		self.crym=''
		self.cryc=''
		self.emmc=''
		self.kl15=''
		self.schrg=''
		self.fcharg=''
		self.led=''
		self.iled=''
		self.bled=''
		self.eled=''
		self.hd1=''
		self.hd2=''
		self.backup=''
		self.adc1=''
		self.adc2=''
		self.adc3=''
		self.eeprom=''
		self.wifiap=''
		self.call=''
		self.imsi=''
		self.gsoft=''
		self.qc=''
		self.app=''
		self.boot=''
		self.battery=''
		#判断项目
		self.wimei=''
		self.hget=''
		self.hconnect=''
		self.adcc=''
		self.scc=''
		self.scf=''
		self.ssid=''
		self.pwd=''
		self.wifistate=''
		self.url=''
	
	def setwifiap(self,slist):
		self.wimei=slist['wimei']
		self.hget=slist['hget']
		self.hconnect=slist['connect']
		if self.wimei=='1' and self.hget=='1' and self.hconnect=='1':
			self.wifiap='1'
		else:
			self.wifiap='0'

	def setws(self,slist):
		self.ssid=slist['ssid']
		self.pwd=slist['pwd']
		self.wifistate=slist['ws']
		if self.ssid=='1' and self.pwd=='1' and self.wifistate=='1':
			self.ws='1'
		else:
			self.ws='0' 
			
	def setbattery(self,slist):
		self.adcc=slist['adcc']
		self.scc=slist['scc']
		self.scf=slist['scf']
		if self.adcc=='0' and self.scc=='0' and self.scf=='1':
			self.battery='1'
		else:
			self.battery='0'
			
	def setimei(self,s):
		self.imei=s['imei']
 
	def setmodel(self,s):
		self.model=s['model']
		
	def setbatch(self,s):
		self.batch=s['batch']
		
	def setgpss(self,s):
		self.gpsStrength=s['gpss']
		
	def setgpst(self,s):
		self.gpsPosiTime=s['gpst']
		
	def setcan(self,s):
		self.can=s['can'] 
		
	def setcsq(self,s):
		self.csq=s['csq'] 
		
	def setisw(self,s):
		self.isw=s['isw'] 
		
	def setbsw(self,s):
		self.bsw=s['bsw'] 
		
	def setesw(self,s):
		self.esw=s['esw'] 
		
	def setsbs(self,s):
		self.sbs=s['sbs'] 
		
	def setcrym(self,s):
		self.crym=s['crym'] 
		
	def setcryc(self,s):
		self.cryc=s['cryc'] 
		
	def setemmc(self,s):
		self.emmc=s['emmc'] 

	def setport(self,s):
		self.setkl15(s)
		self.setschrg(s)
		self.setfchrg(s)
		self.setisw(s)
		self.setbsw(s)
		self.setesw(s)
		self.setsbs(s)
		
	def setkl15(self,s):
		self.kl15=s['kl15'] 
		
	def setschrg(self,s):
		self.schrg=s['schrg'] 
		
	def setfchrg(self,s):
		self.fcharg=s['fchrg'] 
		
	def setled(self,s):
		self.led=s['led'] 
		
	def setiled(self,s):
		self.iled=s['iled'] 
		
	def setbled(self,s):
		self.bled=s['bled']

	def seteled(self,s):
		self.eled=s['eled']

	def sethd1(self,s):
		self.hd1=s['hd1']

	def sethd2(self,s):
		self.hd2=s['hd2']

	def setbackup(self,s):
		self.backup=s['backup']

	def setadc1(self,s):
		self.adc1=s['adc1']

	def setadc2(self,s):
		self.adc2=s['adc2']

	def setadc3(self,s):
		self.adc3=s['adc3']

	def seteeprom(self,s):
		self.eeprom=s['eeprom']

	def setcall(self,s):
		self.call=s['call']

	def setimsi(self,s):
		self.imsi=s['imsi']

	def setgsoft(self,s):
		self.gsoft=s['gsoft']

	def setqc(self,s):
		self.qc=s['qc']

	def setapp(self,s):
		self.app=s['app']

	def setboot(self,s):
		self.boot=s['boot']
 
	def SetValues(self,argument,code):
		switcher = {
			0: self.setimei,
			1: self.setmodel,
			2: self.setbatch,
			3: self.setgpss,
			4: self.setgpst,
			5: self.setws,
			6: self.setcan,
			7: self.setcsq,
			8: self.setisw,
			9: self.setbsw,
			10: self.setesw,
			11: self.setsbs,
			12: self.setcrym,
			13: self.setcryc,
			14: self.setemmc,
			15: self.setkl15,
			16: self.setschrg,
			17: self.setfchrg,
			18: self.setled,
			19: self.setiled,
			20: self.setbled,
			21: self.seteled,
			22: self.sethd1,
			23: self.sethd2,
			24: self.setbackup,
			25: self.setadc1,
			26: self.setadc2,
			27: self.setadc3,
			28: self.seteeprom,
			29: self.setcall,
			30: self.setimsi,
			31: self.setgsoft,
			32: self.setqc,
			33: self.setapp,
			34: self.setboot,
			35: self.setbattery,
			36: self.setwifiap,
			37: self.setws,
			38: self.setport,
		}
		func = switcher.get(argument, lambda: "nothing")
		return func(code)

	def Checklen(self,s):
		isok=False
		if len(s)>0:
			isok=True
		return isok

	def CheckUrl(self):
		i=0
		errcode=''
		if self.Checklen(self.imei):
			i+=1
		else:
			errcode+='imei err\r\n'
		if self.Checklen(self.gpsStrength):
			i+=1
		else:
			errcode+='gpsStrength err\r\n'
		if self.Checklen(self.gpsPosiTime):
			i+=1
		else:
			errcode+='gpsPosiTime err\r\n'
		if self.Checklen(self.ws):
			i+=1
		else:
			errcode+='wifistate err\r\n'
		if self.Checklen(self.can):
			i+=1
		else:
			errcode+='can err\r\n'
		if self.Checklen(self.csq):
			i+=1
		else:
			errcode+='csq err\r\n'
		if self.Checklen(self.isw):
			i+=1
		else:
			errcode+='isw err\r\n'
		if self.Checklen(self.bsw):
			i+=1
		else:
			errcode+='bsw err\r\n'
		if self.Checklen(self.esw):
			i+=1
		else:
			errcode+='esw err\r\n'
		if self.Checklen(self.sbs):
			i+=1
		else:
			errcode+='sbs err\r\n'
		if self.Checklen(self.crym):
			i+=1
		else:
			errcode+='crym err\r\n'
		if self.Checklen(self.cryc):
			i+=1
		else:
			errcode+='cryc err\r\n'
		if self.Checklen(self.emmc):
			i+=1
		else:
			errcode+='emmc err\r\n'
		if self.Checklen(self.kl15):
			i+=1
		else:
			errcode+='kl15 err\r\n'
		if self.Checklen(self.schrg):
			i+=1
		else:
			errcode+='schrg err\r\n'
		if self.Checklen(self.fcharg):
			i+=1
		else:
			errcode+='fchrg err\r\n'
		if self.Checklen(self.led):
			i+=1
		else:
			errcode+='led err\r\n'
		if self.Checklen(self.iled):
			i+=1
		else:
			errcode+='iled err\r\n'
		if self.Checklen(self.bled):
			i+=1
		else:
			errcode+='bled err\r\n'
		if self.Checklen(self.eled):
			i+=1
		else:
			errcode+='eled err\r\n'
		if self.Checklen(self.hd1):
			i+=1
		else:
			errcode+='hd1 err\r\n'
		if self.Checklen(self.hd2):
			i+=1
		else:
			errcode+='hd2 err\r\n'
		if self.Checklen(self.backup):
			i+=1
		else:
			errcode+='backup err\r\n'
		if self.Checklen(self.adc1):
			i+=1
		else:
			errcode+='adc1 err\r\n'
		if self.Checklen(self.adc2):
			i+=1
		else:
			errcode+='adc2 err\r\n'
		if self.Checklen(self.adc3):
			i+=1
		else:
			errcode+='adc3 err\r\n'
		if self.Checklen(self.eeprom):
			i+=1
		else:
			errcode+='eeprom err\r\n'
		if self.Checklen(self.wifiap):
			i+=1
		else:
			errcode+='wifiap err\r\n'
		if self.Checklen(self.call):
			i+=1
		else:
			errcode+='call err\r\n'
		if self.Checklen(self.imsi):
			i+=1
		else:
			errcode+='imsi err\r\n'
		if self.Checklen(self.gsoft):
			i+=1
		else:
			errcode+='gsoft err\r\n'
		if self.Checklen(self.qc):
			i+=1
		else:
			errcode+='qc err\r\n'
		if self.Checklen(self.app):
			i+=1
		else:
			errcode+='app err\r\n'
		if self.Checklen(self.boot):
			i+=1
		else:
			errcode+='boot err\r\n'
		if self.Checklen(self.battery):
			i+=1
		else:
			errcode+='battery err\r\n'
		rlist={}
		if i==35:
			rlist['state']='1'
		else:
			rlist['state']='0'
		rlist['err']=errcode
		return rlist
		
	def GetUrl(self):
		statelist=self.CheckUrl()
		state=statelist['state']
		urllist={}
		if state=='1':
			slist={}
			slist['imei']=self.imei
			slist['model']=self.model
			slist['batch']=self.batch
			slist['gpsStrength']=self.gpsStrength
			slist['gpsPosiTime']=self.gpsPosiTime
			slist['ws']=self.ws
			slist['can']=self.can
			slist['csq']=self.csq
			slist['isw']=self.isw
			slist['bsw']=self.bsw
			slist['esw']=self.esw
			slist['sbs']=self.sbs
			slist['crym']=self.crym
			slist['cryc']=self.cryc
			slist['emmc']=self.emmc
			slist['kl15']=self.kl15
			slist['schrg']=self.schrg
			slist['fcharg']=self.fcharg
			slist['led']=self.led
			slist['iled']=self.iled
			slist['bled']=self.bled
			slist['eled']=self.eled
			slist['hd1']=self.hd1
			slist['hd2']=self.hd2
			slist['backup']=self.backup
			slist['adc1']=self.adc1
			slist['adc2']=self.adc2
			slist['adc3']=self.adc3
			slist['eeprom']=self.eeprom
			slist['wifiap']=self.wifiap
			slist['call']=self.call
			slist['imsi']=self.imsi
			slist['4gsoft']=self.gsoft
			slist['qc']=self.qc
			slist['app']=self.app
			slist['boot']=self.boot
			slist['battery']=self.battery
			self.url=GetC_TboxPcbaUrl(slist)
			gdata=httpgetdata(self.url)
			s=self.SaveUrl()
			urllist['state']='1'
			urllist['saveurl']=s
			urllist['statecode']=gdata
			urllist['url']=self.url
		else:
			urllist['state']='0'
			urllist['err']=statelist['err']
		return urllist
		
	def SaveUrl(self):
		itime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		imeicode=Imei(imei=self.imei,url=self.url,date=itime)
		s=AddImei(imeicode,self.db)
		if s=='aok':
			print('Sql Add Ok')
		else:
			print(s)
		return s
		
	def QueryImei(self,imei):
		sl=QueryImei(imei,self.db)
		return sl
		
	def CloseDb(self):
		s=CloseDb(self.db)
		if s=='cok':
			print('DB Close Ok')
		else:
			print(s)
		
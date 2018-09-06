#coding:utf-8
import urllib3
def CheckGps(charlist):
	length=len(charlist)
	isgpsstart=False
	lgpsdata=""
	glist=[]
	for i in range(0,length):
		if charlist[i]=="$" and isgpsstart==False:
			isgpsstart=True
			lgpsdata+=charlist[i]
		if isgpsstart and charlist[i]=="\n":
			lgpsdata+=charlist[i]
			lgpsdata=lgpsdata.replace("\r","").replace("\n","")
			glist.append(lgpsdata)
			lgpsdata=""
			isgpsstart=False
		elif isgpsstart and charlist[i] != '$':
			lgpsdata += charlist[i]
		elif isgpsstart and charlist[i] == '$' and len(lgpsdata)>1:
			lgpsdata=lgpsdata.replace("\r","").replace("\n","")
			glist.append(lgpsdata)
			lgpsdata=""
			lgpsdata+=charlist[i]
	return glist

def CheckCanList(clist):
	clen=len(clist)
	isok=False
	if clist[0]==0x41 or clist[0]==0x4f and clist[clen-1]==0x0a:
		isok=True
	return isok

def GetCanData(clist):
	dlist=b''
	clen=len(clist)
	if clen>7:
		dlist=clist[7:clen-2]
	return dlist

def GetGpsCanData(clist):
	dlist=b''
	clen=len(clist)
	if clen>7:
		dlist=clist[7:clen-2]
	if len(dlist)==8:
		pass
	else:
		dlist=clist[7:]
	return dlist
	
def httpgetdata(url):
	gdata={}
	try:
		http = urllib3.PoolManager()
		r = http.request('GET', url)
		s=r.status
		d=r.data
		gdata['state']=s
		gdata['data']=d
	except Exception as e:
		gdata['err']=str(e)
	return gdata
#fields={'hello': 'world'}
def httppostdata(url,f):
	gdata={}
	try:
		http = urllib3.PoolManager()
		r = http.request('POST',url,fields=f)
		s=r.status
		d=r.data
		gdata[s]=d
	except Exception as e:
		gdata['err']=str(e)
	return gdata
	
def GetTboxPcbaUrl(slist):
	http="http://www.che08.com/tcm-ice/ws/0.1/inspections/upload?proc=10&"
	imei=slist['imei']
	model=slist['model']
	batch=slist['batch']
	gpsStrength=slist['gpsStrength']
	gpsPosiTime=slist['gpsPosiTime']
	gpsSerialPort=slist['gpsSerialPort']
	can=slist['can']
	gSensorID=slist['gSensorID']
	gSensorValue=slist['gSensorValue']
	gsmStrength=slist['gsmStrength']
	gSensorInt=slist['gSensorInt']
	t_Adc=slist['t_Adc']
	crym=slist['crym']
	cryc=slist['cryc']
	emmc=slist['emmc']
	fram=slist['fram']
	watchdog=slist['watchdog']
	usb=slist['usb']
	hardware=slist['hardware']
	software=slist['software']
	led=slist['led']
	t_GsmSoft=slist['t_GsmSoft']
	http+="imei="+imei+"&model="+model+"&batch="+batch+"&gpsStrength="+gpsStrength+"&gpsPosiTime="+gpsPosiTime+"&gpsSerialPort="+gpsSerialPort+"&can="+can+"&gSensorID="+gSensorID+"&gSensorValue="+gSensorValue+"&gsmStrength="+gsmStrength+"&gSensorInt="+gSensorInt+"&t_Adc="+t_Adc+"&crym="+crym+"&cryc="+cryc+"&emmc="+emmc+"&fram="+fram+"&watchdog="+watchdog+"&usb="+usb+"&hardware="+hardware+"&software="+software+"&led="+led+"&t_GsmSoft="+t_GsmSoft
	return http
	
def GetTboxAllUrl(slist):
	http="http://www.che08.com/tcm-ice/ws/0.1/inspections/upload?proc=10&"
	imei=slist['imei']
	model=slist['model']
	gpsStrength=slist['gpsStrength']
	gpsPosiTime=slist['gpsPosiTime']
	gpsSerialPort=slist['gpsSerialPort']
	can=slist['can']
	gSensorID=slist['gSensorID']
	gSensorValue=slist['gSensorValue']
	gsmStrength=slist['gsmStrength']
	gSensorInt=slist['gSensorInt']
	t_Adc=slist['t_Adc']
	crym=slist['crym']
	cryc=slist['cryc']
	emmc=slist['emmc']
	fram=slist['fram']
	watchdog=slist['watchdog']
	usb=slist['usb']
	hardware=slist['hardware']
	software=slist['software']
	led=slist['led']
	t_GsmSoft=slist['t_GsmSoft']
	http+="imei="+imei+"&model="+model+"&gpsStrength="+gpsStrength+"&gpsPosiTime="+gpsPosiTime+"&gpsSerialPort="+gpsSerialPort+"&can="+can+"&gSensorID="+gSensorID+"&gSensorValue="+gSensorValue+"&gsmStrength="+gsmStrength+"&gSensorInt="+gSensorInt+"&t_Adc="+t_Adc+"&crym="+crym+"&cryc="+cryc+"&emmc="+emmc+"&fram="+fram+"&watchdog="+watchdog+"&usb="+usb+"&hardware="+hardware+"&software="+software+"&led="+led+"&t_GsmSoft="+t_GsmSoft
	return http
	
	
def GetC_TboxPcbaUrl(slist):
	http="http://www.che08.com/tcm-ice/ws/0.1/inspections/upload?proc=10"
	imei=slist['imei']
	model=slist['model']
	batch=slist['batch']
	gpsStrength=slist['gpsStrength']
	gpsPosiTime=slist['gpsPosiTime']
	ws=slist['ws']
	can=slist['can']
	csq=slist['csq']
	isw=slist['isw']
	bsw=slist['bsw']
	esw=slist['esw']
	sbs=slist['sbs']
	crym=slist['crym']
	cryc=slist['cryc']
	emmc=slist['emmc']
	kl15=slist['kl15']
	schrg=slist['schrg']
	fchrg=slist['fcharg']
	led=slist['led']
	iled=slist['iled']
	bled=slist['bled']
	eled=slist['eled']
	hd1=slist['hd1']
	hd2=slist['hd2']
	backup=slist['backup']
	adc1=slist['adc1']
	adc2=slist['adc2']
	adc3=slist['adc3']
	eeprom=slist['eeprom']
	wifiap=slist['wifiap']
	call=slist['call']
	imsi=slist['imsi']
	gsoft=slist['4gsoft']
	qc=slist['qc']
	app=slist['app']
	boot=slist['boot']
	battery=slist['battery']
	http+='&imei='+imei
	http+='&model='+model
	http+='&batch='+batch
	http+='&ws='+ws
	http+='&csq='+csq
	http+='&isw='+isw
	http+='&bsw='+bsw
	http+='&esw='+esw
	http+='&sbs='+sbs
	http+='&Kl15='+kl15
	http+='&schrg='+schrg
	http+='&fchrg='+fchrg
	http+='&ILED='+iled
	http+='&BLED='+bled
	http+='&ELED='+eled
	http+='&HD2='+hd2
	http+='&HD1='+hd1
	http+='&Backup='+backup
	http+='&Adc3='+adc3
	http+='&Adc2='+adc2
	http+='&Adc1='+adc1
	http+='&eeprom='+eeprom
	http+='&wifiap='+wifiap
	http+='&call='+call
	http+='&imsi='+imsi
	http+='&4gsoft='+gsoft
	http+='&qc='+qc
	http+='&app='+app
	http+='&bt='+boot
	http+='&battery='+battery
	http+='&emmc='+emmc
	http+='&cryc='+cryc
	http+='&crym='+crym
	http+='&can='+can
	http+='&led='+led
	http+='&gpsStrength='+gpsStrength
	http+='&gpsPosiTime='+gpsPosiTime
	return http
	
"""	
url="http://www.che08.com/tcm-ice/ws/0.1/inspections/upload?proc=10&imei=861234567890235&model=tbox&batch=160308XJ&gpsStrength=38&gpsPosiTime=30&gpsSerialPort=1&can=1&gSensorID=74&gSensorValue=10&gsmStrength=18&gSensorInt=2&t_Adc=12.00&crym=1&cryc=1&emmc=1&fram=1&watchdog=1&usb=1&hardware=1.0&software=1&led=1&t_GsmSoft=L810_V5G.0D.00.01_T04"
r=httpgetdata(url)
print(r)
http://www.che08.com/tcm-ice/ws/0.1/inspections/query?imei=
http://www.che08.com/tcm-ice/ws/0.1/device/status?imei=863010032423175
"""
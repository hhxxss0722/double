#coding:utf-8
def getssid(imei):
	imei=imei[7:15]
	s=int(imei)
	code=''
	for i in range(0,4):
		scode=s%16
		sl=hex(scode).split('x')
		code+=sl[1]
		s//=16
	ssid='CS-TBOX_'+code.upper()
	#print(ssid)
	return ssid
"""
imei='863010032423027'
getssid(imei)
863010032423175
"""
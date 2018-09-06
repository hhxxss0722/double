#coding:utf-8
import re

class GpsClass(object):
	def __init__(self):
		self.isgga=False
		self.isgll=False
		self.isgsa=False
		self.isrmc=False
		self.weishuliang = ''
		self.gpsqiang = ''
		self.jiexiweixingshuliang = ''

	def isnum(self,s):
		match=re.findall(r'\d+',s, re.I)
		isok=False
		if match:
			isok=True
		return isok
	
	def CheckGpsBuff(self,buff):
		isok = False
		if len(buff.lstrip())==(buff.find('*')+2):
			pass
		else:
			crc=0
			for ch in buff:
				if ch=='$':
					pass
				elif ch=='*':
					break
				else:
					if crc==0:
						crc=ord(ch)
					else:
						crc=crc^ord(ch)
			try:
				#print("------------s---------------")
				#print(buff)
				#print("@@:",buff.find('*')+3)
				#print("##:",len(buff.lstrip()))
				#print("**:",str(hex(crc)))
				#print("------------e---------------")
				if buff.find('*')+3==len(buff.lstrip()):
					length=buff.find('*')
					s=buff[length+1]+buff[length+2]
					scode=(str(hex(crc))[2:]).upper()
					if len(scode)==2:
						pass
					else:
						scode="0"+scode
					if s==scode:
						isok=True
			except Exception as e:
				print("gpsErr:",str(e))
		return isok
		
	def IsNullOrEmpty(self,s):
		isok=True
		if s is not None and len(s)>0:
			isok=False
		return isok
		
	def GetGpsDataList(self,head,buff):
		data = []
		if head=="$GPGSA": #当前卫星信息
			data = self.getgsa(buff)
		elif head=="$GNGSA":#当前卫星信息
			data = self.getgsa(buff);
		elif head=="$GPGSV":#可见卫星信息
			data = self.getgsv(buff)
		elif head=="$GLGSV":#可见卫星信息
			data = self.getgsv(buff)
		elif head=="$GPGGA":#GPS定位信息
			data = self.getgga(buff)
		elif head=="$GNGGA":
			data = self.getgga(buff)
		elif head=="$GPRMC":#推荐定位信息
			data = self.getrmc(buff)
		elif head=="$GNRMC":#推荐定位信息
			data = self.getrmc(buff)
		elif head=="$GPVTG":#地面速度信息
			pass
		elif head=="$GPGLL":#地面速度信息
			data = self.getgll(buff)
		elif head=="$GNGLL":#地面速度信息
			data = self.getgll(buff)
		else:
			pass
		return data
		
	def getgsa(self,buff):
		gsa = [0 for x in range(0, 19)]
		starlist = [0 for x in range(0, 15)]
		linshimoshi = ''
		linshileixing = ''
		moshi = ''
		leixing = ''
		linshimoshi = buff[1]
		if not self.IsNullOrEmpty(buff[2]):
			linshileixing = buff[2]
		for i in range(0,12):
			if not self.IsNullOrEmpty(buff[i+3]):
				starlist[i]=buff[i+3]
		if not self.IsNullOrEmpty(buff[15]):
			starlist[12]=buff[15]
		if not self.IsNullOrEmpty(buff[16]):
			starlist[13]=buff[16]
		if not self.IsNullOrEmpty(buff[17]):
			starlist[14]=buff[17][0:buff[17].find('*')]
		if linshimoshi == 'M':
			moshi = "手动";
		elif linshimoshi == "A":
			moshi = "自动"
		if linshileixing == "1":
			leixing = "未定位"
		elif linshileixing == "2":
			leixing = "2D"
			self.isgsa = True
		elif linshileixing == "3":
			leixing = "3D"
			self.isgsa = True
		if len(moshi)>0:
			pass
		if len(leixing)> 0:
			pass
		gsa[0] = "GSA"
		gsa[1] = moshi
		gsa[2] = leixing
		if self.isgsa:
			gsa[3] = "1"
		else:
			gsa[3] = "0"
		gsa[4] = starlist[0]
		gsa[5] = starlist[1]
		gsa[6] = starlist[2]
		gsa[7] = starlist[3]
		gsa[8] = starlist[4]
		gsa[9] = starlist[5]
		gsa[10] = starlist[6]
		gsa[11] = starlist[7]
		gsa[12] = starlist[8]
		gsa[13] = starlist[9]
		gsa[14] = starlist[10]
		gsa[15] = starlist[11]
		gsa[16] = starlist[12]
		gsa[17] = starlist[13]
		gsa[18] = starlist[14]
		return gsa
			
	def getgsv(self,buff):
		gsv = [0 for x in range(0, 19)]
		weixingshu = ''
		wei1 = ''
		wei1y = ''
		wei1f = ''
		wei1qiang = ''
		wei2 = ''
		wei2y = ''
		wei2f = ''
		wei2qiang = ''
		wei3 = ''
		wei3y = ''
		wei3f = ''
		wei3qiang = ''
		wei4 = ''
		wei4y = ''
		wei4f = ''
		wei4qiang = ''
		length=len(buff)
		if	len(buff) > 3:
			if self.isnum(buff[3]):
				weixingshu = buff[3]
		if len(weixingshu) == 2:
			if len(self.weishuliang) > 0:
				if int(self.weishuliang) > int(weixingshu):
					pass
				else:
					self.weishuliang = weixingshu
			else:
				self.weishuliang = weixingshu
		for i in range(0,length):
			if i==4:
				if self.isnum(buff[4]):
					wei1=buff[4]
			elif i==5:
				if self.isnum(buff[5]):
					wei1y=buff[5]
			elif i==6:
				if self.isnum(buff[6]):
					wei1f=buff[6]
			elif i==7:
				if i == length-1:
					wei1qiang=buff[7][0:buff[7].find('*')]
					break
				elif self.isnum(buff[7]):      
					wei1qiang =buff[7]
			elif i == 8:
				wei2 = buff[8]
			elif i == 9:#仰角
				if self.isnum(buff[9]):
					wei2y = buff[9]
			elif i == 10:#方位角
				if self.isnum(buff[10]):
					wei2f = buff[10]
			elif i == 11:
				if i == length-1:
					wei2qiang=buff[11][0:buff[11].find('*')]
					break;
				elif self.isnum(buff[11]):
					wei2qiang = buff[11]
			elif i== 12:
				wei3 = buff[12]
			elif i == 13:#仰角
				if self.isnum(buff[13]):
					wei3y = buff[13]
			elif i == 14:#方位角
				if self.isnum(buff[14]):
					wei3f = buff[14]
			elif i == 15:
				if i == length-1:
					wei3qiang=buff[15][0:buff[15].find('*')]
					break
				elif self.isnum(buff[15]):
					wei3qiang = buff[15]
			elif i == 16:
				wei4 = buff[16]
			elif i == 17:
				if self.isnum(buff[17]):
					wei4y = buff[17]
			elif i == 18:
				if self.isnum(buff[18]):
					wei4f = buff[18]
			elif i == 19:
				if i == length-1:
					wei4qiang=buff[19][0:buff[19].find("*")]
					break;
				elif self.isnum(buff[19]):
					wei4qiang = buff[19]
		qiang1 = 0
		qiang2 = 0
		qiang3 = 0
		qiang4 = 0
		if len(wei1qiang) == 2:
			qiang1 = int(wei1qiang)
		if len(wei2qiang) == 2:
			qiang2 = int(wei2qiang)
		if len(wei3qiang) == 2:
			qiang3 = int(wei3qiang)
		if len(wei4qiang) == 2:
			qiang4 = int(wei4qiang)
		if qiang1 > qiang2:
			if qiang1 > qiang3:
				if qiang1 > qiang4:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang1:
							pass
						else:
							self.gpsqiang = str(qiang1)
					else:
						self.gpsqiang = str(qiang1)
				else:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang4:
							pass
						else:
							self.gpsqiang = str(qiang4)
					else:
						self.gpsqiang = str(qiang4)
			else:
				if qiang3 > qiang4:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang3:
							pass
						else:
							self.gpsqiang = str(qiang3)
					else:
						self.gpsqiang = str(qiang3)
				else:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang4:
							pass
						else:
							self.gpsqiang = str(qiang4)
					else:
						self.gpsqiang = str(qiang4)
		else:
			if qiang2 > qiang3:
				if qiang2 > qiang4:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang2:
							pass
						else:
							self.gpsqiang = str(qiang2)
					else:
						self.gpsqiang = str(qiang2)
				else:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang4:
							pass
						else:
							self.gpsqiang = str(qiang4)
					else:
						self.gpsqiang = str(qiang4)
			else:
				if qiang3 > qiang4:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang3:
							pass
						else:
							self.gpsqiang = str(qiang3)
					else:
						self.gpsqiang = str(qiang3)
				else:
					if len(self.gpsqiang) > 0:
						if int(self.gpsqiang) > qiang1:
							pass
						else:
							self.gpsqiang = str(qiang4)
					else:
						self.gpsqiang = str(qiang4)
		if int(self.gpsqiang) > 60:
			self.gpsqiang = '0'
		gsv[0] = 'GSV'
		gsv[1] = wei1
		gsv[2] = wei1qiang
		gsv[3] = wei2
		gsv[4] = wei2qiang
		gsv[5] = wei3
		gsv[6] = wei3qiang
		gsv[7] = wei4
		gsv[8] = wei4qiang
		gsv[9] = self.gpsqiang
		gsv[10] = self.weishuliang
		gsv[11] = wei1y
		gsv[12] = wei1f
		gsv[13] = wei2y
		gsv[14] = wei2f
		gsv[15] = wei3y
		gsv[16] = wei3f
		gsv[17] = wei4y
		gsv[18] = wei4f
		return gsv

	def getgga(self,buff):
		gga = [0 for x in range(0, 9)]
		utctime = ''
		wei = ''
		weibanqiu = ''
		jing = ''
		jingbanqiu = ''
		dingwei = ''
		jiexiweixing = ''
		if not self.IsNullOrEmpty(buff[1]):
			utctime = buff[1]
		if not self.IsNullOrEmpty(buff[2]):
			wei = buff[2]
		if not self.IsNullOrEmpty(buff[3]):
			weibanqiu = buff[3]
		if not self.IsNullOrEmpty(buff[4]):
			jing = buff[4]
		if not self.IsNullOrEmpty(buff[5]):
			jingbanqiu = buff[5]
		if not self.IsNullOrEmpty(buff[6]):
			dingwei = buff[6]
		if not self.IsNullOrEmpty(buff[7]):
			if self.isnum(buff[7]):
				jiexiweixing =buff[7]
			if len(jiexiweixing) == 2:
				if len(self.jiexiweixingshuliang) > 0:
					if int(self.jiexiweixingshuliang) > int(jiexiweixing):
						pass
					else:
						self.jiexiweixingshuliang = jiexiweixing
				else:
					self.jiexiweixingshuliang = jiexiweixing
		if dingwei=='0':
			pass
		elif dingwei=='1':
			if len(self.jiexiweixingshuliang) > 0 and int(self.jiexiweixingshuliang) >= 3:
				self.isgga = True
		elif dingwei=='2':
			if len(self.jiexiweixingshuliang) > 0 and int(self.jiexiweixingshuliang) >= 3:
				self.isgga=True
		elif dingwei=='6':
			pass
		gga[0] = 'GGA'
		gga[1] = wei
		gga[2] = weibanqiu
		gga[3] = jing
		gga[4] = jingbanqiu
		gga[5] = jiexiweixing
		if self.isgga:
			gga[6] = '1'
		else:
			gga[6] = '0'
		gga[7] = dingwei
		gga[8] = utctime
		return gga
			
	def getrmc(self,buff):
		rmc = [0 for x in range(0, 9)]
		wei = ''
		weibanqiu = ''
		jing = ''
		jingbanqiu = ''
		dingwei = ''
		utcriqi = ''
		utctime = ''
		speed=''
		if not self.IsNullOrEmpty(buff[1]):
			utctime = buff[1]
		if not self.IsNullOrEmpty(buff[2]):
			dingwei=buff[2]
		if not self.IsNullOrEmpty(buff[3]):
			wei = buff[3]
		if not self.IsNullOrEmpty(buff[4]):
			weibanqiu = buff[4]
		if not self.IsNullOrEmpty(buff[5]):
			jing = buff[5]
		if not self.IsNullOrEmpty(buff[6]):
			jingbanqiu = buff[6]
		if not self.IsNullOrEmpty(buff[7]):
			if len(buff[7])>0:
				speed = str(float(buff[7]) * 1.15077945)
			else:
				speed='0'
		if not self.IsNullOrEmpty(buff[9]):
			utcriqi = buff[9]
		if len(dingwei) > 0:
			if dingwei == 'v':
				self.isrmc = False
			elif dingwei == 'A':
				self.isrmc = True
		if len(weibanqiu) > 0:
			if weibanqiu == 'N':
				pass
			elif weibanqiu == 'S':
				pass
		if len(jingbanqiu) > 0:
			if jingbanqiu == 'E':
				pass
			elif jingbanqiu == 'W':
				pass
		rmc[0] = 'RMC'
		rmc[1] = wei
		rmc[2] = weibanqiu
		rmc[3] = jing
		rmc[4] = jingbanqiu
		rmc[5] = utctime
		rmc[6] = utcriqi
		if self.isrmc:
			rmc[7] = '1'
		else:
			rmc[7] = '0'
		rmc[8] = speed
		#print("rmc:",rmc)
		return rmc
		
	def getgll(self,buff):
		gll = [0 for x in range(0, 8)]
		wei = ''
		weibanqiu = ''
		jing = ''
		jingbanqiu = ''
		dingwei = ''
		utctime = ''
		dingweimoshi = ''
		if not self.IsNullOrEmpty(buff[1]):
			wei = buff[1]
		if not self.IsNullOrEmpty(buff[2]):
			weibanqiu = buff[2]
		if not self.IsNullOrEmpty(buff[3]):
			jing = buff[3]
		if not self.IsNullOrEmpty(buff[4]):
			jingbanqiu = buff[4]
		if not self.IsNullOrEmpty(buff[5]):
			utctime = buff[5]
		if not self.IsNullOrEmpty(buff[6]):
			dingwei = buff[6]
		if not self.IsNullOrEmpty(buff[7]):
			dingweimoshi = buff[7]
		if len(dingwei) > 0:
			if dingwei == 'v':
				pass
			elif dingwei == 'A':
				self.isgll = True
		if len(weibanqiu) > 0:
			if weibanqiu == 'N':
				pass
			elif weibanqiu == 'S':
				pass
		if len(jingbanqiu) > 0:
			if jingbanqiu == 'E':
				pass
			elif jingbanqiu == 'W':
				pass
		gll[0] = 'GLL'
		gll[1] = wei
		gll[2] = weibanqiu
		gll[3] = jing
		gll[4] = jingbanqiu
		gll[5] = utctime
		if self.isgll:
			gll[6] = '1'
		else:
			gll[6] = '0'
		gll[7] = dingweimoshi
		return gll
		
	def cleardata(self):
		self.isrmc = False
		self.isgga = False
		self.isgll = False
		self.isgsa = False
		self.weishuliang = ''
		self.jiexiweixingshuliang = ''
		self.gpsqiang = ''
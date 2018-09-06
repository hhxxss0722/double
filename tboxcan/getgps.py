#coding:utf-8
import re
class GetGpsClass(object):
	def __init__(self,readgpsS,readgpsserchstar,readgpsgetstar,ispcba,iszd):
		self.isrmc=False
		self.isgsa=False
		self.isgga=False
		self.isgsv=False
		self.isgll=False
		self.autogps=0
		self.gpsmiao=0
		self.gpstesttime=0
		self.startable={}
		self.starchangetime=0
		self.upgpsStrength=''
		#设置的固定值
		self.readgpsS=readgpsS
		self.readgpsserchstar=readgpsserchstar
		self.readgpsgetstar=readgpsgetstar
		self.ispcba=ispcba
		self.iszd=iszd
		
	def isnum(self,s):
		match=re.findall(r'\d+',s, re.I)
		isok=False
		if match:
			isok=True
		return isok
		
	def SetGpsMiao(self,m):
		self.gpsmiao=m
		
	def ClaerStarTable(self):
		self.startable.clear()
		
	def ClearData(self):
		self.isrmc=False
		self.isgsa=False
		self.isgga=False
		self.isgsv=False
		self.isgll=False
		self.autogps=0
		self.gpsmiao=0
		self.gpstesttime=0
		self.startable.clear()
		self.starchangetime=0
		self.upgpsStrength=''
		
	def GetStarTable(self):
		return self.startable
		
	def ClearStarTable(self):
		self.startable.clear()
		
	def ClearBooL(self):
		self.isrmc=False
		self.isgsa=False
		self.isgga=False
		self.isgsv=False
		self.isgll=False
		
	def GetGps(self,gbuff):
		#print("gbuff1:",gbuff)
		head = gbuff[0]
		data=[]
		"""
		if self.isrmc and self.isgga and self.isgsa  and self.isgsv and self.gpsmiao>=10:
			self.autogps+=1
			if self.autogps >= 3:
				print("定位成功！-------------------")
				data.append("定位")
				data.append(self.upgpsStrength)
				data.append(str(self.gpsmiao))
				data.append('2')
				print(data)
		"""
		if (self.isrmc and self.isgga and self.isgsa and self.isgsv )and self.gpsmiao < 11:
			self.ClearBooL()
		else:
			self.gpstesttime+=1
			#print("gbuff2:",gbuff)
			if head=="GSA": 
				data=self.GetGsa(gbuff)
			elif head== "GSV":
				data=self.GetGsv(gbuff)
			elif head=="GGA":
				data=self.GetGga(gbuff)
			elif head=="RMC":
				data=self.GetRmc(gbuff)
				#print("grmc:",data)
			elif head=="VTG":
				pass
			elif head=="GLL":
				data=self.GetGll(gbuff)
		return data

	def GetGsa(self,gbuff):
		length = len(gbuff)
		for i in range(4,length-4):
			if gbuff[i] is not None and len(str(gbuff[i]))>0:
				if gbuff[i] in self.startable:
					pass
				else:
					self.startable[gbuff[i]]=1
		print("startable:",self.startable)
		print("PDOP:" + str(gbuff[length - 3]) + " HDOP:" + str(gbuff[length - 2]) + " VDOP:" + str(gbuff[length - 1]))
		self.isgsa = self.GetDW(gbuff[3])
		data=[]
		data.append('GSA')
		data.append('0')
		if self.isgsa:
			print("_________ISGSA________")
			data[1]='1'
		data.append(self.startable)
		return data

	def GetGsv(self,gbuff):
		data=[]
		data.append('GSV')
		wei1 = gbuff[1];
		wei1qiang = gbuff[2];
		wei2 = gbuff[3];
		wei2qiang = gbuff[4];
		wei3 = gbuff[5];
		wei3qiang = gbuff[6];
		wei4 = gbuff[7];
		wei4qiang = gbuff[8];
		if len(self.upgpsStrength) > 0:
			if self.isnum(self.upgpsStrength):
				if self.isnum(gbuff[9]):
					if int(self.upgpsStrength) >= int(gbuff[9]):
						self.starchangetime+=1
					else:
						self.upgpsStrength = gbuff[9];
						self.starchangetime+=1
			else:
				self.upgpsStrength = gbuff[9]
		else:
			self.upgpsStrength = gbuff[9]
			self.starchangetime+=1
		"""
		print('###########')
		print(gbuff[10])
		print("sets:",self.readgpsS)
		print("setc",self.readgpsserchstar)
		print("change:",self.starchangetime)
		print("ups:",self.upgpsStrength)
		print("upm:",self.gpsmiao)
		print('###########')
		"""
		if self.starchangetime >= 2 and self.isnum(gbuff[10]) and self.isnum(self.readgpsS) and self.isnum(self.readgpsserchstar) and int(gbuff[10]) >= int(self.readgpsserchstar) and self.isnum(self.upgpsStrength) and int(self.upgpsStrength) >= int(self.readgpsS) and self.gpsmiao >= 10:
			print('@@@@@@@@@@@@@@@1')
			if self.ispcba:
				data.append("11")#初检测试OK
				data.append(self.upgpsStrength)
				data.append(str(self.gpsmiao))
				data.append('1')
				print('@@@@@@@@@@@@2')
			elif self.iszd:
				self.isgsv = True
				data.append("10")#GSV测试OK
				data.append(self.upgpsStrength)
				data.append(str(self.gpsmiao))
				data.append('1')
				print("_________ISGSV________")
		else:
			data.append("00")
			data.append(self.upgpsStrength)
			data.append(str(self.gpsmiao))
			data.append('0')
		print(u"GPS最大强度值：" + self.upgpsStrength)
		wei1q = [wei1, wei1qiang]
		wei2q = [wei2, wei2qiang]
		wei3q = [wei3, wei3qiang]
		wei4q = [wei4, wei4qiang]
		data.append(wei1q)
		data.append(wei2q)
		data.append(wei3q)
		data.append(wei4q)
		return data

	def GetGga(self,gbuff):
		data=[]
		dingwei = gbuff[7]
		gbuff[2] = self.GetBanqiu(gbuff[2])
		gbuff[4] = self.GetBanqiu(gbuff[4])
		gbuff[7] = self.GetDingwei(gbuff[7])
		self.isgga = self.GetDW(gbuff[6])
		data.append('GGA')
		data.append('0')
		if self.isgga and self.isnum(self.readgpsgetstar) and self.isnum(gbuff[5]) and int(gbuff[5]) > int(self.readgpsgetstar):
			print("_________ISGGA________")
			data[1]='1'
		return data

	def GetBanqiu(self,s):
		data = ''
		if s=="N":
			data = u"北半球"
		elif s=="S":
			data = u"南半球"
		elif s=="E":
			data = u"东经"
		elif s=="W":
			data = u"西经"
		return data

	def GetDingwei(self,s):
		data = ''
		if s=="0":
			data = u"未定位"
		elif s=="1":
			data = u"非差分定位"
		elif s=="2":
			data = u"差分定位"
		elif s=="6":
			data = u"正在估算"
		elif s=="A":
			data = u"自动"
		elif s=="D":
			data = u"差分"
		elif s=="N":
			data = u"数据无效"
		elif s=="S":
			data = u"模拟"
		elif s=="M":
			data = u"手动"
		return data

	def GetDW(self,s):
		isok = False
		if s == "1":
			isok = True
		return isok
		
	def GetRmc(self,gbuff):
		data=[]
		data.append('RMC')
		gbuff[2] = self.GetBanqiu(gbuff[2])
		gbuff[4] = self.GetBanqiu(gbuff[4])
		data.append(gbuff[2])
		data.append(gbuff[4])
		data.append('0')
		self.isrmc = self.GetDW(gbuff[7])
		if self.isrmc:
			print("_________ISRMC________")
			data[3]='1'
		return data

	def GetGll(self,gbuff):
		data=[]
		data.append('GLL')
		gbuff[2] = self.GetBanqiu(gbuff[2])
		gbuff[4] = self.GetBanqiu(gbuff[4])
		gbuff[7] = self.GetDingwei(gbuff[7])
		data.append(gbuff[2])
		data.append(gbuff[4])
		data.append(gbuff[7])
		data.append('0')
		self.isgll = self.GetDW(gbuff[6])
		if self.isgll:
			print("_________ISGLL________")
			data[4]='1'
		return data
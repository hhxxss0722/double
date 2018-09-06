#coding:utf-8
import hashlib
class getmd5():

	def init(self):
		self.hexcode=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "1", "2", "3", "4", "5"]
		self.imeikey="carsmart20122012carsmart"
		
	def byteToHexString(self,b):
		scode=""
		n=int(b,16)
		if	n < 0:
			n = 256 + n
		if n<16 and n>=10:
			n=n-10
			scode=self.hexcode[n]
			#print("#",scode)
		else:
			scode=self.hexcode[n]
			#print("@",scode)
		return scode
		
	def byteArrayToHexString(self,blist):
		strcode=""
		blen=len(blist)
		for i in range(0,blen):
			strcode = strcode+self.byteToHexString(blist[i])
		return strcode
		
	def GetYZM(self,text):
		imeicode = self.md5One(text)
		print(imeicode)
		code = ""
		length = len(imeicode)
		if length > 4:
			code += imeicode[0]
			code += imeicode[3]
			code += imeicode[length - 3]
			code += imeicode[length - 1]
		elif length == 4:
			code = imeicode
		return code
	
	def md5One(self,s):
		m = hashlib.md5()
		m.update((s+self.imeikey).encode('UTF-8'))
		ss=m.hexdigest()
		print(ss)
		code = self.byteArrayToHexString(ss)
		return code
"""		
g=getmd5()
g.init()
imei="869267012272899"
code=g.GetYZM(imei)
print(code)
"""
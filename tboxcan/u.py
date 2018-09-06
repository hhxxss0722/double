#coding:utf-8
import psutil,struct
import hashlib
import os
import stat

def GetUdisk():
	disk=psutil.disk_partitions()
	dlen=len(disk)
	udisk=disk[dlen-1]
	name=udisk[0]
	option=udisk[3]
	if option=='rw,removable':
		pass
	else:
		for e in disk:
			if e[3]=='rw,removable':
				name=e[0]
				break
	return name
	
def md5sum(data):                      
	fmd5 = hashlib.md5(data) 
	return fmd5.hexdigest()  
	
def savebin(path,data):
	if data is not None:
		with open(path,'wb') as f:
			f.write(data)
			f.close()
			
def readbin(path,md5):
	data=None
	with open(path,"rb") as f:
		line=f.readline()  
		while line:
			if data is None:
				data = line
			else:
				data+=line
			line=f.readline()
	rmd5=md5sum(data).upper()
	print(rmd5)
	if rmd5==md5:
		print("OK!")
		return data
	else:
		return "ERR:1"
	
def backup(path,md5,spath):
	data=readbin(path,md5)
	if data=="ERR:1":
		return "Read MD5 Fail"
	else:
		savebin(spath,data)
		data=readbin(spath,md5)
		if data=="ERR:1":
			return "Write MD5 Fail"
		else:
			print("Backup ok!")
			return "<backup ok>"
		
def BackUpBin(path,spath,name,md5):
	mdir=GetUdisk()+spath
	if os.path.exists(mdir):
		pass
	else:
		os.makedirs(mdir)
		os.chmod(mdir, stat.S_IREAD | stat.S_IWRITE)
	spath=GetUdisk()+spath+name
	sdata=backup(path,md5,spath)
	return sdata
	
#BackUpBin()
#readbin("fupgrade.bin","B5335C03583C05F305D34F9830EAE4C1")
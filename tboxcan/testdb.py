#coding:utf-8
"""
from database import *
import time
path="sqlite:///pcbadb//test.db"	
db=InitDb(path)
itime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
imeicode=Imei(imei='8612345689',url='1236666',date=itime)
AddImei(imeicode,db)
QueryImei('8612345689',db)
CloseDb(db)
"""
def zero(code):
	return "zero:"+str(code)
 
def one(code):
	return "one:"+str(code)
 
def numbers_to_functions_to_strings(argument,code):
	switcher = {
		0: zero,
		1: one,
	}
	# Get the function from switcher dictionary
	func = switcher.get(argument, lambda: "nothing")
	# Execute the function
	return func(code)
	
s=numbers_to_functions_to_strings(0,256)
print(s)
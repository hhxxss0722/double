#coding:utf-8
import win32com
from win32com.client import Dispatch
from pymd5.pymd5 import getmd5
class pyprint():
    def __init__(self,path,batch):
        self.path=path
        self.batch=batch
        self.gmd5=getmd5()
        self.gmd5.init()
        self.btApp=win32com.client.Dispatch('BarTender.Application')

    def pirint(self,imei,co):
        btFormat = self.btApp.Formats.Open(self.path, False, '')
        btFormat.PrintSetup.IdenticalCopiesOfLabel = 1
        btFormat.SetNamedSubStringValue('IMEI', imei)
        btFormat.SetNamedSubStringValue('CO', co)
        btFormat.SetNamedSubStringValue('SN', self.batch)
        btFormat.PrintOut(False, False)

    def printimei(self,imei):
        co=self.gmd5.GetYZM(imei)
        self.pirint(imei,co)

    def printsn(self,sn):
        btFormat = self.btApp.Formats.Open(self.path, False, '')
        btFormat.PrintSetup.IdenticalCopiesOfLabel = 1
        btFormat.SetNamedSubStringValue('SN',sn)
        btFormat.PrintOut(False, False)

    def printtbox2(self,slist):
        imei=slist['imei']
        co=self.gmd5.GetYZM(imei)
        btFormat = self.btApp.Formats.Open(self.path, False, '')
        btFormat.PrintSetup.IdenticalCopiesOfLabel = 1
        btFormat.SetNamedSubStringValue('sn',slist['sn'])
        btFormat.SetNamedSubStringValue('sn2',slist['sn'])
        btFormat.SetNamedSubStringValue('bn',self.batch)
        btFormat.SetNamedSubStringValue('code',co)
        btFormat.SetNamedSubStringValue('hw',slist['hw'])
        btFormat.SetNamedSubStringValue('imei',imei)
        btFormat.PrintOut(False, False)

    def closeprint(self):
        self.btApp.Quit(1)
"""
path="D:\\tboxcan\\pyprint\\IMEI2.btw"
bath="180301XJ"
p=pyprint(path,bath)
imei="869267012206657"
p.printimei(imei)
p.closeprint()
"""
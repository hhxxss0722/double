#coding:utf-8
import win32com
from win32com.client import Dispatch
w = win32com.client.Dispatch('BarTender.Application')
btApp=w
btFormat = btApp.Formats.Open(r'D:\tboxcan\pyprint\IMEI2.btw', False, '')
btFormat.PrintSetup.IdenticalCopiesOfLabel = 1
btFormat.SetNamedSubStringValue('IMEI', '86123456789012354')
btFormat.SetNamedSubStringValue('CO', '0124')
btFormat.SetNamedSubStringValue('SN', '170401XJ')
btFormat.PrintOut(False, False)
btApp.Quit(1)
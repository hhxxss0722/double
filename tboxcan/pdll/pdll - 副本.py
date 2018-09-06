#coding:utf-8
from ctypes import *
import time
lib = windll.LoadLibrary("ControlCAN.dll")
class CanCfg(Structure):  
    _fields_ = [("AccCode", c_ulong),
                ("Reserved ", c_ulong),
                ("AccMask", c_ulong),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)]
class Canobj(Structure):
    _fields_ =[
                ("ID",c_uint),
                ("TimeStamp",c_uint),
                ("TimeFlag",c_byte),
                ("SendType",c_byte),
                ("RemoteFlag",c_byte),
                ("ExternFlag",c_byte),
                ("DataLen",c_byte),
                ("Data",c_byte*8),
                ("Reserved",c_byte*3)]
class Errobj(Structure):
    _fields_ =[
                ("ErrCode",c_ulong),
                ("Passive_ErrData",c_byte*3),
                ("ArLost_ErrData",c_byte)]
opendev=lib.VCI_OpenDevice
initcan=lib.VCI_InitCAN
startcan=lib.VCI_StartCAN
senddata=lib.VCI_Transmit
closedev=lib.VCI_CloseDevice
receivenum=lib.VCI_GetReceiveNum
receivedata=lib.VCI_Receive
readerrinfo=lib.VCI_ReadErrInfo
cancfg=CanCfg()
cobj=Canobj()
errobj=Errobj()
devtype=4
devindex=0
canindex=0
cancfg.AccCode=0x00000000
cancfg.AccMask=0xFFFFFFFF
cancfg.Filter=0x01
cancfg.Timing0=0x00
cancfg.Timing1=0x1C
cancfg.Mode=0
dev=opendev(4,0,0)
print('devopen:',dev)
devinit=initcan(devtype,devindex,canindex,byref(cancfg))
print('caninit:',devinit)
scan=startcan(devtype,devindex,canindex)
print('startcan:',scan)
def SendCanData(cobj):
    cobj.RemoteFlag = 0x00
    cobj.ExternFlag = 0x00
    cobj.ID = 3
    cobj.DataLen =0x08
    cobj.Data[0]=0x17
    cobj.Data[1]=0x00
    cobj.Data[2]=0x00
    cobj.Data[3]=0x00
    cobj.Data[4]=0x00
    cobj.Data[5]=0x00
    cobj.Data[6]=0x00
    cobj.Data[7]=0x00
    return cobj
cobj=SendCanData(cobj)
sendok=senddata(devtype, devindex, canindex,byref(cobj),1)
print('senddata:',sendok)
import threading
import timer
def ToHex(dlist):
    dstr=""
    for e in dlist:
        dstr+=str(e)+" "
    return dstr
def fun_timer():
    rnum=receivenum(4,0,0)
    #print('receivenum:',rnum)
    if rnum==0:
        pass
    else:
        robj=Canobj()
        lRel = receivedata(devtype,devindex,canindex,byref(robj),1,50)
        if lRel==0:
            pass
        else:
            print('receivedata:',lRel)
            print('收到数据：',ToHex(robj.Data))
    global timer
    timer = threading.Timer(0.1,fun_timer)
    timer.start()
        #cok=closedev(devtype,devindex)
        #print('closedev:',cok)

timer = threading.Timer(1,fun_timer)  #首次启动
timer.start()

"""
while True:
    time.sleep(0.1)
    rnum=receivenum(devtype,devindex,canindex)
    print('receivenum:',rnum)
    robj=Canobj()
    if rnum==0:
        bRel = readerrinfo(devtype, devindex, canindex, byref(errobj))
        if bRel==1:
            print(errobj.ErrCode)
    else:
        lRel = receivedata(devtype,devindex, canindex,byref(robj),1,50)
        print('receivedata:',lRel)
        cok=closedev(devtype,devindex)
        print('closedev:',cok)
        break
"""
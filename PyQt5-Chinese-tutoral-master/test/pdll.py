#coding:utf-8
from ctypes import *
class CanCfg(Structure):  
    _fields_ = [("AccCode", c_ulong),
                ("AccMask", c_ulong),
                ("Reserved ", c_ulong),
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
#ControlCAN.dll
class CanDev(object):
    def __init__(self,dllpath):
        self.dllpath=dllpath
        self.lib=windll.LoadLibrary(self.dllpath)
        self.GetFunction()
        self.InitData()

    def GetFunction(self):
        self.opendev=self.lib.VCI_OpenDevice
        self.initcan=self.lib.VCI_InitCAN
        self.startcan=self.lib.VCI_StartCAN
        self.senddata=self.lib.VCI_Transmit
        self.closedev=self.lib.VCI_CloseDevice
        self.receivenum=self.lib.VCI_GetReceiveNum
        self.receivedata=self.lib.VCI_Receive
        self.readerrinfo=self.lib.VCI_ReadErrInfo
        self.resetcan=self.lib.VCI_ResetCAN
        self.GetSet=self.lib.VCI_GetReference2
        #self.GetSet.argtypes = [c_int, c_int, c_int, c_int, Array]

    def InitData(self):
        self.cancfg=CanCfg()
        self.InitDefaultCanData()
        self.cobj=Canobj()
        self.errobj=Errobj()
        self.devtype=4
        self.devindex=0
        self.canindex=0
        self.devopen=False

    def SetDev(self,list):
        self.devtype=list[0]
        self.devindex=list[1]
        self.canindex=list[2]
    #CAN通讯速率500Kbps
    def InitDefaultCanData(self):
        self.cancfg.AccCode=1<<21
        self.cancfg.AccMask=3<<21
        self.cancfg.Filter=1
        self.cancfg.Timing0=0
        self.cancfg.Timing1=28
        self.cancfg.Mode=0

    def OpenDevDefault(self):
        self.devopen=False
        openmsg={}
        dev=self.opendev(self.devtype,self.devindex,0)
        if dev==1:
            openmsg['state']=1
            openmsg['msg']="opendev ok"
            self.devopen=True
        else:
            openmsg['state']=-1
            openmsg['msg']="opendev fail"
        return openmsg

    def isDevOpen(self):
        return self.devopen

    def InitCanDefault(self):
        self.cancfg=CanCfg()
        self.InitDefaultCanData()
        devinit=self.initcan(self.devtype,self.devindex,self.canindex,byref(self.cancfg))
        initmsg={}
        if devinit==1:
            initmsg['state']=1
            initmsg['msg']="init can ok"
        else:
            initmsg['state']=-1
            initmsg['msg']="init can fail"
        info= ( c_byte * 27) ()
        gmsg=self.GetSet(self.devtype,self.devindex,self.canindex,0,info)
        print(self.ToHexStr(info))
        return initmsg

    def StartCan(self):
        scan=self.startcan(self.devtype,self.devindex,self.canindex)
        scmsg={}
        if scan==1:
            scmsg['state']=1
            scmsg['msg']='start can ok'
        else:
            scmsg['state']=-1
            scmsg['msg']='start can fail'
        return scmsg

    def InitCobjDefault(self):
        self.cobj.RemoteFlag = 0x00
        self.cobj.ExternFlag = 0x00
        self.cobj.ID = 3
        self.cobj.DataLen =0x08
        self.cobj.Data[0]=0x17
        self.cobj.Data[1]=0x00
        self.cobj.Data[2]=0x00
        self.cobj.Data[3]=0x00
        self.cobj.Data[4]=0x00
        self.cobj.Data[5]=0x00
        self.cobj.Data[6]=0x00
        self.cobj.Data[7]=0x00

    def FillCanObj(self,blist):
        self.cobj.RemoteFlag = 0x00
        self.cobj.ExternFlag = 0x00
        self.cobj.ID = 3
        self.cobj.DataLen =0x08
        for i in range(0,8):
            self.cobj.Data[i]=blist[i]

    def ToHexStr(self,dlist):
        data=""
        for e in dlist:
            data+=hex(e)+" "
        return data

    def SendData(self,blist):
        self.FillCanObj(blist)
        self.sendok=self.senddata(self.devtype, self.devindex, self.canindex,byref(self.cobj),1)
        smsg={}
        if self.sendok==1:
            smsg['state']=1
            smsg['msg']='发送数据：'+self.ToHexStr(blist)
        else:
            smsg['state']=-1
            smsg['msg']='发送失败！'
        return smsg

    def SendCanDataDefault(self):
        self.InitCobjDefault()
        self.sendok=self.senddata(self.devtype, self.devindex, self.canindex,byref(self.cobj),1)
        smsg={}
        if self.sendok==1:
            smsg['state']=1
            smsg['msg']='send test ok'
        else:
            smsg['state']=-1
            smsg['msg']='send test fail'
        return smsg
    
    def ReceiveNum(self):
        rnum=self.receivenum(4,0,0)
        return rnum

    def ListToString(self,slist):
        lstr=""
        for e in slist:
            lstr+=str(e)+" "
        return lstr

    def ReceiveData(self):
        robj=Canobj()
        robj= ( Canobj * 20) ()
        lRel = self.receivedata(self.devtype,self.devindex,self.canindex,byref(robj),20,50)
        rmsg={}
        rmsg['slen']=lRel
        rmsg['obj']=robj
        return rmsg

    def ResetCan(self):
        info={}
        rstate=self.resetcan(self.devtype,self.devindex,self.canindex)
        info['state']=rstate
        info['msg']='Resetcan'
        return info

    def CloseDev(self):
        cstate=self.closedev(self.devtype,self.devindex)
        cmsg={}
        cmsg['state']=cstate
        cmsg['msg']="Close Dev"
        return cmsg
import threading
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
# 继承QThread  用于调用dll接收数据
class RunCanthread(QtCore.QThread):   
    _signal = pyqtSignal(list)  
  
    def __init__(self, parent=None):  
        super(RunCanthread, self).__init__()

    def init(self,cdev,a):
        self.cdev=cdev
        self.alive=a
  
    def __del__(self):  
        self.wait()  

    def ToHex(self,dlist):
        dstr=""
        for e in dlist:
            dstr+=str(c_ubyte(e))+" "
        return dstr

    def ToBytes(self,dlist):
        data=b''
        for e in dlist:
            data+=c_ubyte(e)
        #print('objdata:',data)
        return data
  
    def run(self):  
        while self.alive.isSet():
            try:
                rnum=self.cdev.ReceiveNum()
                if rnum==0:
                    pass
                else:
                    print('rnum:',rnum)
                    for i in range(0,rnum):
                        rdata = self.cdev.ReceiveData()
                        if rdata['slen']==0:
                            pass
                        else:
                            robj=rdata['obj']
                            slen=rdata['slen']
                            print('receivedata:',slen)
                            for i in range(0,slen):
                                #print('收到数据@@##：',self.ToHex(robj.Data))
                                dlist=[]
                                dlist.append(robj[i].ID)
                                dlist.append(self.ToBytes(robj[i].Data))
                                self._signal.emit(dlist)
                                #print("数据OK！")
            except Exception as e:
                print("线程异常：",str(e))
                elist=[]
                elist.append(-1)
                elist.append(str(e).encode('utf-8'))
                self._signal.emit(elist)
                break
  
    def callback(self, msg):  
        self._signal.emit(0,msg)

class TestPydll():
    def callback(self,msg):
        print("调用：：：：：：")
        print("收到调用数据：",msg)

    def StartWThread(self,cdev,t,a):
        self.t=t
        self.a=a
        self.cdev=cdev
        # 创建线程  
        self.t = RunCanthread()  
        # 连接信号
        self.a.set()
        self.t.init(self.cdev,self.a)		
        self.t._signal.connect(self.callback)		
        # 开始线程  
        self.t.start()  	

    #停止线程
    def StopWThread(self,t,a,cdev):
        self.t=t
        self.a=a
        self.cdev=cdev
        if t is not None:
            self.a.clear() 			# clear alive event for thread
            self.t.quit()
            self.t.wait()
            self.t.exit()
            self.t = None
"""
def main():
    dllpath="ControlCAN.dll"
    cdev=CanDev(dllpath)
    omsg=cdev.OpenDevDefault()
    if omsg['state']==1:
        imsg=cdev.InitCanDefault()
        if imsg['state']==1:
            smsg=cdev.StartCan()
            if smsg['state']==1:
                sendmsg=cdev.SendCanDataDefault()
                if sendmsg['state']==1:
                    print('数据发送成功')
                    t=None
                    a = threading.Event()
                    tpll=TestPydll()
                    tpll.StartWThread(cdev,t,a)
main()
"""
#coding:utf-8
class SendCanData():
    def __init__(self):
        self.gpsbyte=b''
    #65 84 0 96 0 0 8
    def GetHead(self):
        head=b''
        head+=bytes([65])
        head+=bytes([84])
        head+=bytes([0])
        head+=bytes([96])
        head+=bytes([0])
        head+=bytes([0])
        head+=bytes([8])
        return head

    def GetEnd(self):
        end=b''
        end+=bytes([13])
        end+=bytes([10])
        return end

    def makelist(self,bn):
        bytelist=b''
        bytelist+=bytes([bn])
        for i in range(0,7):
            bytelist+=bytes([0])
        return bytelist

    def SetGpsByte(self,gbytes):
        self.gpsbyte=gbytes

    #01 00 00 00 00 00 00 00
    def enterqc(self,code):
        bytelist=self.makelist(1)
        return bytelist
    #02
    def outqc(self,code):
        bytelist=self.makelist(2)
        return bytelist
    #03
    def Getsoft(self,code):
        bytelist=self.makelist(3)
        return bytelist
    #04
    def GetDtu(self,code):
        bytelist=self.makelist(4)
        return bytelist
    #05
    def GetWifiState(self,code):
        bytelist=self.makelist(5)
        return bytelist
    #06
    def GetWifiOpen(self,code):
        bytelist=self.makecanlist(code['f'],6)
        return bytelist

    def GetCallD(self,code):
        bl=[]
        bytelist=code['port'].encode("utf-8")
        blen=len(bytelist)
        if blen<=12:
            for i in range(blen,12):
                bytelist+=bytes([0])
        else:
            bytelist=bytelist[0:12]
        sendlist=b''
        sendlist+=bytes([7])
        sendlist+=bytes([1])
        for i in range(0,6):
            sendlist+=bytes([bytelist[i]])
        bl.append(sendlist)
        sendlist=b''
        sendlist+=bytes([7])
        sendlist+=bytes([2])
        for i in range(6,12):
            sendlist+=bytes([bytelist[i]])
        bl.append(sendlist)
        return bl

    def GetCallA(self,code):
        bytelist=self.makelist(8)
        return bytelist

    def GetCallH(self,code):
        bytelist=self.makelist(9)
        return bytelist

    def GetAdc(self,code):
        bytelist=self.makelist(16)
        return bytelist

    def GetE2r(self,code):
        bytelist=self.makelist(17)
        return bytelist

    def GetEmmc(self,code):
        bytelist=self.makelist(18)
        return bytelist

    def makecanlist(self,code,dn):
        bytelist=b''
        bytelist+=bytes([dn])
        bytelist+=bytes([0])
        bytelist+=bytes([code])
        for i in range(0,5):
            bytelist+=bytes([0])
        return bytelist

    def GetCan(self,code):
        bytelist=self.makecanlist(code['port'],19)
        return bytelist

    def GetBattery(self,code):
        bytelist=self.makelist(20)
        return bytelist

    def GetUsbOpen(self,code):
        bytelist=self.makecanlist(1,21)
        return bytelist

    def GetUsbClose(self,code):
        bytelist=self.makecanlist(0,21)
        return bytelist

    def GpsColdStart(self,code):
        bytelist=self.makecanlist(1,22)
        return bytelist

    #agps close
    def GetGpsOpen(self,code):
        bytelist=b''
        bytelist+=bytes([22])
        bytelist+=bytes([0])
        bytelist+=bytes([3])
        bytelist+=bytes([1])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    #agps open
    def GetGpsOpen2(self,code):
        bytelist=b''
        bytelist+=bytes([22])
        bytelist+=bytes([0])
        bytelist+=bytes([3])
        bytelist+=bytes([1])
        bytelist+=bytes([1])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetSendGps(self,code):
        bytelist=b''
        bytelist+=bytes([22])
        bytelist+=bytes([0])
        bytelist+=bytes([4])
        bytelist+=self.gpsbyte[0]
        bytelist+=self.gpsbyte[1]
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetSendGpsLogOn(self,code):
        bytelist=b''
        bytelist+=bytes([22])
        bytelist+=bytes([0])
        bytelist+=bytes([3])
        bytelist+=bytes([1])
        bytelist+=bytes([1])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetSendGpsLogOff(self,code):
        bytelist=b''
        bytelist+=bytes([22])
        bytelist+=bytes([0])
        bytelist+=bytes([3])
        bytelist+=bytes([2])
        bytelist+=bytes([2])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetGpsClose(self,code):
        bytelist=self.makecanlist(2,22)
        return bytelist

    def GetGpio(self,code):
        bytelist=self.makelist(23)
        return bytelist

    def GetJz(self,code):
        bytelist=self.makelist(24)
        return bytelist

    def GetL99m(self,code):
        p=code['port']
        f=code['f']
        bytelist=b''
        bytelist+=bytes([25])
        bytelist+=bytes([0])
        bytelist+=bytes([p])
        bytelist+=bytes([f])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetPowerOpen(self,code):
        bytelist=b''
        bytelist+=bytes([0x20])
        bytelist+=bytes([0])
        bytelist+=bytes([code['port']])
        bytelist+=bytes([code['f']])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetPowerClose(self,code):
        bytelist=self.makecanlist(code['port'],32)
        return bytelist

    def GetReadUpgrade(self,code):
        p=code['port']
        bytelist=b''
        if p ==1:
            bytelist=self.makecanlist(1,33)
        elif p==2:
            bytelist+=bytes([0x21])
            bytelist+=bytes([0])
            bytelist+=bytes([2])
            bytelist+=bytes([code['f']])
            bytelist+=bytes([0])
            bytelist+=bytes([0])
            bytelist+=bytes([0])
            bytelist+=bytes([0])
        return bytelist

    def GetLogin(self,code):
        bytelist=self.makelist(34)
        return bytelist

    def Getlpm(self,code):
        bytelist=self.makelist(35)
        return bytelist

    def GetSim(self,code):
        p=code['port']
        bytelist=b''
        if p ==0:
            bytelist=self.makecanlist(0,36)
        elif p==1:
            bytelist+=bytes([36])
            bytelist+=bytes([0])
            bytelist+=bytes([1])
            bytelist+=code['f']
            bytelist+=bytes([0])
            bytelist+=bytes([0])
            bytelist+=bytes([0])
            bytelist+=bytes([0])
        return bytelist

    def GetLog(self,code):
        bytelist=self.makecanlist(code['f'],37)
        return bytelist

    def Upload(self,code):
        bytelist=self.makelist(38)
        return bytelist

    def GetEmc(self,code):
        p=code['port']
        bytelist=b''
        bytelist+=bytes([39])
        bytelist+=bytes([0])
        bytelist+=p
        bytelist+=code['f']
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetLed(self,code):
        p=code['port']
        bytelist=b''
        bytelist+=bytes([0x28])
        bytelist+=bytes([0])
        bytelist+=p
        bytelist+=code['f']
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        bytelist+=bytes([0])
        return bytelist

    def GetCanData(self,argument,data):
        switcher ={
            0:self.enterqc,
            1:self.outqc,
            2:self.Getsoft,
            4:self.GetDtu,
            5:self.GetWifiState,
            6:self.GetWifiOpen,
            7:self.GetCallD,
            8:self.GetCallA,
            9:self.GetCallH,
            10:self.GetAdc,
            11:self.GetE2r,
            12:self.GetEmmc,
            13:self.GetCan,
            14:self.GetBattery,
            15:self.GetUsbOpen,
            16:self.GetUsbClose,
            17:self.GpsColdStart,
            18:self.GetGpsOpen,
            19:self.GetGpsOpen2,
            20:self.GetSendGps,
            21:self.GetGpsClose,
            22:self.GetGpio,
            23:self.GetJz,
            24:self.GetL99m,
            25:self.GetPowerOpen,
            26:self.GetPowerClose,
            27:self.GetReadUpgrade,
            28:self.GetLogin,
            29:self.Getlpm,
            30:self.GetSim,
            31:self.GetLog,
            32:self.Upload,
            33:self.GetEmc,
            34:self.GetLed,
            35:self.GetSendGpsLogOn,
            36:self.GetSendGpsLogOff,
        }
        func = switcher.get(argument,lambda:"nothing")
        return func(data)
#coding:utf-8
import struct,re
class GetCanOrder():
    def __init__(self):
        self.boot=""
        self.app=""
        self.qc=""
        self.dtusoft=""
        self.imei=""
        self.imsi=""
        self.c1=""
        self.c2=""
        self.c3=""
        self.wifistate=""
        self.ssid=""
        self.pwd=""
        self.wopen=""
        self.callds=""
        self.callas=""
        self.callhs=""
        self.adc1=""
        self.adc2=""
        self.adc3=""
        self.e2r={}
        self.emmcid=""
        self.emmcstate={}
        self.can={}
        self.gpsset={}
        self.port=""
        self.m=""
        self.rtc=""
        self.l99m={}
        self.power={}
        self.insertsoft=""
        self.upgradestate={}
        self.loginstate=""
        self.lpmstate=""
        self.simstate=""
        self.logstate=""
        self.upload=""
        self.uploadurl=""
        self.emc={}

    def Getdatabuff(self,data):
        buff=b''
        dlen=len(data)
        for i in range(0,dlen-2):
            buff+=bytes([data[i+2]])
        return buff

    def Getdatabuff2(self,data):
        buff=b''
        dlen=len(data)
        for i in range(0,dlen-3):
            buff+=bytes([data[i+3]])
        return buff

    def enterqc(self,data):
        return {'port':'enterqc','v':'1'}

    def outqc(self,data):
        return {'port':'outqc','v':'1'}

    def dtuready(self,data):
        return {'port':'dtuok','v':'1'}

    def GetAscii(self,s):
        pattern = re.compile(r'[a-zA-Z0-9]+')
        slist=re.findall(pattern, s)
        slen=len(slist)
        pdata=""
        if slen==1:
            pdata=slist[0]
        else:
            for e in slist:
                pdata+=e
        return pdata

    def getboot(self,data):
        sid=data[1]
        if sid==0x01:
            self.boot=""
        bytelist=self.Getdatabuff(data)
        self.boot+=bytelist.decode('ascii', 'replace')
        #print('boot',self.boot)
        return {'port':'boot','v':self.boot}

    def getapp(self,data):
        self.app =self.Getdatabuff(data).decode('ascii', 'replace')
        #print('app:',self.app)
        return {'port':'app','v':self.app}

    def getqc(self,data):
        sid=data[1]
        if sid==0x01:
            self.qc=""
        self.qc+=self.Getdatabuff(data).decode('ascii', 'replace')
        #print('qc:',self.qc)
        return {'port':'qc','v':self.qc}

    def getdtusoft(self,data):
        sid=data[1]
        if sid==0x01:
            self.dtusoft=""
        self.dtusoft+=self.Getdatabuff(data).decode("utf-8")
        return {'port':'dtusoft','v':self.dtusoft}

    def getimei(self,data):
        sid=data[1]
        if sid==0x01:
            self.imei=""
        self.imei+=self.Getdatabuff(data).decode("utf-8")
        return {'port':'imei','v':self.imei}

    def getimsi(self,data):
        sid=data[1]
        if sid==0x01:
            self.imsi=""
        self.imsi+=self.Getdatabuff(data).decode("utf-8")
        return {'port':'imsi','v':self.imsi}

    def getcsq(self,data):
        self.c1=str(data[2])
        self.c2=str(data[3])
        self.c3=str(data[4])
        return {'port':'csq','v1':self.c1,'v2':self.c2,'v3':self.c3}

    def getwifistate(self,data):
        if data[2]==0x01:
            self.wifistate="1"
        elif data[2]==0x00:
            self.wifistate="0"
        return {'port':'wifistate','v':self.wifistate}

    def getwifissid(self,data):
        self.ssid=self.Getdatabuff(data).decode("utf-8")
        return {'port':'ssid','v':self.ssid}

    def getwifipwd(self,data):
        if data[1]==0x01:
            self.pwd=""
        self.pwd+=self.Getdatabuff(data).decode("utf-8")
        return {'port':'pwd','v':self.pwd}

    def getopenwifi(self,data):
        if data[2]==0x00:
            if data[3]==0x01:
                self.wopen="0,1"
            else:
                self.wopen="0,0"
        elif data[2]==0x01:
            if data[3]==0x01:
                self.wopen="1,1"
            else:
                self.wopen="1,0"

    def calld(self,data):
        if data[2]==0x01:
            self.callds="1"
        else:
            self.callds="0"
        return {'port':'calld','v':self.callds}

    def calla(self,data):
        if data[2]==0x01:
            self.callas="1"
        else:
            self.callas="0"
        return {'port':'calla','v':self.callas}

    def callh(self,data):
        if data[2]==0x01:
            self.callhs="1"
        else:
            self.callhs="0"
        return {'port':'callh','v':self.callh}

    def getadc(self,data):
        sid=data[2]
        if sid==0x01:
            self.adc1=int.from_bytes(data[3:7], byteorder = 'big')
            print('@',self.adc1)
            return {'port':'adc1','v':self.adc1}
        elif sid==0x02:
            self.adc2=int.from_bytes(data[3:7], byteorder = 'big')
            print('@',self.adc2)
            return {'port':'adc2','v':self.adc2}
        elif sid==0x03:
            self.adc3=int.from_bytes(data[3:7], byteorder = 'big')
            print('@',self.adc3)
            return {'port':'adc3','v':self.adc3}

    def gete2r(self,data):
        sid=data[2]
        if sid == 0x01:
            if data[3]==0x01:
                self.e2r['read']="1"
            else:
                self.e2r['read']="0"
        elif sid==0x02:
            if data[3]==0x01:
                self.e2r['write']="1"
            else:
                self.e2r['write']="0"
        elif sid==0x03:
            self.e2r['id']=hex(data[3])[2:]
        elif sid==0x04:
            self.e2r['size']=str(int(data[3]))
        print(self.e2r)
        return {'port':'eeprom','v':self.e2r}

    def HexToString(self,oid):
        data=""
        for e in oid:
            data+=hex(e)[2:]
        return data

    def getemmc(self,data):
        sid=data[1]
        fid=data[2]
        if sid==0x01 and fid == 0x01:
            self.emmcid=""
            #self.emmcid+=self.HexToString(self.Getdatabuff2(data))
            self.emmcid+=self.Getdatabuff2(data).decode("utf-8","replace")
        elif fid==0x01:
            self.emmcid+=self.Getdatabuff2(data).decode("utf-8","replace")
            #self.emmcid+=self.HexToString(self.Getdatabuff2(data))
        elif fid==0x02:
            if data[3]==0x01:
                self.emmcstate['read']="1"
            else:
                self.emmcstate['read']="0"
        elif fid == 0x03:
            if data[3]==0x01:
                self.emmcstate["write"]="1"
            else:
                self.emmcstate["write"]="0"
        elif fid==0x04:
            if data[3]==0x01:
                self.emmcstate["erase"]="1"
            else:
                self.emmcstate["erase"]="0"
        return {"port":"emmc",'eid':self.emmcid,'v':self.emmcstate}

    def getcan(self,data):
        sid=data[2]
        fid=data[3]
        if sid==0x01:
            if fid==0x01:
                self.can["0"]="1"
            else:
                self.can["0"]="0"
        elif sid == 0x02:
            if fid==0x01:
                self.can["1"]="1"
            else:
                self.can["1"]="0"
        elif sid== 0x03:
            if fid==0x01:
                self.can["2"]="1"
            else:
                self.can["2"]="0"
        print(self.can)
        return {'port':'can','v':self.can}

    def getbattery(self,data):
        sid=data[2]
        bdata=str(bin(sid))
        return {'port':'battery','v':bdata}

    def getgps(self,data):
        if data[2]==0x01:
            if data[3]==0x01:
                self.gpsset["冷启动"]="1"
            else:
                self.gpsset["冷启动"]="1"
        elif data[2]==0x02:
            if data[3]==0x01:
                self.gpsset["关闭"]="1"
            else:
                self.gpsset["关闭"]="0"
        elif data[2]==0x03:
            if data[3]==0x01:
                self.gpsset["控制"]="1"
            else:
                self.gpsset["控制"]="1"
        elif data[3]==0x04:
            if data[3]==0x01:
                self.gpsset["状态"]="1"
            else:
                self.gpsset["状态"]="0"
        return {'port':'gpsset','v':self.gpsset}

    def getgpio(self,data):
        sid=data[2]
        bdata=str(bin(sid))
        self.port=bdata
        print(bdata)
        return {'port':'gpio','v':self.port}

    def getjz(self,data):
        if data[2]==0x01:
            self.m="1"
        else:
            self.m="0"
        if data[3]==0x01:
            self.rtc="1"
        else:
            self.rtc="0"
        return {'port':'crystal','m':self.m,'rtc':self.rtc}

    def getl99m(self,data):
        self.l99m["port"]=str(data[2])
        self.l99m["state"]=str(data[3])
        return {'port':'l99m','v':self.l99m}

    def getpower(self,data):
        sid=data[2]
        fid=data[3]
        self.power["port"]=str(sid)
        self.power["state"]=str(fid)
        return {'port':'power','v':self.power}

    def getupgrade(self,data):
        sid=data[2]
        fid=data[3]
        state=data[4]
        if sid==0x01:
            if data[1]==0x01:
                self.insertsoft=""
            self.insertsoft+=self.Getdatabuff(data).decode("utf-8","replace")
        elif sid==0x02:
            self.upgradestate["port"]=str(fid)
            self.upgradestate["state"]=str(state)
        print(self.insertsoft)
        return {'port':'upgrade','v':self.upgradestate}

    def getlogin(self,data):
        self.loginstate=str(data[2])
        return {'port':'login','v':self.loginstate}

    def getlpm(self,data):
        self.lpmstate=str(data[2])
        return {'port':'lpm','v':self.lpmstate}

    def getsim(self,data):
        self.simstate=str(data[2])
        return {'port':'sim','v':self.simstate}

    def getlog(self,data):
        self.logstate=str(data[2])
        return {'port':'log','v':self.logstate}

    def getupload(self,data):
        self.upload=str(data[2])
        return {'port':'upload','v':self.upload}

    def geturl(self,data):
        sid=data[1]
        if sid==0x01:
            self.uploadurl=""
        self.uploadurl+=self.Getdatabuff(data).decode("utf-8")
        return {'port':'uploadurl','v':self.uploadurl}

    def getemc(self,data):
        self.emc["port"]=str(data[2])
        self.emc["state"]=str(data[3])
        return {'port':'emc','v':self.emc}

    def getLed(self,data):
        led={}
        led['port']=str(data[2])
        led['state']=str(data[3])
        return {'port':'led','v':led}

    def GetCanData(self,argument,data):
        switcher ={
            0x81:self.enterqc,
            0x82:self.outqc,
            0x80:self.dtuready,
            0x84:self.getboot,
            0x85:self.getapp,
            0x86:self.getqc,
            0x87:self.getdtusoft,
            0x88:self.getimei,
            0x89:self.getimsi,
            0x8a:self.getcsq,
            0x8b:self.getwifistate,
            0x8c:self.getwifissid,
            0x8d:self.getwifipwd,
            0x8e:self.getopenwifi,
            0x90:self.calld,
            0x91:self.calla,
            0x92:self.callh,
            0x93:self.getadc,
            0x94:self.gete2r,
            0x95:self.getemmc,
            0x98:self.getcan,
            0x99:self.getbattery,
            0x9a:self.getgps,
            0x9c:self.getgpio,
            0x9d:self.getjz,
            0x9e:self.getl99m,
            0x9f:self.getpower,
            0xa0:self.getupgrade,
            0xa1:self.getlogin,
            0xa2:self.getlpm,
            0xa3:self.getsim,
            0xa4:self.getlog,
            0xa5:self.getupload,
            0xa6:self.geturl,
            0xa7:self.getemc,
            0xa8:self.getLed,
        }
        func = switcher.get(argument,lambda:"nothing")
        return func(data)
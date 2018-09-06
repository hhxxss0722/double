#-*- coding:utf-8 -*-
import time
import datetime
from var import var
from file import fn
import threading 
import datahd
if var.ptform == "cwhl":
    from dtbs.hadoop import pySpark
elif var.ptform == "mlxy":
    from dtbs.mongo import pyMongo
from mail import eml
import xlshd

mylock = threading.RLock()  

class myThread(threading.Thread):  
    def __init__(self,conn_hd,data,abnormal,imeis):  
        threading.Thread.__init__(self)  
        self.conn_hd = conn_hd
        self.data = data
        self.abnormal = abnormal
        self.imeis = imeis
    def run(self):  
        while True:  
            mylock.acquire()  
            if var.len_imei > var.num_imei:
                imei = self.imeis[var.num_imei]
            else:
                mylock.release() 
                break
            var.num_imei += 1
            mylock.release()  

            #数据处理
            datahd.datahd(self.conn_hd,self.data,self.abnormal,imei.strip(),var.num_imei)


def main():
    try:
        #读取txt内保存的imei号
        ff = open(var.path_imei,"r")
        imeis = ff.readlines()
        var.len_imei = len(imeis)
        print var.len_imei
        
        #创建一个xls，sheet页分别为data和abnormal
        wbk,data,abnormal = fn.openxlwt()
        
        #在xls文件中写入head
        fn.write_dict_data(data,0,var.dict1)
        fn.write_dict_data(data,0,var.dict2)
        fn.write_dict_data(data,0,var.dict3)
        fn.write_dict_data(data,0,var.dict4)
        fn.write_dict_data(data,0,var.dict5)
        fn.write_dict_data(data,0,var.dict6)
        #connect platform 
        if var.ptform == "cwhl":
            transport = []
            for i in xrange(var.count_threading):
                transport.append(pySpark.impylaConnect("10.26.8.132",21051))
                time.sleep(1)
        elif var.ptform == "mlxy":
            transport = []
            for i in xrange(var.count_threading):
                transport.append(pyMongo.mongoConnect("10.21.7.74",32800))
                time.sleep(1)
            
        #多线程处理
        thread = []
        for i in xrange(var.count_threading):
            if var.ptform == "cwhl":
                t = myThread(transport[i],data,abnormal,imeis) 
            elif var.ptform == "mlxy":
                t = myThread(transport[i][1],data,abnormal,imeis) 
            thread.append(t)
        for i in xrange(var.count_threading):
            thread[i].start()
            time.sleep(0.2)
        for i in xrange(var.count_threading):
            thread[i].join()
            time.sleep(0.2)
        
        
        #汇总设备的登录、异常、获取数据失败的数量
        #datahd.write_lgin_nolgin_count(data)
        
    except Exception,ex:
        print Exception,'main:',ex
        
    finally:    
        #close platform
        if var.ptform == "cwhl":
            for i in xrange(var.count_threading):
                if transport[i] == -1 or transport[i] == None:
                    pass
                else:
                    pySpark.impylaClose(transport[i])
        elif var.ptform == "mlxy":
            for i in xrange(var.count_threading):
                if transport[i][0] != -1 or transport[i][0] != None:
                    pyMongo.mongoClose(transport[i][0])
            
        ff.close()
        fn.savexls(wbk,var.path_rslt)

if __name__ == "__main__":
    main()
    print "xls."
    if 1:#if var.type_imei = "imei":
        xlshd.login_record_everyday()
    print "eml."
    if var.mail_recv == "self":
        eml.mailsmtp()



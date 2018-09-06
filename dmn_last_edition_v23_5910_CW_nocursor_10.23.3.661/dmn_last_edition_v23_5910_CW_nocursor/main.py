#-*- coding:utf-8 -*-
import time,datetime
from variable import var
from database.mongo import pyMongo
from database.mysql import pyMysql
from filehandling import fn
import threading 
import datahd
from mail import eml
from xlshandling import xlshd
from xlutils.copy import copy
import xlwt,xlrd
import pymongo
if var.ctrl_sign != 'JG':
    from database.hadoop import pySpark


mylock = threading.RLock()  
mylock1 = threading.RLock() 
mylock2 = threading.RLock() 
mylock3 = threading.RLock() 
class myThread(threading.Thread):  
    def __init__(self,conn_hd,cursor_obd,data,abnormal,rows_imei):  
        threading.Thread.__init__(self)  
        self.conn_hd = conn_hd
        self.cursor_obd = cursor_obd
        self.data = data
        self.abnormal = abnormal
        self.rows_imei = rows_imei
    def run(self):  
        while True:  
            mylock.acquire()  
            if var.len_imei > var.num_imei:
                row_imei = self.rows_imei[var.num_imei]
            else:
                mylock.release() 
                break
            var.num_imei += 1
            mylock.release()  

            # 数据处理
            datahd.datahd(self.conn_hd,self.cursor_obd,self.data,self.abnormal,row_imei,var.num_imei)

class myThread1(threading.Thread):  
    def __init__(self,cursor_tcm,sht1,imei_dx):  
        threading.Thread.__init__(self)  
        self.cursor_tcm = cursor_tcm
        self.sht1 = sht1
        self.imei_dx = imei_dx

    def run(self):  
        while True:  
            mylock2.acquire()  
            if var.len_dx > var.num_dx:
                #print var.num_dx
                if self.imei_dx[var.num_dx] != "" and self.imei_dx[var.num_dx][:2] == "86":
                    imei = self.imei_dx[var.num_dx]
                else:
                    var.num_dx += 1
                    mylock2.release() 
                    continue
            else:
                mylock2.release() 
                break
            var.num_dx += 1
            num = var.num_dx-1
            mylock2.release()  
            print imei,num,var.len_dx,datetime.datetime.now()
            #数据处理
            sql = var.sql_upgrade1 + imei
            self.cursor_tcm.execute(sql)
            rows_tcm = self.cursor_tcm.fetchall() 
            mylock3.acquire()  
            ln = len(rows_tcm)
            dt1 = datetime.datetime.strptime(var.dt, '%Y%m%d')
            for i in xrange(ln):
                dt2 = rows_tcm[ln-1-i][0]
                #print dt2,type(dt2)
                if (dt2-dt1).days == 0:
                    var.sign_rst += 1
                elif (dt2-dt1).days < 0:
                    break
                else:
                    pass
            if var.sign_rst > 0:
                fn.write_single_data(self.sht1,num,var.col_count_reset,var.sign_rst)
                var.sign_rst = 0
            # 获取批次
            fn.write_single_data(self.sht1,num,var.col_batch,datahd.product_batch(self.cursor_tcm,imei))
            
            mylock3.release()  



def main():
    try:
        '''
        database connect
        '''
        # connect mysql obd database
        conn_obd,cursor_obd = pyMysql.mysqlConnect( var.sql_ip_obd,
                                                    var.sql_name_obd,
                                                    var.sql_pw_obd,
                                                    var.sql_base_obd,
                                                    var.sql_char_obd
                                                    )

        # from obd db get imei
        if var.model_sign == 0 or var.model_sign == 1 :
            rows_imei = pyMysql.mysqlGetMessage(cursor_obd,var.sql_getimei)
            # close mysql obd cursor and obd
            if conn_obd != -1 or conn_obd != None:
                pyMysql.mysqlClose(conn_obd,cursor_obd)
            
        else:
            file_imei,rows_imei = fn.open_file_imei(var.file_imei_txt)
        # 得到imei的数量
        var.len_imei = len(rows_imei)
        #print var.len_imei
        wbk,data,abnormal = fn.openxlwt()
        fn.write_dict_data(data,0,var.dict1)
        fn.write_dict_data(data,0,var.dict1_1)
        fn.write_dict_data(data,0,var.dict2)
        fn.write_dict_data(data,0,var.dict3)
        fn.write_dict_data(data,0,var.dict4)
        fn.write_dict_data(data,0,var.dict5)
        fn.write_dict_data(data,0,var.dict6)
        
        if var.ctrl_sign == 'JG':
            # connect mongo database
            transport = []
            for i in xrange(var.count_threading):
                transport.append(pyMongo.mongoConnect(var.mongo_ip,var.mongo_port))
                time.sleep(1)
            #print transport
            thread = []
            # 多线程处理
            for i in xrange(var.count_threading):
                t = myThread(transport[i][1],cursor_obd,cursor_obd,transport[i][1],data,abnormal,rows_imei,1) 
                thread.append(t)
            for i in xrange(var.count_threading):
                thread[i].start()
                time.sleep(0.2)

            for i in xrange(var.count_threading):
                thread[i].join()
                time.sleep(0.2)

        else:
            '''
            # connect mysql serviceopen database
            conn_csr,cursor_csr = pyMysql.mysqlConnect( var.sql_ip_csr,
                                                        var.sql_name_csr,
                                                        var.sql_pw_csr,
                                                        var.sql_base_csr,
                                                        var.sql_char_csr
                                                        )
            
            # connect mongo database
            conn_mg,cursor_mg = pyMongo.mongoConnect(   var.mongo_ip,
                                                        var.mongo_port
                                                        )
            
            # connect mysql tcm database
            conn_tcm,cursor_tcm = pyMysql.mysqlConnect( var.sql_ip_tcm,
                                                        var.sql_name_tcm,
                                                        var.sql_pw_tcm,
                                                        var.sql_base_tcm,
                                                        var.sql_char_tcm
                                                        )
            '''
            # connect hadoopSpark database
            transport = []
            for i in xrange(var.count_threading):
                transport.append(pySpark.impylaConnect("10.26.8.132",21051))
                
                '''
                transport.append(pySpark.hadoopConnect( var.hadoop_ip,
                                                         var.hadoop_port,
                                                         var.hadoop_name,
                                                         var.hadoop_pw,
                                                         var.hadoop_database,
                                                         var.hadoop_authMechanism
                                                        )
                                )
                '''
                time.sleep(1)
            #print transport
            # 多线程处理
            thread = []
            for i in xrange(var.count_threading):
                t = myThread(transport[i],cursor_obd,data,abnormal,rows_imei) 
                thread.append(t)
            #print thread
            for i in xrange(var.count_threading):
                thread[i].start()
                time.sleep(0.2)
            
            for i in xrange(var.count_threading):
                thread[i].join()
                time.sleep(0.2)
            
        
        # 汇总设备的登录、异常、获取数据失败的数量
        datahd.write_lgin_nolgin_count(data)
        
    except Exception,ex:
        print Exception,'main:',ex
        
    finally:
        if var.model_sign == 0 or var.model_sign == 1 :
            pass
        else:
            # close mysql obd cursor and obd
            if conn_obd == -1 or conn_obd == None:
                pass
            else:
                
                pyMysql.mysqlClose(conn_obd,cursor_obd)
        
        if var.ctrl_sign == 'JG':
            # close mongo db
            for i in xrange(var.count_threading):
                if transport[i][0] != -1 or transport[i][0] != None:
                    pyMongo.mongoClose(transport[i][0])

        else:
            
                
            # close hadoopSpark cursor and db
            for i in xrange(var.count_threading):
                if transport[i] != -1 or transport[i] != None:
                    pySpark.impylaClose(transport[i])
        fn.savexls(wbk,var.excel_file_name)
        if var.model_sign == 2 or var.model_sign == 3:
            fn.close_file_imei(file_imei)

def xlsmongo():
    wbk_dx,table_dx = fn.openxlrd(var.excel_file_name,u'data')
    imei_dx = table_dx.col_values(var.col_imei)
    tid_dx = table_dx.col_values(var.col_tid)
    applogin_dx = table_dx.col_values(var.col_applogin)
    var.len_dx = len(imei_dx)
    #print imei_dx
    #print applogin_dx
    # 复制xls
    wbk_cp = copy(wbk_dx)
    sht1 = wbk_cp.get_sheet(0)
    '''
    # connect mongo database
    conn_mg,cursor_mg = pyMongo.mongoConnect(   var.mongo_ip,
                                                var.mongo_port
                                                )
    try:
        
        for index_dx in xrange(var.len_dx):
            imei = imei_dx[index_dx]
            
            if imei != "" and imei[:2] == "86":
                print imei,index_dx,var.len_dx,datetime.datetime.now()
                tid = tid_dx[index_dx]
                applogin = applogin_dx[index_dx]
                num = index_dx
                
                # 数据库查询起始时间
                login_rows = pyMongo.mongoGetMessage(cursor_mg,{'tid':int(tid)}).sort([('Time', pymongo.DESCENDING)])
                if login_rows != -1:
                    login_len = login_rows.count()
                    if login_len == 0:
                        fn.write_single_data(sht1,num,var.col_date,'no record')
                    else:
                        # 设备起始时间、当前在线状态的判断
                        if login_rows[0]['type'] == 1:
                            fn.write_single_data(sht1,num,var.col_date,str(login_rows[0]['Time'] + datetime.timedelta(hours = 8))+ ' - ' + str(login_rows[login_len-1]['Time'] + datetime.timedelta(hours = 8)) + u' :登出' + '\n')
                        elif login_rows[0]['type'] == 0:
                            fn.write_single_data(sht1,num,var.col_date,str(login_rows[0]['Time'] + datetime.timedelta(hours = 8))+ ' - ' + str(login_rows[login_len-1]['Time'] + datetime.timedelta(hours = 8)) + u' :登录' + '\n')
                        else:
                            fn.write_single_data(sht1,num,var.col_date,str(login_rows[0]['Time'] + datetime.timedelta(hours = 8))+ ' - ' + str(login_rows[login_len-1]['Time'] + datetime.timedelta(hours = 8)) + u' :错误' + '\n')
                        
                        fn.write_single_data(sht1,num,var.col_runtime,(login_rows[0]['Time']-login_rows[login_len-1]['Time']).days)

                        # 统计用户最近登录时间与设备最近登录登出的情况
                        if applogin != "" and applogin[:3] == "201":
                            apploginrecord = datetime.datetime.strptime(applogin, '%Y-%m-%d %H:%M:%S')
                            fn.write_single_data(sht1,num,var.col_action,((login_rows[0]['Time'] + datetime.timedelta(hours = 8)) - apploginrecord).days)
                        
                        #col_count_in、col_count_out 对应var dict3的参数
                
                        # 设备查询日当天登录、登出次数的处理
                        tmp = datetime.datetime.strptime(var.dt, '%Y%m%d')
                        for login_row in login_rows:
                            # 当天 == 0
                            if ((login_row['Time'] + datetime.timedelta(hours = 8)) - tmp).days == 0 :
                                if login_row['type'] == 1:
                                    var.count_out += 1
                                elif login_row['type'] == 0:
                                    var.count_in += 1
                                else:
                                    print 'login_rows type error.'
                            # 前一天 < 0 
                            elif ((login_row['Time'] + datetime.timedelta(hours = 8)) - tmp).days < 0:
                                break
                            # 后一天 > 0
                            else:
                                pass
                        if var.count_in > 0 :
                            fn.write_single_data(sht1,num,var.col_count_in,var.count_in)
                        if var.count_out > 0:
                            fn.write_single_data(sht1,num,var.col_count_out,var.count_out)
                        var.count_in,var.count_out = 0,0
                else:
                    fn.write_single_data(sht1,num,var.col_date,'server_error')

    except Exception,ex:
        print Exception,"xlsmongo:",ex
    finally:
        # close mongo db
        if conn_mg != -1 or conn_mg != None:
            pyMongo.mongoClose(conn_mg)
    '''
    # connect mysql tcm database

    try:
        count_mysql = 2
        transport = []
        print var.sql_ip_tcm,var.sql_name_tcm,var.sql_pw_tcm,var.sql_base_tcm,var.sql_char_tcm
        for i in xrange(count_mysql):
            transport.append(pyMysql.mysqlConnect( var.sql_ip_tcm,var.sql_name_tcm,var.sql_pw_tcm,var.sql_base_tcm,var.sql_char_tcm)
)

        # 多线程处理
        thread = []
        for i in xrange(count_mysql):
            t = myThread1(transport[i][1],sht1,imei_dx) 
            thread.append(t)
        #print thread
        for i in xrange(count_mysql):
            thread[i].start()
            time.sleep(0.2)
        
        for i in xrange(count_mysql):
            thread[i].join()
            time.sleep(0.2)
            
    except Exception,ex:
        print Exception,"xlsmysql:",ex
    finally:
        for i in xrange(count_mysql):
            if transport[i][0] != -1 or transport[i][0] != None:
                pyMysql.mysqlClose(transport[i][0],transport[i][1])
            
    wbk_cp.save(var.excel_file_name)
    #wbk_cp.save('/root/xiao/tst/11.xls')
    
def xls_eml():
    if var.ismail == 'ym' or var.ismail == 'YM':
        try:
            wbk_dx,table_dx = fn.openxlrd(var.excel_file_name,u'data')
            
            xlshd.obd_login_table(wbk_dx,table_dx)
            time.sleep(1)

            xlshd.xls_handling(wbk_dx,table_dx)
            time.sleep(1)
            var.row_bg = 0
            eml.mailsmtp()
        except Exception,ex:
            var.row_bg = 0
            print Exception,"mail:",ex
    elif var.ismail == 'nm' or var.ismail == 'NM':
        pass
    else:
        print 'input ym(nm) error'
    

if __name__ == '__main__':

    if var.model_sign == 0:
        while 1:
            nowhour = datetime.datetime.now().strftime('%H')
            exehour = '02'
            if nowhour == exehour:
                var.dt = ''.join(str(datetime.date.today()- datetime.timedelta(1)).split('-'))
                var.excel_file_name = var.save_excel_path_1 + var.dt + '-' + datetime.datetime.now().strftime('%H%M%S') + var.save_excel_path_2
                var.len_imei,var.num_imei,var.server_error,var.login_imei,var.nologin_imei,var.ct_sms = 0,0,0,0,0,0
                main()
                time.sleep(1)
                if var.server_error < 100:
                    xlsmongo()
                    time.sleep(1)
                    xls_eml()
                    time.sleep(2)
                    break
            else:
                print nowhour,exehour,'time.sleep(900)',datetime.datetime.now(),'var.dt = ',var.dt
                time.sleep(900)
    elif var.model_sign == 1:
        main()
        time.sleep(1)
        if var.server_error < 100:
            #xlsmongo()
            time.sleep(1)
            xls_eml()
        
    elif var.model_sign == 2:
        main()
        time.sleep(1)
        if var.server_error == 0:
            if var.ismail == 'YM':
                xlsmongo()
            else:
                pass
            time.sleep(1)
        xls_eml()
    elif var.model_sign == 3:
        main()
        time.sleep(1)
        if var.server_error == 0:
            #xlsmongo()
            time.sleep(1)
            xls_eml()
    
    else:
        while 1:
            main()
            time.sleep(1)
            xls_eml()
            var.len_imei,var.num_imei,var.server_error,var.login_imei,var.nologin_imei = 0,0,0,0,0
            print 'time sleep 1800',datetime.datetime.now(),'var.dt = ',var.dt
            time.sleep(1800)
        



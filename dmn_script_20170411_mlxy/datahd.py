#-*- coding:utf-8 -*-
from file import fn
import datetime
from var import var
from var import gps
import re
import sys
import main
import time
if var.ptform == "cwhl":
    from dtbs.hadoop import pySpark
elif var.ptform == "mlxy":
    from dtbs.mongo import pyMongo


def sht2_write_error(sht2,num,data):
    if var.cl_sht2 < var.cl_vale:
        fn.write_single_data(sht2,num,var.cl_sht2,data)
        var.cl_sht2 += 1
    

#平台下发的配置信息
def conf_info(data,num,sht2):
    #todo var.count_fbox += 1
    conf = re.search(var.re_conf,data)
    if conf is not None:
        var.st_fbox = conf.group(1)
        var.st_amvl = conf.group(2)
        var.st_shak = conf.group(3)
        var.st_agps = conf.group(4)
        var.st_coll = conf.group(6)
    else:
        sht2_write_error(sht2,num,data)
        


#数据延迟判定
def judge_delay(data,num,sht2,dt_tm,dp_tm):
    if dt_tm[:10] != "0000-00-00" and dt_tm[:10] != "1970-01-01":
        try:
            #print dt_tm,data_process_time
            dt1 = datetime.datetime.strptime(dt_tm, "%Y-%m-%d %H:%M:%S")
            dp1 = datetime.datetime.strptime(dp_tm, "%Y%m%d %H:%M:%S")
            dt2 = datetime.datetime.strptime(var.dt, "%Y%m%d")
            '''
            #total_seconds()在linux py2.6.6中报错，用用其他方式
            dt_sec1 = (dp1 - dt1).total_seconds()
            #平台接收时间与写包时间相差10800s,则判定为延迟..
            if dt_sec1 > 10800:
                var.ct_dely  += 1
            dt_sec2 = (dt2 - dt1).total_seconds()
            if dt_sec2 <= 0:#查询日期的当天数据
                var.tmp_dy0 += 1
            elif 86400 * 0 < dt_sec2 <= 86400 * 1:#查询日期的前一天数据
                var.tmp_dy1 += 1
            elif 86400 * 1 < dt_sec2 <= 86400 * 2:#查询日期的前两天数据
                var.tmp_dy2 += 1
            elif 86400 * 2 < dt_sec2 <= 86400 * 3:#查询日期的前三天数据
                var.tmp_dy3 += 1
            elif 86400 * 3 < dt_sec2 <= 86400 * 4:#查询日期的前四天数据
                var.tmp_dy4 += 1
            elif 86400 * 4 < dt_sec2 <= 86400 * 5:#查询日期的前五天数据
                var.tmp_dy5 += 1
            else:#前六天及前的数据
                var.tmp_dy6 += 1
            '''
            dt_sec1 = (dp1 - dt1).seconds #时间部分相差秒数
            dt_day1 = (dp1 - dt1).days   #相差天数
            if (dt_day1 == 0 and dt_sec1 > 10800) or (dt_day1 >= 1):
                var.ct_dely  += 1
            dt_day2 = (dt2 - dt1).days   #相差天数
            if dt_day2 <= -1:#查询日期的当天及以后的数据
                var.tmp_dy0 += 1
            elif dt_day2 == 0:#查询日期的前一天数据
                var.tmp_dy1 += 1
            elif dt_day2 == 1:#查询日期的前两天数据
                var.tmp_dy2 += 1
            elif dt_day2 == 2:#查询日期的前三天数据
                var.tmp_dy3 += 1
            elif dt_day2 == 3:#查询日期的前四天数据
                var.tmp_dy4 += 1
            elif dt_day2 == 4:#查询日期的前五天数据
                var.tmp_dy5 += 1
            else:#前六天及以前的数据
                var.tmp_dy6 += 1
            
        except:
            var.er_time += 1
            sht2_write_error(sht2,num,data)

    else:
        pass
   
#数据重复统计
def repeat_statistics(data,dt_tm,dt_tp):
    if cmp(var.tmp_tm,dt_tm) == 0 and cmp(var.tmp_tp,dt_tp) == 0 and ">1014<" not in data:
        var.ct_rept += 1
        var.tmp_tm = dt_tm
        var.tmp_tp = dt_tp
        
    else:
        var.tmp_tm = dt_tm
        var.tmp_tp = dt_tp
#1004包的处理
def pk_1004(data,num,sht2):
    pk_1004 = re.search(var.re_1004,data)
    if pk_1004 is not None:
        volt_1004 = float(pk_1004.group(7))
        #var.dc_volt[pk_1004.group(2)] = volt_1004
        if volt_1004 < 11.3:
            var.ct_vlow += 1

    else:
        var.er_1004 += 1
        sht2_write_error(sht2,num,data)

#2001包的处理
def pk_2001(data,num,sht2):
    pk_2001 = re.search(var.re_2001,data)
    if pk_2001 is not None:
        pass
        #todo 2001车辆数据分析
    else:
        var.er_2001 += 1
        sht2_write_error(sht2,num,data)
        
#pk_2021包的处理
def pk_2021(data,num,sht2):
    pk_2021 = re.search(var.re_2021,data)
    if pk_2021 is not None:
        lac_2021 = pk_2021.group(1)
        if var.tmp_lac == "":
            var.tmp_lac = lac_2021
        elif cmp(var.tmp_lac,lac_2021) != 0:
            #var.ct_omsn += 1
            pass
        else:
            pass
    else: 
        var.er_2021 += 1
        sht2_write_error(sht2,num,data)

#pk_2031包的处理
def pk_2031(data,num,sht2):
    pk_2031 = re.search(var.re_2031,data)
    if pk_2031 is not None:
        pass
    else: 
        var.er_2031 += 1
        sht2_write_error(sht2,num,data)

#pk_3021包的处理
def pk_3021(data,num,sht2):
    pk_3021 = re.search(var.re_3021,data)
    if pk_3021 is not None:
        if re.search("4E3A002D",data) is not None:
            var.er_3021 += 1
            sht2_write_error(sht2,num,data)
        else:
            pass
    else: 
        var.er_3021 += 1
        sht2_write_error(sht2,num,data)
#pk_3022包的处理
def pk_3022(data,num,sht2):
    pk_3022 = re.search(var.re_3022,data)
    if pk_3022 is not None:
        var.st_imsi = pk_3022.group(1)
        var.st_ccid = pk_3022.group(2)
        if pk_3022.group(3)[:1] == "+":
            var.st_numb = pk_3022.group(3)[1:]
        else:
            var.st_numb = pk_3022.group(3)
    else: 
        var.er_3022 += 1
        sht2_write_error(sht2,num,data)

#pk_3031包的处理
def pk_3031(data,num,sht2):
    pk_3031 = re.search(var.re_3031,data)
    if pk_3031 is not None:
        pass
    else: 
        var.er_3031 += 1
        sht2_write_error(sht2,num,data)

#pk_3032包的处理
def pk_3032(data,num,sht2):
    pk_3032 = re.search(var.re_3032,data)
    if pk_3032 is not None:
         var.dc_dscn.append(pk_3032.group(1))
    else: 
        var.er_3032 += 1
        sht2_write_error(sht2,num,data)

#4001包的处理
def pk_4001(data,num,sht2,dt_tm):
    pk_4001 = re.search(var.re_4001,data)
    if pk_4001 is not None:
        vin = pk_4001.group(5)
        if len(vin) == 17:
            var.st_vinn = vin
        elif vin == "null":
            pass
        else:
            var.er_4001 += 1
            sht2_write_error(sht2,num,data)
    else:
        var.er_4001 += 1
        sht2_write_error(sht2,num,data)
        
#4002包的处理
def pk_4002(data,num,sht2,dt_tm):
    pk_4002 = re.search(var.re_4002,data)
    if pk_4002 is not None:
        if pk_4002.group(1) != "<a>-1.0</a><o>-1.0</o><s>-1.0</s>":
            speed_4002 = pk_4002.group(4)
            if speed_4002 != -1.0:
                if float(speed_4002) > 35.0:
                    #var.ct_msjd += 1
                    pass
    else:
        var.er_4002 += 1
        sht2_write_error(sht2,num,data)

#4011包的处理
def pk_4011(data,num,sht2):
    pk_4011 = re.search(var.re_4011,data)
    if pk_4011 is not None:
        var.ct_vlow += 1
        volt_4011 = float(pk_4011.group(2))
        #var.dc_volt[pk_4011.group(1)] = volt_4011
    else:
        var.er_4011 += 1
        sht2_write_error(sht2,num,data)

#pk_5001包的处理
def pk_5001(data,num,sht2):
    pk_5001 = re.search(var.re_5001,data)
    if pk_5001 is not None:
        if pk_5001.group(1) != "<a>-1.0</a><o>-1.0</o><s>-1.0</s>":
            try:
                speed_gps = float(pk_5001.group(4))
            except Exception,ex:
                speed_gps = 0.0
                print Exception,":",ex
            if speed_gps > 10.0:
                var.ct_omsn += 1
            else:
                pass
    else: 
        var.er_5001 += 1
        sht2_write_error(sht2,num,data)

#pk_5005包的处理
def pk_5005(data,num,sht2):
    pk_5005 = re.search(var.re_5005,data)
    if pk_5005 is not None:
        pass
    else: 
        var.er_5005 += 1
        sht2_write_error(sht2,num,data)
        
#pk_5006包的处理
def pk_5006(data,num,sht2):
    pk_5006 = re.search(var.re_5006,data)
    if pk_5006 is not None:
        pass
    else: 
        var.er_5006 += 1
        sht2_write_error(sht2,num,data)


#pk_9000包的处理
def pk_9000(data,num,sht2):
    pk_9000 = re.search(var.re_9000,data)
    if pk_9000 is not None:
        pass
    else: 
        var.er_9000 += 1
        sht2_write_error(sht2,num,data)

#pk_9990包的处理
def pk_9990(data,num,sht2):
    pk_9990 = re.search(var.re_9990,data)
    if pk_9990 is not None:
        pass
    else: 
        var.er_9990 += 1
        sht2_write_error(sht2,num,data)


#9999包
def pk_9999(data,num,sht2):
    if "<debug_infor>9667</debug_infor>" not in data:
        pk_9999 = re.search(var.re_9999,data)
        if pk_9999 is not None:
            infor_x = pk_9999.group(2)
            volt_9999 = float(pk_9999.group(5))
            #var.dc_volt[pk_9999.group(1)] = volt_9999
            if infor_x == "0":
                var.ct_0 += 1
            elif infor_x == "1":
                var.ct_1 += 1
            elif infor_x == "2":
                var.ct_2 += 1
            elif infor_x == "3":
                var.ct_3 += 1
            elif infor_x == "4":
                var.ct_4 += 1
            elif infor_x == "5":
                var.ct_5 += 1
            elif infor_x == "6":
                var.ct_6 += 1
            elif infor_x == "7":
                var.ct_7 += 1
            elif infor_x == "1014":
                var.ct_1014 += 1
            elif infor_x == "9011":
                var.ct_9011 += 1
            elif infor_x == "9021":
                var.ct_9021 += 1
            elif infor_x == "9031":
                var.ct_9031 += 1
            elif infor_x == "9051":
                var.ct_9051 += 1
            elif infor_x == "9052":
                var.ct_9052 += 1
            elif infor_x == "9053":
                var.ct_9053 += 1
            elif infor_x == "9054":
                var.ct_9054 += 1
            elif infor_x == "9061":
                var.ct_9061 += 1
            elif infor_x == "9071":
                var.ct_9071 += 1
            elif infor_x == "9072":
                var.ct_9072 += 1
            elif infor_x == "9073":
                var.ct_9073 += 1
            elif infor_x == "9074":
                var.ct_9074 += 1
            elif infor_x == "9075":
                var.ct_9075 += 1
            elif infor_x == "9076":
                var.ct_9076 += 1
            elif infor_x == "9081":
                var.ct_9081 += 1
            elif infor_x == "9082":
                var.ct_9082 += 1
            elif infor_x == "9100":
                var.ctg_9100 += 1
            elif infor_x == "9101":
                var.ct_9101 += 1
            elif infor_x == "9102":
                var.ct_9102 += 1
            elif infor_x == "9103":
                var.ct_9103 += 1
            elif infor_x == "9109":
                var.ct_9109 += 1
            elif infor_x == "9301":
                var.ct_9301 += 1
            elif infor_x == "9303":
                var.ct_9303 += 1
            elif infor_x == "9304":
                var.ct_9304 += 1
            elif infor_x == "9305":
                var.ct_9305 += 1
            elif infor_x == "9306":
                var.ct_9306 += 1
            elif infor_x == "9307":
                var.ct_9307 += 1
            elif infor_x == "9308":
                var.ct_9308 += 1
            elif infor_x == "9309":
                var.ct_9309 += 1
            elif infor_x == "9310":
                var.ct_9310 += 1
            elif infor_x == "9331":
                var.ct_9331 += 1
            elif infor_x == "9332":
                var.ct_9332 += 1
            elif infor_x == "9401":
                var.ct_9401 += 1
            elif infor_x == "9993":
                var.ct_9993 += 1
            elif infor_x == "9994":
                var.ct_9994 += 1
            elif infor_x == "9665":
                var.ct_9995 += 1
            elif infor_x == "3001":
                var.ct_3001 += 1
            elif infor_x == "3002":
                var.ct_3002 += 1
            elif infor_x == "3003":
                var.ct_3003 += 1
            elif infor_x == "3004":
                var.ct_3004 += 1
            elif infor_x == "3005":
                var.ct_3005 += 1
            elif infor_x == "3006":
                var.ct_3006 += 1
            elif infor_x == "3007":
                var.ct_3007 += 1
            elif infor_x == "3008":
                var.ct_3008 += 1
                if "BKP_DR42:0" in data:
                    var.ct_3015 += 1
                elif "BKP_DR42:2" in data:
                    var.ct_3014 += 1
                elif "BKP_DR42:1" in data:
                    var.ct_3013 += 1
            elif infor_x == "3009":
                var.ct_3009 += 1
                csq_str = pk_9999.group(3)
                ln = len(csq_str)
                for csq in csq_str[14:ln-15].split(","):
                    #csq 14 == -85
                    if(14 < int(csq) <= 31):
                        var.ctg_9100 += 1
                    elif(5 <= int(csq) <= 14):
                        var.ct_9101 += 1
                    else:
                        var.ct_9102 += 1
            elif infor_x == "3010":
                var.ct_3010 += 1
            elif infor_x == "3011":
                var.ct_3011 += 1
                if "tick_st:901" in data:
                    var.ct_3012 += 1
            elif infor_x == "3012":
                var.ct_3012 += 1
            elif infor_x == "3013":
                var.ct_3013 += 1
            elif infor_x == "3014":
                var.ct_3014 += 1
            elif infor_x == "3015":
                var.ct_3015 += 1
            
            # 统计其他的异常情况
            else:
                pass
        else:
            var.er_9999 += 1
            sht2_write_error(sht2,num,data)
        
      

def variable():
    var.ct_1004,var.ct_2001,var.ct_2011,var.ct_2021,var.ct_2031,var.ct_3021,var.ct_3022,var.ct_3031,var.ct_3032,var.ct_4001,var.ct_4002,var.ct_4011,\
    var.ct_5001,var.ct_5005,var.ct_5006,var.ct_6001,var.ct_9000,var.ct_9100,var.ct_9990,var.ct_9999,var.ct_dely,var.ct_rept,var.ct_bnds,\
    var.ct_omsn,var.ct_msjd,var.ct_vlow,var.ct_conn = [0] * 27
    
    var.er_1004,var.er_2001,var.er_2011,var.er_2021,var.er_2031,var.er_3021,var.er_3022,var.er_3031,var.er_3032,var.er_4001,var.er_4002,var.er_4011,\
    var.er_5001,var.er_5005,var.er_5006,var.er_6001,var.er_9000,var.er_9100,var.er_9990,var.er_9999,var.er_time = [0] * 21
    
    var.ct_0,   var.ct_1,   var.ct_2,   var.ct_3,   var.ct_4,   var.ct_5,   var.ct_6,   var.ct_7,   var.ct_1014,var.ct_9011,var.ct_9021,\
    var.ct_9031,var.ct_9051,var.ct_9052,var.ct_9053,var.ct_9054,var.ct_9061,var.ct_9071,var.ct_9072,var.ct_9073,var.ct_9074,var.ct_9075,\
    var.ct_9076,var.ct_9081,var.ct_9082,var.ctg_9100,var.ct_9101,var.ct_9102,var.ct_9103,var.ct_9109,var.ct_9301,var.ct_9303,var.ct_9304,\
    var.ct_9305,var.ct_9306,var.ct_9307,var.ct_9308,var.ct_9309,var.ct_9310,var.ct_9331,var.ct_9332,var.ct_9333,var.ct_9401,var.ct_9993,\
    var.ct_9994,var.ct_9995 = [0] * 46

    var.tmp_tm,var.tmp_tp,var.tmp_gps,var.tmp_41,var.tmp_42,var.tmp_lac = [""] * 6
    var.tmp_dy0,var.tmp_dy1,var.tmp_dy2,var.tmp_dy3,var.tmp_dy4,var.tmp_dy5,var.tmp_dy6 = [0] * 7
    
    var.st_imei,var.st_lgin,var.st_mast,var.st_cm33,var.st_vinn = [""] * 5
    
    var.dc_volt,var.dc_dscn,var.dc_dlay = {},[],{}
    var.st_fbox,var.st_amvl,var.st_shak,var.st_agps,var.st_coll,var.st_imsi,var.st_ccid,var.st_numb = [""] * 8
    var.ct_3001,var.ct_3002,var.ct_3003,var.ct_3004,var.ct_3005,var.ct_3006,var.ct_3007,var.ct_3008,var.ct_3009,var.ct_3010,var.ct_3011,\
    var.ct_3012,var.ct_3013,var.ct_3014,var.ct_3015 = [0] * 15
    var.cl_sht2 = 1
    
def base_info():
    #print var.tmp_dy0,var.tmp_dy1,var.tmp_dy2,var.tmp_dy3,var.tmp_dy4,var.tmp_dy5,var.tmp_dy6
    if len(var.dc_dscn) > 500:
        var.dc_dscn = {"dict":"too big."}
    if var.tmp_dy0 > 0:
        var.dc_dlay['day0'] = var.tmp_dy0
    if var.tmp_dy1 > 0:
        var.dc_dlay['day1'] = var.tmp_dy1
    if var.tmp_dy2 > 0:
        var.dc_dlay['day2'] = var.tmp_dy2
    if var.tmp_dy3 > 0:
        var.dc_dlay['day3'] = var.tmp_dy3
    if var.tmp_dy4 > 0:
        var.dc_dlay['day4'] = var.tmp_dy4
    if var.tmp_dy5 > 0:
        var.dc_dlay['day5'] = var.tmp_dy5
    if var.tmp_dy6 > 0:
        var.dc_dlay['day6'] = var.tmp_dy6    
    
def datahd(conn_hd,sht1,sht2,imei,num):
    try:
        fn.write_single_data(sht2,num,0,imei)
        if var.ptform == "cwhl":
            #print imei,num,datetime.datetime.now()
            sql_hd = var.sql_hd1 + var.dt + var.sql_hd2 + imei + var.sql_hd3
            rows_hd = pySpark.impylaGetMessage(conn_hd,sql_hd)
            main.mylock.acquire()
            var.st_imei = imei
            if rows_hd == -1:
                #impyla获取数据失败
                var.ct_svrr += 1
                var.st_lgin = "svr_err"
            elif rows_hd == []:
                #impyla获取数据为空
                var.ct_nlgin += 1
                var.st_lgin = "nolgin"
            else:
                for rows in rows_hd:
                    if "UP" in rows:
                        lgin_sign = 1
                        break
                    else:
                        lgin_sign = 0
                if lgin_sign == 0:
                    #impyla获取数据有下发\无上报
                    var.ct_nlgin += 1
                    var.st_lgin = "nolgin"
                else:
                    #有效数据处理
                    var.ct_lgin += 1
                    var.st_lgin = "login"
                    for line in xrange(len(rows_hd)):
                        #print line,len(rows_hd),rows_hd[line]
                        up_dn = rows_hd[line][0]
                        data = rows_hd[line][1]
                        ps_tm = rows_hd[line][2]
                        #print data
                        if up_dn == "DOWN" and len(data) > 100:
                            #解析平台下发的配置信息
                            conf_info(data,num,sht2)
                        elif data[:2] == "11":
                            #解析login包,主控和cm3版本
                            var.ct_conn += 1
                            var.st_cm33 = data[3:13]
                            var.st_mast = data[13:23]
                        elif 10 < len(data) < 35 and "~" not in data:
                            #BNDS包的处理
                            var.ct_bnds += 1
                        else:
                            dt_tp = re.search(var.re_type,data)
                            dt_tm = re.search(var.re_time,data)
                            if dt_tm is None or dt_tp is None:
                                if "~" in data:
                                    var.ct_2011 += 1
                                    if cmp(var.tmp_gps,data) == 0:
                                        var.ct_rept += 1
                                        var.tmp_gps = data
                                    #todo 2011解析  原始报文暂无法解析  pk_2011(data,num,sht2)
                            else:
                                dt_tm = dt_tm.group(1)
                                dt_tp = dt_tp.group(1)
                                
                                #数据延迟判定
                                judge_delay(data,num,sht2,dt_tm,ps_tm)
                                
                                #数据重复统计
                                repeat_statistics(data,dt_tm,dt_tp)
                                
                                #按照数据包的类型进行解析
                                if dt_tp == "1004" or dt_tp == "1002":
                                    var.ct_1004 += 1
                                    pk_1004(data,num,sht2)
                                elif dt_tp == "2001":
                                    var.ct_2001 += 1
                                    pk_2001(data,num,sht2)
                                elif dt_tp == "2011":
                                    var.ct_2011 += 1
                                elif dt_tp == "2021":
                                    var.ct_2021 += 1
                                    pk_2021(data,num,sht2)
                                elif dt_tp == "2031":
                                    var.ct_2031 += 1
                                    pk_2031(data,num,sht2)
                                elif dt_tp == "3021":
                                    var.ct_3021 += 1
                                    pk_3021(data,num,sht2)
                                elif dt_tp == "3022":
                                    var.ct_3022 += 1
                                    pk_3022(data,num,sht2)
                                elif dt_tp == "3031":
                                    var.ct_3031 += 1
                                    pk_3031(data,num,sht2)
                                elif dt_tp == "3032":
                                    var.ct_3032 += 1
                                    pk_3032(data,num,sht2)
                                elif dt_tp == "4001":
                                    if cmp(var.tmp_41,dt_tm) != 0:
                                        var.ct_4001 += 1
                                        var.tmp_41 = dt_tm
                                        pk_4001(data,num,sht2,dt_tm)
                                elif dt_tp == "4002":
                                    if cmp(var.tmp_42,dt_tm) != 0:
                                        var.ct_4002 += 1
                                        var.tmp_42 = dt_tm
                                        pk_4002(data,num,sht2,dt_tm)
                                elif dt_tp == "4011":
                                    var.ct_4011 += 1
                                    pk_4011(data,num,sht2)
                                elif dt_tp == "5001":
                                    var.ct_5001 += 1
                                    pk_5001(data,num,sht2)
                                elif dt_tp == "5005":
                                    var.ct_5005 += 1
                                    pk_5005(data,num,sht2)
                                elif dt_tp == "5006":
                                    var.ct_5006 += 1
                                    pk_5006(data,num,sht2)
                                elif dt_tp == "6001":
                                    var.ct_6001 += 1
                                    #todo 6001解析    pk_6001(data,num,sht2)
                                elif dt_tp == "9000":
                                    var.ct_9000 += 1
                                    pk_9000(data,num,sht2)
                                elif dt_tp == "9100":
                                    var.ctg_9100 += 1
                                    #9100有2种类型的包
                                    #todo 9100解析    pk_9100(data,num,sht2)
                                elif dt_tp == "9990":
                                    var.ct_9990 += 1
                                    pk_9990(data,num,sht2)
                                elif dt_tp == "9999":
                                    var.ct_9999 += 1
                                    pk_9999(data,num,sht2)
                                else:
                                    pass
        elif var.ptform == "mlxy":
            print imei,num,datetime.datetime.now()
            rows_hd = pyMongo.mongoGetMessage(conn_hd,{'imei':imei.strip(),'process_time':{'$regex':var.dt}})
            #sql = {'imei':"869267018412010",'process_time':{'$regex':var.dt}}
            #rows_hd = conn_hd.obd_raw_data.find(sql).sort("process_time",pymongo.DESCENDING)
            main.mylock.acquire()
            var.st_imei = imei
            if rows_hd == -1:
                var.ct_svrr += 1
                var.st_lgin = "svr_err"
            elif rows_hd.count() == 0:
                var.ct_nlgin += 1
                var.st_lgin = "nolgin"
            else:
                for rows in rows_hd:
                    if rows['category'] == 'up' or rows['category'] == 'UP':
                        lgin_sign = 1
                        break
                    else:
                        lgin_sign = 0
                if lgin_sign == 0:
                    var.ct_nlgin += 1
                    var.st_lgin = "nolgin"
                else:
                    var.ct_lgin += 1
                    var.st_lgin = "login"
                    for line in rows_hd:
                        up_dn = line['category']
                        data = line['content']
                        ps_tm = line['process_time']
                        #print data
                        if up_dn == "DOWN" and len(data) > 100:
                            #解析平台下发的配置信息
                            conf_info(data,num,sht2)
                        elif data[:2] == "11":
                            #解析login包,主控和cm3版本
                            var.ct_conn += 1
                            var.st_cm33 = data[3:13]
                            var.st_mast = data[13:23]
                        elif 10 < len(data) < 35 and "~" not in data:
                            #BNDS包的处理
                            var.ct_bnds += 1
                        else:
                            dt_tp = re.search(var.re_type,data)
                            dt_tm = re.search(var.re_time,data)
                            if dt_tm is None or dt_tp is None:
                                if "~" in data:
                                    var.ct_2011 += 1
                                    if cmp(var.tmp_gps,data) == 0:
                                        var.ct_rept += 1
                                        var.tmp_gps = data
                                    #todo 2011解析  原始报文暂无法解析  pk_2011(data,num,sht2)
                            else:
                                dt_tm = dt_tm.group(1)
                                dt_tp = dt_tp.group(1)
                                
                                #数据延迟判定
                                judge_delay(data,num,sht2,dt_tm,ps_tm)
                                
                                #数据重复统计
                                repeat_statistics(data,dt_tm,dt_tp)
                                
                                #按照数据包的类型进行解析
                                if dt_tp == "1004" or dt_tp == "1002":
                                    var.ct_1004 += 1
                                    pk_1004(data,num,sht2)
                                elif dt_tp == "2001":
                                    var.ct_2001 += 1
                                    pk_2001(data,num,sht2)
                                elif dt_tp == "2011":
                                    var.ct_2011 += 1
                                elif dt_tp == "2021":
                                    var.ct_2021 += 1
                                    pk_2021(data,num,sht2)
                                elif dt_tp == "2031":
                                    var.ct_2031 += 1
                                    pk_2031(data,num,sht2)
                                elif dt_tp == "3021":
                                    var.ct_3021 += 1
                                    pk_3021(data,num,sht2)
                                elif dt_tp == "3022":
                                    var.ct_3022 += 1
                                    pk_3022(data,num,sht2)
                                elif dt_tp == "3031":
                                    var.ct_3031 += 1
                                    pk_3031(data,num,sht2)
                                elif dt_tp == "3032":
                                    var.ct_3032 += 1
                                    pk_3032(data,num,sht2)
                                elif dt_tp == "4001":
                                    if cmp(var.tmp_41,dt_tm) != 0:
                                        var.ct_4001 += 1
                                        var.tmp_41 = dt_tm
                                        pk_4001(data,num,sht2,dt_tm)
                                elif dt_tp == "4002":
                                    if cmp(var.tmp_42,dt_tm) != 0:
                                        var.ct_4002 += 1
                                        var.tmp_42 = dt_tm
                                        pk_4002(data,num,sht2,dt_tm)
                                elif dt_tp == "4011":
                                    var.ct_4011 += 1
                                    pk_4011(data,num,sht2)
                                elif dt_tp == "5001":
                                    var.ct_5001 += 1
                                    pk_5001(data,num,sht2)
                                elif dt_tp == "5005":
                                    var.ct_5005 += 1
                                    pk_5005(data,num,sht2)
                                elif dt_tp == "5006":
                                    var.ct_5006 += 1
                                    pk_5006(data,num,sht2)
                                elif dt_tp == "6001":
                                    var.ct_6001 += 1
                                    #todo 6001解析    pk_6001(data,num,sht2)
                                elif dt_tp == "9000":
                                    var.ct_9000 += 1
                                    pk_9000(data,num,sht2)
                                elif dt_tp == "9100":
                                    var.ctg_9100 += 1
                                    #9100有2种类型的包
                                    #todo 9100解析    pk_9100(data,num,sht2)
                                elif dt_tp == "9990":
                                    var.ct_9990 += 1
                                    pk_9990(data,num,sht2)
                                elif dt_tp == "9999":
                                    var.ct_9999 += 1
                                    pk_9999(data,num,sht2)
                                else:
                                    pass

        #写入数据包统计
        if var.ct_omsn > 0 and var.ct_4001 != 0:
            var.ct_omsn = 0
        dict_count = {
        var.cl_ct_1004:var.ct_1004,var.cl_ct_2001:var.ct_2001,var.cl_ct_2011:var.ct_2011,var.cl_ct_2021:var.ct_2021,var.cl_ct_2031:var.ct_2031,\
        var.cl_ct_3021:var.ct_3021,var.cl_ct_3022:var.ct_3022,var.cl_ct_3031:var.ct_3031,var.cl_ct_3032:var.ct_3032,var.cl_ct_4001:var.ct_4001,\
        var.cl_ct_4002:var.ct_4002,\
        var.cl_ct_4011:var.ct_4011,var.cl_ct_5001:var.ct_5001,var.cl_ct_5005:var.ct_5005,var.cl_ct_5006:var.ct_5006,var.cl_ct_6001:var.ct_6001,\
        var.cl_ct_9000:var.ct_9000,var.cl_ct_9100:var.ct_9100,var.cl_ct_9990:var.ct_9990,var.cl_ct_9999:var.ct_9999,var.cl_ct_dely:var.ct_dely,\
        var.cl_ct_rept:var.ct_rept,var.cl_ct_bnds:var.ct_bnds,var.cl_ct_omsn:var.ct_omsn,var.cl_ct_msjd:var.ct_msjd,var.cl_ct_vlow:var.ct_vlow,
        var.cl_ct_conn:var.ct_conn
        }
        fn.write_dict_other(sht1,num,dict_count)
        
        #写入数据包错误
        dict_error = {
        var.cl_er_1004:var.er_1004,var.cl_er_2001:var.er_2001,var.cl_er_2011:var.er_2011,var.cl_er_2021:var.er_2021,var.cl_er_2031:var.er_2031,\
        var.cl_er_3021:var.er_3021,var.cl_er_3022:var.er_3022,var.cl_er_3031:var.er_3031,var.cl_er_3032:var.er_3032,var.cl_er_4001:var.er_4001,\
        var.cl_er_4002:var.er_4002,\
        var.cl_er_4011:var.er_4011,var.cl_er_5001:var.er_5001,var.cl_er_5005:var.er_5005,var.cl_er_5006:var.er_5006,var.cl_er_6001:var.er_6001,\
        var.cl_er_9000:var.er_9000,var.cl_er_9100:var.er_9100,var.cl_er_9990:var.er_9990,var.cl_er_9999:var.er_9999,var.cl_er_time:var.er_time
        }
        fn.write_dict_other(sht1,num,dict_error)
        
        
        if len(var.dc_volt) > 500:
            var.dc_volt = {"dict":"too big."}
        #写入debug包的数据
        dict_debug = {
        var.cl_db_0:var.ct_0,      var.cl_db_1:var.ct_1,      var.cl_db_2:var.ct_2,      var.cl_db_3:var.ct_3,      var.cl_db_4:var.ct_4,      \
        var.cl_db_5:var.ct_5,      var.cl_db_6:var.ct_6,      var.cl_db_7:var.ct_7,      var.cl_db_1014:var.ct_1014,var.cl_db_9011:var.ct_9011,\
        var.cl_db_9021:var.ct_9021,var.cl_db_9031:var.ct_9031,var.cl_db_9051:var.ct_9051,var.cl_db_9052:var.ct_9052,var.cl_db_9053:var.ct_9053,\
        var.cl_db_9054:var.ct_9054,var.cl_db_9061:var.ct_9061,var.cl_db_9071:var.ct_9071,var.cl_db_9072:var.ct_9072,var.cl_db_9073:var.ct_9073,\
        var.cl_db_9074:var.ct_9074,var.cl_db_9075:var.ct_9075,var.cl_db_9075:var.ct_9075,var.cl_db_9081:var.ct_9081,var.cl_db_9082:var.ct_9082,\
        var.cl_db_9100:var.ctg_9100,var.cl_db_9101:var.ct_9101,var.cl_db_9102:var.ct_9102,var.cl_db_9103:var.ct_9103,var.cl_db_9109:var.ct_9109,\
        var.cl_db_9301:var.ct_9301,var.cl_db_9303:var.ct_9303,var.cl_db_9304:var.ct_9304,var.cl_db_9305:var.ct_9305,var.cl_db_9306:var.ct_9306,\
        var.cl_db_9307:var.ct_9307,var.cl_db_9308:var.ct_9308,var.cl_db_9309:var.ct_9309,var.cl_db_9310:var.ct_9310,var.cl_db_9331:var.ct_9331,\
        var.cl_db_9332:var.ct_9332,var.cl_db_9333:var.ct_9333,var.cl_db_9401:var.ct_9401,var.cl_db_9993:var.ct_9993,var.cl_db_9994:var.ct_9994,\
        var.cl_db_9995:var.ct_9995,var.cl_dt_volt:str(var.dc_volt)
        }
        fn.write_dict_other(sht1,num,dict_debug)
        
        #写入下发的配置信息
        dict_conf = {
        var.cl_fbox:var.st_fbox,var.cl_amvl:var.st_amvl,var.cl_shak:var.st_shak,var.cl_agps:var.st_agps,var.cl_coll:var.st_coll,\
        var.cl_imsi:var.st_imsi,var.cl_ccid:var.st_ccid,var.cl_numb:var.st_numb
        }
        fn.write_dict_data(sht1,num,dict_conf)
        
        #写入测试debug
        dict_test = {
        var.cl_db_3001:var.ct_3001,var.cl_db_3002:var.ct_3002,var.cl_db_3003:var.ct_3003,var.cl_db_3004:var.ct_3004,var.cl_db_3005:var.ct_3005,\
        var.cl_db_3006:var.ct_3006,var.cl_db_3007:var.ct_3007,var.cl_db_3008:var.ct_3008,var.cl_db_3009:var.ct_3009,var.cl_db_3010:var.ct_3010,\
        var.cl_db_3011:var.ct_3011,var.cl_db_3012:var.ct_3012,var.cl_db_3013:var.ct_3013,var.cl_db_3014:var.ct_3014,var.cl_db_3015:var.ct_3015
        }
        fn.write_dict_other(sht1,num,dict_test)

        #基本信息
        base_info()
        dict_base = {
        var.cl_imei:var.st_imei,var.cl_lgin:var.st_lgin,var.cl_dscn:var.dc_dscn,var.cl_dlay:str([(k,var.dc_dlay[k]) for k in sorted(var.dc_dlay.keys())]),var.cl_mast:var.st_mast,var.cl_cm33:var.st_cm33,\
        var.cl_vinn:var.st_vinn
        }        
        fn.write_dict_data(sht1,num,dict_base)
        
        variable()
        main.mylock.release()
    except Exception,ex:
        print "datahd:",Exception,":",ex
        #基本信息
        base_info()
        dict_base = {
        var.cl_imei:var.st_imei,var.cl_lgin:var.st_lgin,var.cl_dscn:var.dc_dscn,var.cl_dlay:str([(k,var.dc_dlay[k]) for k in sorted(var.dc_dlay.keys())]),var.cl_mast:var.st_mast,var.cl_cm33:var.st_cm33,\
        var.cl_vinn:var.st_vinn
        }        
        fn.write_dict_data(sht1,num,dict_base)
        main.mylock.release()
        


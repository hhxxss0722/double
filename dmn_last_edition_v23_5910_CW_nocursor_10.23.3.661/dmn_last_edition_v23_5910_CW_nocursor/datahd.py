#-*- coding:utf-8 -*-
from filehandling import fn
import datetime
from variable import var
from variable import gps
import re
from database.mongo import pyMongo
from database.mysql import pyMysql
import sys
import main
import pymongo
import time
if var.ctrl_sign != 'JG':
    from database.hadoop import pySpark

def datahd(conn_hd,cursor_obd,sht1,sht2,row_imei,num):
    try:
        if var.model_sign == 0 or var.model_sign == 1:
            # 解析row_imei
            tid,imei,imsi,hw_vs,sw_vs,group,supplier,network,bind_time,domain,\
            licence_plate,vin,style_name,model_name,apploginrecord,mobile,latest_login,first_login = obd_version(row_imei)            
        else:
            tid,imei,imsi,hw_vs,sw_vs,group,supplier,network,bind_time,domain,\
            licence_plate,vin,style_name,model_name,apploginrecord,mobile,latest_login,first_login = obd_version1(cursor_obd,row_imei)
            
        print imei,num,var.len_imei,var.dt,datetime.datetime.now()


        if tid == "null" or imei == "null" or tid == "except" or imei == "except":
            print "tid or imei == 'null',it's pass. row_imei:",row_imei
            fn.write_single_data(sht1,num,var.col_imei,imei)
        else:
            fn.write_single_data(sht2,num,0,imei)
            if var.ctrl_sign == 'JG':
                rows_hd = pyMongo.mongoGetMessage1(cursor_mg,{'imei':imei,'process_time':{'$regex':var.dt}}).sort("process_time",pymongo.ASCENDING) 
                main.mylock1.acquire()
                if rows_hd == -1:
                    var.server_error += 1
                    # 写数据
                    fn.write_single_data(sht1,num,var.col_login,'server_error')
                    print "mongoGetMessage except,it's pass"
                elif rows_hd.count() == 0:
                    var.nologin_imei += 1
                    # 写数据
                    fn.write_single_data(sht1,num,var.col_login,'nolgin')
                else:
                    lgin_sign = 0
                    for line in rows_hd:
                        up_dowm = line['category']
                        data = line['content']
                        ps_time = line['process_time']
                        #print data
                        if up_dowm == 'DOWN' and len(data) > 100:
                            # 解析平台的配置信息
                            conf(data,num,sht1)
                        elif data == '':
                            pass
                            # 空数据
                        elif 10 < len(data) < 15:
                            # BNDS包的处理
                            var.ct_bnds += 1
                        else:
                            if up_dowm == 'UP':
                                lgin_sign += 1                            
                            datatype = re.search(var.re_type,data)
                            datatime = re.search(var.re_time,data)
                            if datatime is None or datatype is None:
                                pass
                            else:
                                datatime = datatime.group(1)
                                datatype = datatype.group(1)
                                # 是否存在数据延迟的判断处理
                                judge_datatime(data,num,sht2,datatime,ps_time)
                                # 上报的数据包是否相同的统计
                                duplicate(data,datatime,datatype)
                                # 按照数据包的类型进行解析
                                if datatype == '1004' or datatype == '1002':
                                    var.ct_1004 += 1
                                    pk_1004(data,num,sht2)
                                elif datatype == '2001':
                                    var.ct_2001 += 1
                                    pk_2001(data,num,sht2)
                                elif datatype == '2011':
                                    var.ct_2011 += 1
                                    pk_2011(data,num,sht2)
                                elif datatype == '2021':
                                    var.ct_2021 += 1
                                    pk_2021(data,num,sht2)
                                elif datatype == '2031':
                                    var.ct_2031 += 1
                                    pk_2031(data,num,sht2)
                                elif datatype == '3021':
                                    var.ct_3021 += 1
                                    pk_3021(data,num,sht2)
                                elif datatype == '3031':
                                    var.ct_3031 += 1
                                    pk_3031(data,num,sht2)
                                elif datatype == '3032':
                                    var.ct_3032 += 1
                                    pk_3032(data,num,sht2)
                                elif datatype == '4001':
                                    # ct_4001 需判断包是否重复
                                    pk_4001(data,num,sht2,datatime)
                                elif datatype == '4002':
                                    # ct_4002 需判断包是否重复
                                    pk_4002(data,num,sht2,datatime)
                                elif datatype == '4011':
                                    var.ct_4011 += 1
                                    pk_4011(data,num,sht2)
                                elif datatype == '5001':
                                    var.ct_5001 += 1
                                    pk_5001(data,num,sht2)
                                elif datatype == '5005':
                                    var.ct_5005 += 1
                                    pk_5005(data,num,sht2)
                                elif datatype == '5006':
                                    var.ct_5006 += 1
                                    pk_5006(data,num,sht2)
                                elif datatype == '6001':
                                    var.ct_6001 += 1
                                    pk_6001(data,num,sht2)
                                elif datatype == '9000':
                                    var.ct_9000 += 1
                                    pk_9000(data,num,sht2)
                                elif datatype == '9100':
                                    var.ctg_9100 += 1
                                    # 9100有2种类型的包，需分开解析，待续.
                                    #pk_9100(data,num,sht2)
                                elif datatype == '9990':
                                    var.ct_9990 += 1
                                    pk_9990(data,num,sht2)
                                elif datatype == '9999':
                                    var.ct_9999 += 1
                                    pk_9999(data,num,sht2)
                                else:
                                    pass
                    if lgin_sign == 0:
                        var.nologin_imei += 1
                        # 写数据
                        fn.write_single_data(sht1,num,var.col_login,'nolgin')
                    else:
                        var.login_imei += 1
                        # 写数据包
                        fn.write_single_data(sht1,num,var.col_login,'login')
                
            else:
                sql_hd = var.sql_hd1 + var.dt + var.sql_hd2 + imei + var.sql_hd3
                rows_hd = pySpark.impylaGetMessage(conn_hd,sql_hd)
                
                main.mylock1.acquire()
                if rows_hd == -1:
                    var.server_error += 1
                    # 写数据
                    fn.write_single_data(sht1,num,var.col_login,'server_error')
                    print "hadoopGetMessage except,it's pass"
                elif rows_hd == []:
                    var.nologin_imei += 1
                    # 写数据
                    fn.write_single_data(sht1,num,var.col_login,'nolgin')
                else:
                    for rows in rows_hd:
                        if "UP" in rows:
                            lgin_sign = 1
                            break
                        else:
                            lgin_sign = 0
                    if lgin_sign == 0:
                        var.nologin_imei += 1
                        # 写数据
                        fn.write_single_data(sht1,num,var.col_login,'nolgin')
                    else:
                        var.login_imei += 1
                        for line in xrange(len(rows_hd)):
                            #print line,len(rows_hd),rows_hd[line]
                            up_dowm = rows_hd[line][0]
                            data = rows_hd[line][1]
                            ps_time = rows_hd[line][2]
                            #print data
                            if up_dowm == 'DOWN' and len(data) > 100:
                                # 解析平台的配置信息
                                conf(data,num,sht1)
                            elif data == '':
                                pass
                                # 空数据
                            elif 10 < len(data) < 35:
                            #elif len(data) == 23:
                                # BNDS包的处理
                                #print 'len(data):',len(data)
                                var.ct_bnds += 1
                            else:
                                
                                datatype = re.search(var.re_type,data)
                                datatime = re.search(var.re_time,data)
                                if datatime is None or datatype is None:
                                    pass
                                else:
                                    
                                    datatime = datatime.group(1)
                                    datatype = datatype.group(1)
                                    # 是否存在数据延迟的判断处理
                                    judge_datatime(data,num,sht2,datatime,ps_time)
                                    # 上报的数据包是否相同的统计
                                    duplicate(data,datatime,datatype)
                                    # 按照数据包的类型进行解析
                                    if datatype == '1004' or datatype == '1002':
                                        var.ct_1004 += 1
                                        pk_1004(data,num,sht2)
                                    elif datatype == '2001':
                                        var.ct_2001 += 1
                                        pk_2001(data,num,sht2)
                                    elif datatype == '2011':
                                        var.ct_2011 += 1
                                        pk_2011(data,num,sht2)
                                    elif datatype == '2021':
                                        var.ct_2021 += 1
                                        pk_2021(data,num,sht2)
                                    elif datatype == '2031':
                                        var.ct_2031 += 1
                                        pk_2031(data,num,sht2)
                                    elif datatype == '3021':
                                        var.ct_3021 += 1
                                        pk_3021(data,num,sht2)
                                    elif datatype == '3031':
                                        var.ct_3031 += 1
                                        pk_3031(data,num,sht2)
                                    elif datatype == '3032':
                                        var.ct_3032 += 1
                                        pk_3032(data,num,sht2)
                                    elif datatype == '4001':
                                        # ct_4001 需判断包是否重复
                                        pk_4001(data,num,sht2,datatime)
                                    elif datatype == '4002':
                                        # ct_4002 需判断包是否重复
                                        pk_4002(data,num,sht2,datatime)
                                    elif datatype == '4011':
                                        var.ct_4011 += 1
                                        pk_4011(data,num,sht2)
                                    elif datatype == '5001':
                                        var.ct_5001 += 1
                                        pk_5001(data,num,sht2)
                                    elif datatype == '5005':
                                        var.ct_5005 += 1
                                        pk_5005(data,num,sht2)
                                    elif datatype == '5006':
                                        var.ct_5006 += 1
                                        pk_5006(data,num,sht2)
                                    elif datatype == '6001':
                                        var.ct_6001 += 1
                                        pk_6001(data,num,sht2)
                                    elif datatype == '9000':
                                        var.ct_9000 += 1
                                        pk_9000(data,num,sht2)
                                    elif datatype == '9100':
                                        var.ctg_9100 += 1
                                        # 9100有2种类型的包，需分开解析，待续.
                                        #pk_9100(data,num,sht2)
                                    elif datatype == '9990':
                                        var.ct_9990 += 1
                                        pk_9990(data,num,sht2)
                                    elif datatype == '9999':
                                        var.ct_9999 += 1
                                        pk_9999(data,num,sht2)
                                    else:
                                        pass
                        # 写数据包
                        fn.write_single_data(sht1,num,var.col_login,'login')
            '''
            if tid == "null" or imei == "null" or tid == "except" or imei == "except":
                pass
            else:
                # 数据库查询车辆信息
                model_name,style_name,vin,licence_plate = cartypes(cursor_obd,imei,tid)
                
                # 用户手机号码
                mobile = customermoble(cursor_obd,tid)
            '''
            #对应var dict1的参数
            
            # 将设备信息及车辆信息写入到xls中
            dict_obd = {
            var.col_imei:imei,var.col_type:supplier,var.col_imsi:imsi,var.col_hardware:hw_vs,var.col_software:sw_vs,var.col_group:group,\
            var.col_network:network,var.col_domain:domain,var.col_licence_plate:licence_plate,var.col_vin:vin,var.col_tid:tid,\
            var.col_style:style_name,var.col_model:model_name,var.col_applogin:str(apploginrecord),var.col_phone:mobile,\
            var.col_date:str(latest_login),var.col_runtime:str(first_login)}
            fn.write_dict_data(sht1,num,dict_obd)
            
            # 2001包内数据的判断
            if var.ct_2001 > 5:
                judge_2001(sht1,num)

            # 4001包内vin的判断
            if var.ct_vin > 0:
                fn.write_single_data(sht1,num,var.col_carvin,'支持')
                fn.write_single_data(sht1,num,var.col_vin_value,var.vin_value)
            elif var.ct_vin == 0 and var.ct_4001 > 1 and (var.ct_4001-var.sign_rst) > 0:
                fn.write_single_data(sht1,num,var.col_carvin,'不支持')
                fn.write_single_data(sht1,num,var.col_vin_value,'null')
            elif var.ct_vin == 0 and var.ct_4001 == 1:
                fn.write_single_data(sht1,num,var.col_carvin,'待定')
                fn.write_single_data(sht1,num,var.col_vin_value,'点火1次')
            else:
                fn.write_single_data(sht1,num,var.col_carvin,'待定')
                fn.write_single_data(sht1,num,var.col_vin_value,'未点火')
            '''
            # 最近APP登录时间
            apploginrecord = applogin(cursor_obd,imei)
            fn.write_single_data(sht1,num,var.col_applogin,str(apploginrecord))
            
            # 数据库查询起始时间
            login_rows = pyMongo.mongoGetMessage(cursor_mg,{'tid':int(tid)}).sort([('Time', pymongo.DESCENDING)])
            if login_rows != -1:
                login_len = login_rows.count()
                if login_len == 0:
                    fn.write_single_data(sht1,num,var.col_date,'no record')
                else:
                    # 设备起始时间、当前在线状态的判断
                    if login_rows[0]['type'] == 1:
                        fn.write_single_data(sht1,num,var.col_date,str(login_rows[0]['Time'] + datetime.timedelta(hours = 8))+ ' - ' + str(login_rows[login_len-1]['Time'] + datetime.timedelta(hours = 8)) + ' :登出' + '\n')
                    elif login_rows[0]['type'] == 0:
                        fn.write_single_data(sht1,num,var.col_date,str(login_rows[0]['Time'] + datetime.timedelta(hours = 8))+ ' - ' + str(login_rows[login_len-1]['Time'] + datetime.timedelta(hours = 8)) + ' :登录' + '\n')
                    else:
                        fn.write_single_data(sht1,num,var.col_date,str(login_rows[0]['Time'] + datetime.timedelta(hours = 8))+ ' - ' + str(login_rows[login_len-1]['Time'] + datetime.timedelta(hours = 8)) + ' :错误' + '\n')
                    
                    # 统计设备运行时长
                    if bind_time == "null" or bind_time == "except":
                        #fn.write_single_data(sht1,num,var.col_runtime,str(login_rows[0]['Time']-login_rows[login_len-1]['Time']) + ':NoBind')
                        fn.write_single_data(sht1,num,var.col_runtime,(login_rows[0]['Time']-login_rows[login_len-1]['Time']).days)
                    else:
                        #fn.write_single_data(sht1,num,var.col_runtime,str((login_rows[0]['Time'] + datetime.timedelta(hours = 8)) - bind_time) + ':YsBind')
                        fn.write_single_data(sht1,num,var.col_runtime,((login_rows[0]['Time'] + datetime.timedelta(hours = 8)) - bind_time).days)

                    # 统计用户最近登录时间与设备最近登录登出的情况
                    if apploginrecord == "None" or apploginrecord == "No_Record":
                        pass
                    else:
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
            else:
                fn.write_single_data(sht1,num,var.col_date,'server_error')
            '''
            # 掉电时间处理
            if var.dt_discon != []:
                if len(var.dt_discon) < 100:
                    fn.write_single_data(sht1,num,var.col_discon,str(sorted(var.dt_discon)))
                else:
                    fn.write_single_data(sht1,num,var.col_discon,'too big.')
            
            # 两点距离大于3km的处理
            if var.ct_distance > 0 and var.ct_4001 > 0:
                fn.write_single_data(sht1,num,var.col_distance,var.ct_distance)
            
            '''  对应var dict2的参数  '''
            
            # 各数据包数量
            dict_count = {
            var.col_count_1004:var.ct_1004,var.col_count_2001:var.ct_2001,var.col_count_2011:var.ct_2011,\
            var.col_count_2021:var.ct_2021,var.col_count_2031:var.ct_2031,var.col_count_3021:var.ct_3021,\
            var.col_count_3031:var.ct_3031,var.col_count_3032:var.ct_3032,\
            var.col_count_4001:var.ct_4001,var.col_count_4002:var.ct_4002,\
            var.col_count_4011:var.ct_4011,var.col_count_5001:var.ct_5001,var.col_count_5005:var.ct_5005,\
            var.col_count_5006:var.ct_5006,var.col_count_6001:var.ct_6001,var.col_count_9000:var.ct_9000,\
            var.col_count_9100:var.ct_9100,var.col_count_9990:var.ct_9990,var.col_count_9999:var.ct_9999
            }
            fn.write_dict_other(sht1,num,dict_count)

            '''
            #对应var dict3的参数
            if var.ctrl_sign != 'JG':
                # 设备的重启判断
                tcm_upgrade(cursor_tcm,imei)
                if var.sign_rst > 0:
                    fn.write_single_data(sht1,num,var.col_count_reset,var.sign_rst)
                else:
                    pass
                # 设备所属批次
                fn.write_single_data(sht1,num,var.col_batch,product_batch(cursor_tcm,imei))
            else:
                pass
            '''
            # 漏报4001的判断
            if var.sign_2011 > 0 or var.sign_2021 > 0:
                if var.ct_4001 == 0 and var.ct_4002 == 0:
                    var.miss_4001 = var.sign_2011 + var.sign_2021

            dict_other = {
            var.col_count_vlow:var.ct_vlow,var.col_count_lgin:var.count_fbox,var.col_duplicate:var.count_duplicate,\
            var.col_bnds:var.ct_bnds,var.col_count_miss4001:var.miss_4001,var.col_count_error4002:var.sign_4002,\
            var.col_count_updelay:var.sign_delay
            }
            fn.write_dict_other(sht1,num,dict_other)

            '''  对应var dict4的参数  '''

            # 各数据包错误
            dict_error = {
            var.col_er_rate2001:var.er_rate2001,\
            var.col_form1004:var.er_1004,var.col_form2001:var.er_2001,var.col_form2011:var.er_2011,\
            var.col_form2021:var.er_2021,var.col_form2031:var.er_2031,var.col_form3021:var.er_3021,\
            var.col_form3031:var.er_3031,var.col_form3032:var.er_3032,\
            var.col_form4001:var.er_4001,var.col_form4002:var.er_4002,\
            var.col_form4011:var.er_4011,var.col_form5001:var.er_5001,var.col_form5005:var.er_5005,\
            var.col_form5006:var.er_5006,var.col_form6001:var.er_6001,var.col_form9000:var.er_9000,\
            var.col_form9100:var.er_9100,var.col_form9990:var.er_9990,var.col_form9999:var.er_9999,\
            var.col_formtime:var.formtime,var.col_timeerror:var.timeerror,}
            fn.write_dict_other(sht1,num,dict_error)
            
            
            '''  对应var dict5的参数  '''
            
            # 写入debug包的数据
            dict_debug = {
            var.col_debug_0:var.ct_0,var.col_debug_1:var.ct_1,var.col_debug_2:var.ct_2,\
            var.col_debug_3:var.ct_3,var.col_debug_4:var.ct_4,var.col_debug_5:var.ct_5,var.col_debug_6:var.ct_6,\
            var.col_debug_7:var.ct_7,var.col_debug_9011:var.ct_9011,var.col_debug_9021:var.ct_9021,\
            var.col_debug_9031:var.ct_9031,var.col_debug_9041:var.ct_9041,var.col_debug_9051:var.ct_9051,\
            var.col_debug_9052:var.ct_9052,var.col_debug_9053:var.ct_9053,var.col_debug_9054:var.ct_9054,\
            var.col_debug_9061:var.ct_9061,var.col_debug_9062:var.ct_9062,var.col_debug_9063:var.ct_9063,\
            var.col_debug_9064:var.ct_9064,var.col_debug_9065:var.ct_9065,var.col_debug_9066:var.ct_9066,\
            var.col_debug_9067:var.ct_9067,var.col_debug_9068:var.ct_9068,var.col_debug_9069:var.ct_9069,\
            var.col_debug_9071:var.ct_9071,var.col_debug_9072:var.ct_9072,var.col_debug_9073:var.ct_9073,\
            var.col_debug_9074:var.ct_9074,var.col_debug_9075:var.ct_9075,var.col_debug_9075:var.ct_9075,\
            var.col_debug_9081:var.ct_9081,var.col_debug_9082:var.ct_9082,\
            var.col_debug_9100:var.ctg_9100,var.col_debug_9101:var.ct_9101,var.col_debug_9102:var.ct_9102,\
            var.col_debug_9103:var.ct_9103,var.col_debug_9109:var.ct_9109,var.col_debug_9301:var.ct_9301,\
            var.col_debug_9302:var.ct_9302,\
            var.col_debug_9303:var.ct_9303,var.col_debug_9304:var.ct_9304,var.col_debug_9305:var.ct_9305,\
            var.col_debug_9306:var.ct_9306,var.col_debug_9307:var.ct_9307,var.col_debug_9308:var.ct_9308,\
            var.col_debug_9309:var.ct_9309,\
            var.col_debug_9310:var.ct_9310,var.col_debug_9331:var.ct_9331,var.col_debug_9332:var.ct_9332,\
            var.col_debug_9401:var.ct_9401,\
            var.col_debug_9991:var.ct_9991,var.col_debug_9992:var.ct_9992,\
            var.col_debug_9993:var.ct_9993,var.col_debug_9994:var.ct_9994,var.col_debug_9995:var.ct_9995
            }
            fn.write_dict_other(sht1,num,dict_debug)
            '''
            # 所有数据包内的电压数据
            if len(var.dt_volt) < 500:
                fn.write_single_data(sht1,num,var.col_volt_time,str([(k,var.dt_volt[k]) for k in sorted(var.dt_volt.keys())]))
            else:
                fn.write_single_data(sht1,num,var.col_volt_time,'dict is too big!')
            '''
            
            '''
            对应dict6
            '''
            
            # 诊断数据
            if var.ct_6001 == 0:
                pass
            elif var.dgtg_ys >0 or var.dgtg_no > 0 or var.dgtg_ag > 0:
                fn.write_single_data(sht1,num,var.col_dgtg,'全车诊断:发起' + str(var.dgtg_ys + var.dgtg_no) + '次;' + \
                '205包数量:' + str(var.dgtg_ag) +';' + \
                '不对称' + str(var.dgtg_ys - var.dgtg_ab - var.dgtg_ac - var.dgtg_ae - var.dgtg_af) + '次;' + '满足条件:' + \
                str(var.dgtg_ys) + ';' + '不满足条件:' + str(var.dgtg_no) + ';' + '完成:' + str(var.dgtg_ae) + \
                '诊断时行驶:' + str(var.dgtg_ab) + ';' + '诊断时熄火:' + str(var.dgtg_ac) +';' + \
                '其他异常:' + str(var.dgtg_af) + ';' + \
                '全车诊断:' +str(var.dgtg_list) + ';' + '实时诊断:' + str(var.dgak_list))
            else:
                fn.write_single_data(sht1,num,var.col_dgtg,'全车诊断:没有发起' + ';' + '实时诊断:' + str(var.dgak_list))
            # 百公里加速
            if var.tacc_ys > 0 or var.tacc_no > 0 or var.tacc_ab > 0:
                fn.write_single_data(sht1,num,var.col_tacc,'准备就绪:' + str(var.tacc_ys) + ';' + '未定位:' + \
                str(var.tacc_no) + ';' + '行驶or熄火:' + str(var.tacc_ab) + ';' + '完成:' + str(var.tacc_ac) + \
                ';' + '测试中定位失败:' + str(var.tacc_ad) + ';' + '超时:' + str(var.tacc_ae))
            
            
            # 重置所有临时参数
            parameter_init()
            
            main.mylock1.release()  
    except Exception,ex:
        print Exception,":",ex
        print 'datahandling is except.'
        main.mylock1.release()



def parameter_init():
    '''
    对应dict2的参数
    '''
    #上行数据包的统计
    var.ct_1004,var.ct_2001,var.ct_2011,var.ct_2021,var.ct_2031,var.ct_3021,var.ct_3031,var.ct_3032,\
    var.ct_4001,\
    var.ct_4002,var.ct_4011,var.ct_5001,var.ct_5005,var.ct_5006,var.ct_6001,var.ct_9000,var.ct_9100,\
    var.ct_9990,var.ct_9999 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

    '''
    对应dict3的参数
    '''
    var.ct_vlow,var.count_fbox,var.count_in,var.count_out,\
    var.count_duplicate,var.ct_bnds,var.sign_2011,var.sign_2021,\
    var.miss_4001,var.sign_4002,var.sign_delay,var.sign_rst = 0,0,0,0,0,0,0,0,0,0,0,0

    '''
    对应dict4的参数
    '''
    # 数据包格式错误的统计
    var.er_rate2001,\
    var.er_1004,var.er_2001,var.er_2011,var.er_2021,var.er_2031,var.er_3021,var.er_3031,var.er_3032,\
    var.er_4001,\
    var.er_4002,var.er_4011,var.er_5001,var.er_5005,var.er_5006,var.er_6001,var.er_9000,var.er_9100,\
    var.er_9990,var.er_9999,var.formtime,var.timeerror = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

    '''
    对应dict5的参数
    '''
    #debug包的统计
    var.ct_0,var.ct_1,var.ct_2,var.ct_3,var.ct_4,var.ct_5,var.ct_6,var.ct_7,var.ct_9011,var.ct_9021,\
    var.ct_9031,var.ct_9041,var.ct_9051,var.ct_9052,var.ct_9053,var.ct_9054,var.ct_9061,var.ct_9062,\
    var.ct_9063,var.ct_9064,var.ct_9065,var.ct_9066,var.ct_9067,var.ct_9067,var.ct_9068,var.ct_9069,\
    var.ct_9071,var.ct_9072,var.ct_9073,var.ct_9074,var.ct_9075,var.ct_9076,var.ct_9081,var.ct_9082,\
    var.ctg_9100,var.ct_9101,var.ct_9102,var.ct_9103,var.ct_9109,\
    var.ct_9301,var.ct_9302,var.ct_9303,var.ct_9304,var.ct_9305,var.ct_9306,\
    var.ct_9307,var.ct_9308,var.ct_9309,var.ct_9310,var.ct_9331,var.ct_9332,var.ct_9401,\
    var.ct_9991,var.ct_9992,var.ct_9993,var.ct_9994,var.ct_9995 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

    '''
    2001包解析的参数
    '''
    #用于里程分析的参数
    var.mileage_no,var.mileage_yes,var.mileage_ab,var.mileage_init = 0,0,0,0
    #用于油量分析的参数
    var.oil_no,var.oil_yes,var.oil_ab = 0,0,0
    #用于转速分析的参数
    var.enginespeed_yes,var.enginespeed_ab,var.enginespeed_no = 0,0,0
    #用于车速分析的参数
    var.speed_no,var.speed_yes,var.speed_ab = 0,0,0

    '''
    temp_time,temp_type : 是否相同的临时参数
    temp_4001,temp_4002 ：4001，4002是否重复的临时参数
    lac_value ：2021包中lac是否变化的临时参数
    '''
    var.temp_time,var.temp_type,var.temp_4001,var.temp_4002,var.lac_value= '','','','',0

    #数据包格式错误的列控制参数
    var.sht2_colx = 1

    #所有数据包内电压的统计
    var.dt_volt,var.dt_discon = {},[]

    #vin的参数
    var.ct_vin,var.vin_value = 0,''
    
    #2001包时间间隔
    var.temp_2001,var.rate1_2001,var.rate2_2001,var.rate3_2001,var.rate4_2001,rate_sign = '',0,0,0,0,0

    # gps.py 计算GPS距离的参数
    var.f1,var.f2,var.ct_distance = 0,0,0

    # 6001包的解析参数
    var.data_6001,var.dgak_list,var.dgtg_list,var.dgtg_ys,var.dgtg_no,var.dgtg_ab,var.dgtg_ac,var.dgtg_ae,var.dgtg_af,var.dgtg_ag = '',[],[],0,0,0,0,0,0,0
    
    # 9100包的解析参数
    var.data_9100,var.tacc_ys,var.tacc_no,var.tacc_ab,var.tacc_ac,var.tacc_ad,var.tacc_ae = '',0,0,0,0,0,0
    
    # 记录自动下发短信的imei号
    var.imei_list = []
    

# 配置信息解析
def conf(data,num,sht1):
    var.count_fbox += 1
    conf = re.search(var.re_conf,data)
    if conf is not None:
        fbox = conf.group(1)
        alarmvolt = conf.group(2)
        shakevalue = conf.group(3)
        accgps = conf.group(4)
        collision = conf.group(6)
        if var.count_fbox == 1:
            fn.write_single_data(sht1,num,var.col_fbox,fbox)
            fn.write_single_data(sht1,num,var.col_alarmvolt,alarmvolt)
            fn.write_single_data(sht1,num,var.col_shakevalue,shakevalue)
            fn.write_single_data(sht1,num,var.col_accgps,accgps)
            fn.write_single_data(sht1,num,var.col_collision,collision)
        else:
            pass
    else:
        pass

# 包内时间格式判断，延迟判断
def judge_datatime(data,num,sht2,datatime,data_process_time):
    if datatime[:10] != '0000-00-00':
        try:
            #print datatime,data_process_time
            dt1 = datetime.datetime.strptime(datatime, '%Y-%m-%d %H:%M:%S')
            dp1 = datetime.datetime.strptime(data_process_time, '%Y%m%d %H:%M:%S')
            dt_day = (dp1 - dt1).seconds
            
            if dt_day > 10800:
                var.sign_delay  += 1
            
            '''
            dt_day = (dp1 - dt1).days
            if var.value_delay_max > dt_day > var.value_delay_min:
                var.sign_delay  += 1
                #print var.sign_delay
            elif dt_day > 360 or dt_day < -(var.value_delay_max):
                var.timeerror += 1
                if var.sht2_colx < var.value_sht2_err:
                    fn.write_single_data(sht2,num,var.sht2_colx,data)
                    var.sht2_colx += 1                
            else:
                pass
            '''
        except:
            var.formtime += 1
            if var.sht2_colx < var.value_sht2_err:
                fn.write_single_data(sht2,num,var.sht2_colx,data)
                var.sht2_colx += 1

    else:
        pass
   
# 数据包重复的判断
def duplicate(data,datatime,datatype):
    if cmp(var.temp_time,datatime) == 0 and cmp(var.temp_type,datatype) == 0:
        var.count_duplicate += 1
        var.temp_time = datatime
        var.temp_type = datatype
    else:
        var.temp_time = datatime
        var.temp_type = datatype

# 解析row_imei   
def obd_version(row_imei):
    try:
        t_id = str(row_imei[0])
        imei = row_imei[1]
        #print imei,imei[:5],"imei"
        if imei[:2] == "86":
            imsi = row_imei[2]
            hw_vs = row_imei[3]
            sw_vs = row_imei[4]
            group = row_imei[5]
            supplier = row_imei[6]
            network = row_imei[7]
            bind_time = row_imei[8]
            domain = row_imei[9]
            licence_plate = row_imei[10]
            vin = row_imei[11]
            style_name = row_imei[12]
            model_name = row_imei[13]
            apploginrecord = row_imei[14]
            mobile = row_imei[15]
            latest_login = row_imei[16]
            first_login = row_imei[17]
            if imsi == None:
                imsi = "null"
            if hw_vs == None:
                hw_vs = "null"
            if sw_vs == None:
                sw_vs= "null"
            if group == None:
                group = "null"
            if network == None:
                network = "null"
            if bind_time == None:
                bind_time = "null"
            if domain == None:
                domain = "null"
            if licence_plate == None:
                licence_plate = "null"
            if vin == None:
                vin = "null"
            if style_name == None:
                style_name = "null"
            if model_name == None:
                model_name = "null"
            if apploginrecord == None:
                apploginrecord = "null"
            if mobile == None:
                mobile = "null"
            if latest_login == None:
                latest_login = "null"
            if first_login == None:
                first_login = "null"
            
            
            return t_id,imei,imsi,hw_vs,sw_vs,group,supplier,network,bind_time,domain,licence_plate,vin,style_name,model_name,apploginrecord,mobile,latest_login,first_login
        else:
            return "null",imei,"null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null"
    except Exception,ex:
        print Exception,":",ex
        print "obd_version except.",row_imei
        return "except","except","except","except","except","except","except","except","except","except","except","except","except","except","except","except","except","except"

def obd_version1(cursor_obd,imei):
    try:
        #time.sleep(0.1)

        cursor_obd.execute(var.sql_obdversion + imei)
        
        row_imei = cursor_obd.fetchall() 
        #print row_imei
        t_id = str(row_imei[0][0])
        imei = row_imei[0][1]
        imsi = row_imei[0][2]
        hw_vs = row_imei[0][3]
        sw_vs = row_imei[0][4]
        group = row_imei[0][5]
        supplier = row_imei[0][6]
        network = row_imei[0][7]
        bind_time = row_imei[0][8]
        domain = row_imei[0][9]
        licence_plate = row_imei[0][10]
        vin = row_imei[0][11]
        style_name = row_imei[0][12]
        model_name = row_imei[0][13]
        apploginrecord = row_imei[0][14]
        mobile = row_imei[0][15]
        latest_login = row_imei[0][16]
        first_login = row_imei[0][17]
        if imsi == None:
            imsi = "null"
        if hw_vs == None:
            hw_vs = "null"
        if sw_vs == None:
            sw_vs= "null"
        if group == None:
            group = "null"
        if network == None:
            network = "null"
        if bind_time == None:
            bind_time = "null"        
        if domain == None:
            domain = "null"
        if licence_plate == None:
            licence_plate = "null"
        if vin == None:
            vin = "null"
        if style_name == None:
            style_name = "null"
        if model_name == None:
            model_name = "null"
        if apploginrecord == None:
            apploginrecord = "null"
        if mobile == None:
            mobile = "null"
        if latest_login == None:
            latest_login = "null"
        if first_login == None:
            first_login = "null"
        
        
        return t_id,imei,imsi,hw_vs,sw_vs,group,supplier,network,bind_time,domain,licence_plate,vin,style_name,model_name,apploginrecord,mobile,latest_login,first_login
    except Exception,ex:
        print Exception,":",ex
        print "obd_version1 except.",imei
        return "except","except","except","except","except","except","except","except","except","except","except","except","except","except","except","except","except","except"

# 1004包的处理
def pk_1004(data,num,sht2):
    pk_1004 = re.search(var.re_1004,data)
    if pk_1004 is not None:
        volt_1004 = float(pk_1004.group(7))
        # 增加到dt_volt,用于观察电压曲线
        var.dt_volt[pk_1004.group(2)] = volt_1004

        if volt_1004 < var.value_volt_low:
            var.ct_vlow += 1

    else:
        var.er_1004 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1

# 2001包的处理
def pk_2001(data,num,sht2):
    pk_2001 = re.search(var.re_2001,data)
    if pk_2001 is not None:
        time_2001 = pk_2001.group(1)
        mileage = int(pk_2001.group(2))
        oil = pk_2001.group(6)
        volt_2001 = float(pk_2001.group(8))
        enginespeed = int(pk_2001.group(9))
        speed = pk_2001.group(11)
        #2001包时间间隔的判断
        if var.rate_sign == 1:
            if var.temp_2001 == '':
                var.temp_2001 = time_2001
            elif var.temp_2001 == time_2001:
                pass
            else:
                dt1 = datetime.datetime.strptime(time_2001,'%Y-%m-%d %H:%M:%S')
                tp1 = datetime.datetime.strptime(var.temp_2001,'%Y-%m-%d %H:%M:%S')
                if 27 <(dt1-tp1).seconds < 33:
                    var.rate1_2001 += 1
                    var.temp_2001 = time_2001
                elif 290 <(dt1-tp1).seconds < 310:
                    var.rate2_2001 += 1
                    var.temp_2001 = time_2001
                elif 0 <(dt1-tp1).seconds < 310:
                    var.rate4_2001 += 1
                    var.temp_2001 = time_2001
                else:
                    var.rate3_2001 += 1
                    #print time_2001,var.temp_2001,data
                    var.temp_2001 = time_2001
                    var.er_rate2001 += 1
                    if var.sht2_colx < var.value_sht2_err:
                        fn.write_single_data(sht2,num,var.sht2_colx,data)
                        var.sht2_colx += 1
                    

        else:
            pass
        
        # 里程是否支持、异常的判断
        if mileage == -1 or mileage == 0:
            var.mileage_no += 1
        elif var.mileage_init <= mileage <= var.value_mileage_max:
            var.mileage_yes += 1
            if var.mileage_yes > 1 and (mileage - var.mileage_init > 30):
                var.mileage_ab += 1
                #print mileage,var.mileage_init,data
            var.mileage_init = mileage
        else:
            var.mileage_ab += 1
            #print mileage,var.mileage_init
        # 油量是否支持、异常的判断
        oil_split = oil.split(',')
        for i in oil_split:
            try:
                oil_int = int(i)
            except:
                oil_int = -1
                var.oil_ab += 1
            if var.value_oil_min <= oil_int <= var.value_oil_max:
                var.oil_yes += 1
            elif oil_int == -1 :
                var.oil_no += 1
            else:
                var.oil_ab += 1
        # 电压的应用
        var.dt_volt[pk_2001.group(1)] = volt_2001
        # 转速是否异常的判断
        if enginespeed == -1:
            var.enginespeed_no += 1
        elif var.value_enginespeed_min <= enginespeed < var.value_enginespeed_max:
            var.enginespeed_yes += 1
        else:
            var.enginespeed_ab += 1
        # 速度是否支持、异常的判断
        speed_split = speed.split(',')
        for i in speed_split:
            try:
                speed_int = int(i)
            except:
                speed_int = -1
                var.speed_ab += 1
            if var.value_speed_min <= speed_int <= var.value_speed_max:
                var.speed_yes += 1
            elif speed_int == -1 :
                var.speed_no += 1
            else:
                var.speed_ab += 1
    else:
        var.er_2001 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1

# pk_2011包的处理
def pk_2011(data,num,sht2):
    pk_2011 = re.search(var.re_2011,data)
    if pk_2011 is not None:
        try:
            speed_gps = float(pk_2011.group(4))
        except Exception,ex:
            speed_gps = 0.0
            print Exception,"pk2011:",ex
        if speed_gps > 10.0:
            var.sign_2011 += 1
        else:
            pass
        # gps两点的距离计算
        if var.f1 == 0:
            var.f1 = float(pk_2011.group(1))
            var.f2 = float(pk_2011.group(2))
            #print 'f1,f2:',var.f1,var.f2

        else:

            t1 = float(pk_2011.group(1))
            t2 = float(pk_2011.group(2))
            #print 't1,t2:',var.f1,var.f2,t1,t2
            if var.f1 != t1 and var.f2 != t2:
                
                dist = gps.GPS().spherical_distance(var.f1,var.f2,t1,t2)

                if dist > 3:
                    # gps两点的距离大于3，认为定位存在问题
                    #print data,var.f1,var.f2,t1,t2
                    var.ct_distance += 1

                    if var.sht2_colx < var.value_sht2_err and var.ct_4001 > 0:
                        fn.write_single_data(sht2,num,var.sht2_colx,data)
                        var.sht2_colx += 1                    
                else:
                    pass
                var.f1 = t1
                var.f2 = t2
        
    else: 
        var.er_2011 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
# pk_2021包的处理
def pk_2021(data,num,sht2):
    pk_2021 = re.search(var.re_2021,data)
    if pk_2021 is not None:
        lac_2021 = int(pk_2021.group(1))
        if var.lac_value == 0:
            var.lac_value = lac_2021
        elif var.lac_value != lac_2021:
            var.sign_2021 += 1 
            var.lac_value = lac_2021
        else:
            pass
    else: 
        var.er_2021 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1

# pk_2031包的处理
def pk_2031(data,num,sht2):
    pk_2031 = re.search(var.re_2031,data)
    if pk_2031 is not None:
        pass
    else: 
        var.er_2031 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1

# pk_3021包的处理
def pk_3021(data,num,sht2):
    pk_3021 = re.search(var.re_3021,data)
    if pk_3021 is not None:
        if re.search('4E3A002D',data) is not None:
            var.er_3021 += 1
            if var.sht2_colx < var.value_sht2_err:
                fn.write_single_data(sht2,num,var.sht2_colx,data)
                var.sht2_colx += 1
        else:
            pass
    else: 
        var.er_3021 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1


# pk_3031包的处理
def pk_3031(data,num,sht2):
    pk_3031 = re.search(var.re_3031,data)
    if pk_3031 is not None:
        pass
    else: 
        var.er_3031 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        
# pk_3032包的处理
def pk_3032(data,num,sht2):
    pk_3032 = re.search(var.re_3032,data)
    if pk_3032 is not None:
        var.dt_discon.append(pk_3032.group(1))
    else: 
        var.er_3032 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1

# 4001包的处理
def pk_4001(data,num,sht2,datatime):
    var.temp_2001 = ''
    var.rate_sign = 1
    var.dt_volt[datatime] = var.value_volt_4001
    pk_4001 = re.search(var.re_4001,data)
    if pk_4001 is not None:
        vin = pk_4001.group(5)
        if len(vin) == 17:
            var.ct_vin += 1
            var.vin_value = vin
        else:
            pass
    else:
        var.er_4001 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        
    if cmp(var.temp_4001,datatime) != 0:
        var.ct_4001 += 1
        var.temp_4001 = datatime
    else:
        var.temp_4001 = datatime
        
# 4002包的处理
def pk_4002(data,num,sht2,datatime):
    var.rate_sign = 2
    var.dt_volt[datatime] = var.value_volt_4002
    pk_4002 = re.search(var.re_4002,data)
    if pk_4002 is not None:
        if pk_4002.group(1) != '<a>-1.0</a><o>-1.0</o><s>-1.0</s>':
            speed_4002 = pk_4002.group(4)
            if speed_4002 != -1.0:
                if float(speed_4002) > var.speed_gps_4002:
                    var.sign_4002 += 1
    else:
        var.er_4002 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        
    if cmp(var.temp_4002,datatime) != 0:
        var.ct_4002 += 1
        var.temp_4002 = datatime
    else:
        var.temp_4002 = datatime
# 4011包的处理
def pk_4011(data,num,sht2):
    pk_4011 = re.search(var.re_4011,data)
    if pk_4011 is not None:
        var.ct_vlow += 1
        volt_4011 = float(pk_4011.group(2))
        var.dt_volt[pk_4011.group(1)] = volt_4011
    else:
        var.er_4011 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        

# pk_5001包的处理
def pk_5001(data,num,sht2):
    pk_5001 = re.search(var.re_5001,data)
    if pk_5001 is not None:
        if pk_5001.group(1) != '<a>-1.0</a><o>-1.0</o><s>-1.0</s>':
            
            try:
                speed_gps = float(pk_5001.group(4))
            except Exception,ex:
                speed_gps = 0.0
                print Exception,":",ex
            if speed_gps > 10.0:
                var.sign_2011 += 1
            else:
                pass
        
    else: 
        var.er_5001 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        

# pk_5005包的处理
def pk_5005(data,num,sht2):
    pk_5005 = re.search(var.re_5005,data)
    if pk_5005 is not None:
        pass
    else: 
        var.er_5005 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        

# pk_5006包的处理
def pk_5006(data,num,sht2):
    pk_5006 = re.search(var.re_5006,data)
    if pk_5006 is not None:
        pass
    else: 
        var.er_5006 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        

# pk_6001包的处理
def pk_6001(data,num,sht2):
    if cmp(var.data_6001,data) != 0:
        var.data_6001 = data
        pk_6001 = re.search(var.re_6001,data)
        if pk_6001 is not None:

            type_6001 = pk_6001.group(1)
            if type_6001 == '101':
                # 实时诊断，统计诊断的系统号
                sys_num = pk_6001.group(3)
                if sys_num == '-1':
                    pass
                else:
                    if sys_num not in var.dgak_list:
                        var.dgak_list.append(sys_num)
                    else:
                        pass

            elif type_6001 == '201':
                # 满足条件，开始诊断
                var.dgtg_ys += 1
            elif type_6001 == '202':
                # 不满足诊断条件
                var.dgtg_no += 1
            elif type_6001 == '205':
                var.dgtg_ag += 1
                sys_num = pk_6001.group(3)
                if sys_num == '-1':
                    pass
                else:
                    if sys_num not in var.dgak_list:
                        var.dgtg_list.append(sys_num)
                    else:
                        pass
            elif type_6001 == '206':
                # 诊断过程中车辆行驶
                var.dgtg_ab += 1
            elif type_6001 == '207':
                # 诊断过程中车辆熄火
                var.dgtg_ac += 1
            elif type_6001 == '210':
                # 诊断完成
                var.dgtg_ae += 1
            else:
                # 其他异常
                var.dgtg_af += 1
        else: 
            var.er_6001 += 1
            if var.sht2_colx < var.value_sht2_err:
                fn.write_single_data(sht2,num,var.sht2_colx,data)
                var.sht2_colx += 1
    else:
        pass

# pk_9000包的处理
def pk_9000(data,num,sht2):
    pk_9000 = re.search(var.re_9000,data)
    if pk_9000 is not None:
        pass
    else: 
        var.er_9000 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1

# pk_9100包的处理
def pk_9100(data,num,sht2):
    if cmp(var.data_9100,data) != 0:
        var.data_9100 = data
        pk_9100 = re.search(var.re_9100,data)
        if pk_9100 is not None:
            status = pk_9100.group(1)
            if status == '101':
                var.tacc_ys += 1
            elif status == '102':
                var.tacc_no += 1
            elif status == '103':
                var.tacc_ab += 1
            elif status == '201':
                var.tacc_ac += 1
            elif status == '202':
                var.tacc_ad += 1
            elif status == '203':
                var.tacc_ae += 1
            else:
                pass
            
        else: 
            var.er_9100 += 1
            if var.sht2_colx < var.value_sht2_err:
                fn.write_single_data(sht2,num,var.sht2_colx,data)
                var.sht2_colx += 1
    else:
        pass

# pk_9990包的处理
def pk_9990(data,num,sht2):
    pk_9990 = re.search(var.re_9990,data)
    if pk_9990 is not None:
        pass
    else: 
        var.er_9990 += 1
        if var.sht2_colx < var.value_sht2_err:
            fn.write_single_data(sht2,num,var.sht2_colx,data)
            var.sht2_colx += 1
        

# 9999包的处理
def pk_9999(data,num,sht2):
    pk_9999 = re.search(var.re_9999,data)
    if pk_9999 is not None:
        infor_x = pk_9999.group(2)
        volt_9999 = float(pk_9999.group(5))
        var.dt_volt[pk_9999.group(1)] = volt_9999

        if infor_x == '0':
            var.ct_0 += 1
        elif infor_x == '1':
            var.ct_1 += 1
        elif infor_x == '2':
            var.ct_2 += 1
        elif infor_x == '3':
            var.ct_3 += 1
        elif infor_x == '4':
            var.ct_4 += 1
        elif infor_x == '5':
            var.ct_5 += 1
        elif infor_x == '6':
            var.ct_6 += 1
        elif infor_x == '7':
            var.ct_7 += 1
        elif infor_x == '9011':
            var.ct_9011 += 1
        elif infor_x == '9021':
            var.ct_9021 += 1
        elif infor_x == '9031':
            var.ct_9031 += 1
        elif infor_x == '9041':
            var.ct_9041 += 1
        elif infor_x == '9051':
            var.ct_9051 += 1
        elif infor_x == '9052':
            var.ct_9052 += 1
        elif infor_x == '9053':
            var.ct_9053 += 1
        elif infor_x == '9054':
            var.ct_9054 += 1
        elif infor_x == '9061':
            var.ct_9061 += 1
        elif infor_x == '9062':
            var.ct_9062 += 1
        elif infor_x == '9063':
            var.ct_9063 += 1
        elif infor_x == '9064':
            var.ct_9064 += 1
        elif infor_x == '9065':
            var.ct_9065 += 1
        elif infor_x == '9066':
            var.ct_9066 += 1
        elif infor_x == '9067':
            var.ct_9067 += 1
        elif infor_x == '9068':
            var.ct_9068 += 1
        elif infor_x == '9069':
            var.ct_9069 += 1
        elif infor_x == '9071':
            var.ct_9071 += 1
        elif infor_x == '9072':
            var.ct_9072 += 1
        elif infor_x == '9073':
            var.ct_9073 += 1
        elif infor_x == '9074':
            var.ct_9074 += 1
        elif infor_x == '9075':
            var.ct_9075 += 1
        elif infor_x == '9076':
            var.ct_9076 += 1
        elif infor_x == '9081':
            var.ct_9081 += 1
        elif infor_x == '9082':
            var.ct_9082 += 1
        elif infor_x == '9100':
            var.ct_9100 += 1
        elif infor_x == '9101':
            var.ct_9101 += 1
        elif infor_x == '9102':
            var.ct_9102 += 1
        elif infor_x == '9103':
            var.ct_9103 += 1
        elif infor_x == '9109':
            var.ct_9109 += 1

        elif infor_x == '9301':
            var.ct_9301 += 1
        elif infor_x == '9302':
            var.ct_9302 += 1
        elif infor_x == '9303':
            var.ct_9303 += 1
        elif infor_x == '9304':
            var.ct_9304 += 1
        elif infor_x == '9305':
            var.ct_9305 += 1
        elif infor_x == '9306':
            var.ct_9306 += 1
        elif infor_x == '9307':
            var.ct_9307 += 1
        elif infor_x == '9308':
            var.ct_9308 += 1
        
        elif infor_x == '9309':
            var.ct_9309 += 1

        elif infor_x == '9310':
            var.ct_9310 += 1
            pk_9310 = re.search(var.re_9310,data)
            if pk_9310 is not None:
                pass
            else:
                var.er_9999 += 1
                if var.sht2_colx < var.value_sht2_err:
                    fn.write_single_data(sht2,num,var.sht2_colx,data)
                    var.sht2_colx += 1
        elif infor_x == '9331':
            var.ct_9331 += 1
        elif infor_x == '9332':
            var.ct_9332 += 1
        elif infor_x == '9401':
            var.ct_9401 += 1
        
        elif infor_x == '9991':
            var.ct_9991 += 1
        elif infor_x == '9992':
            var.ct_9992 += 1
        elif infor_x == '9993':
            var.ct_9993 += 1
        elif infor_x == '9994':
            var.ct_9994 += 1
        elif infor_x == '9665':
            var.ct_9995 += 1

        # 统计其他的异常情况
        else:
            pass
    else:
        pass
        #var.er_9999 += 1
        #if var.sht2_colx < var.value_sht2_err:
            #fn.write_single_data(sht2,num,var.sht2_colx,data)
            #var.sht2_colx += 1
        
        

# 2001包内的数据判断
def judge_2001(sht1,num):
    # 里程的判断
    if var.mileage_ab > 0:
        fn.write_single_data(sht1,num,var.col_mileage,'异常')
    elif var.mileage_no >0 and var.mileage_yes == 0:
        fn.write_single_data(sht1,num,var.col_mileage,'不支持')
    else:
        fn.write_single_data(sht1,num,var.col_mileage,'支持')
    # 油量的判断
    if var.oil_ab > 0:
        fn.write_single_data(sht1,num,var.col_oil,'异常')
    elif var.oil_no >0 and var.oil_yes == 0:
        fn.write_single_data(sht1,num,var.col_oil,'不支持')
    else:
        fn.write_single_data(sht1,num,var.col_oil,'支持')
    # 转速的判断
    if var.enginespeed_ab > 0 :
        fn.write_single_data(sht1,num,var.col_enginespeed,'异常')
    elif var.enginespeed_no > 0 and var.enginespeed_yes == 0:
        fn.write_single_data(sht1,num,var.col_enginespeed,'不支持')
    else:
        fn.write_single_data(sht1,num,var.col_enginespeed,'支持')
    # 车速的判断
    if var.speed_ab > 0:
        fn.write_single_data(sht1,num,var.col_speed,'异常')
    elif var.speed_no > 0 and var.speed_yes == 0:
        fn.write_single_data(sht1,num,var.col_speed,'不支持')
    else:
        fn.write_single_data(sht1,num,var.col_speed,'支持')

    # 2001包时间间隔判断
    if var.rate3_2001 > 0:
        # 上报间隔不正常
        fn.write_single_data(sht1,num,var.col_rate2001,'异常')
    elif var.rate1_2001 == 0 and var.rate2_2001 > 0:
        # 前3个包上报不正常
        fn.write_single_data(sht1,num,var.col_rate2001,'异常')
    elif var.rate1_2001 > 0 and var.rate2_2001 > 0:
        # 上报正常
        fn.write_single_data(sht1,num,var.col_rate2001,'正常')
    elif var.rate4_2001 > 0 and var.rate1_2001 == 0 and var.rate2_2001 == 0:
        fn.write_single_data(sht1,num,var.col_rate2001,'频繁点熄火')
    else:
        # 未达到判断条件
        fn.write_single_data(sht1,num,var.col_rate2001,'待定')


def cartypes(cursor_obd,imei,terminal_id):
    try:
        cursor_obd.execute(var.sql_carinfo1 + str(terminal_id) + var.sql_carinfo2)
        rows_style2 = cursor_obd.fetchall ()
        if rows_style2 != ():
            licence_plate = rows_style2[0][0]
            vin = rows_style2[0][1]
            if vin == None:
                vin = 'null'
            if licence_plate == None:
                licence_plate = 'Null'
            style_id = rows_style2[0][2]
            if style_id != None:
                cursor_obd.execute(var.sql_carinfo3 + str(style_id) )
                rows_style3 = cursor_obd.fetchall () 
                model_id = rows_style3[0][0]
                style_name = rows_style3[0][1]
                if style_name == None:
                    style_name = 'null'
                if model_id != None:
                    cursor_obd.execute(var.sql_carinfo4 + str(model_id) )
                    rows_style4 = cursor_obd.fetchall () 
                    model_name = rows_style4[0][0]
                    if model_name == None:
                        model_name = 'null'
                    return model_name,style_name,vin,licence_plate
                else:
                    return 'null',style_name,vin,licence_plate
            else:
                return 'null','null',vin,licence_plate
        else:
            return 'null','null','null','null'
    except Exception,ex:
        print Exception,"cartypes:",ex,imei
        return 'except','except','except','except'

def tcm_upgrade(cursor_tcm,imei):
    try:
        #sql = var.sql_upgrade1 + imei + var.sql_upgrade2
        sql = var.sql_upgrade1 + imei
        cursor_tcm.execute(sql)
        rows_tcm = cursor_tcm.fetchall() 
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
    except Exception,ex:
        print Exception,"tcm:",ex,imei


def write_lgin_nolgin_count(sht1):    
    fn.write_single_data(sht1,var.len_imei+5,0,'count_login:')
    fn.write_single_data(sht1,var.len_imei+6,0,'count_nolgn:')
    fn.write_single_data(sht1,var.len_imei+7,0,'servererror:')

    
    fn.write_single_data(sht1,var.len_imei+5,2,var.login_imei)
    fn.write_single_data(sht1,var.len_imei+6,2,var.nologin_imei)
    fn.write_single_data(sht1,var.len_imei+7,2,var.server_error)

# 从serviceopen获取group信息
def group_customer(cursor_csr,imei):
    sql = var.sql_customer1 + imei
    result = pyMysql.mysqlGetMessage(cursor_csr,sql)
    if result == -1:
        return -1
    elif result == ():
        return "None1"
    else:
        tid = result[0][0]
        sql = var.sql_customer2 + str(tid)
        result = pyMysql.mysqlGetMessage(cursor_csr,sql)
        if result == -1:
            return -1
        elif result == ():
            return "None2"
        else:
            group_id = result[0][0]
            if group_id != None:
                return group_id
            else:
                return "None3"

# 用户最近登录app时间
def applogin(cursor_obd,imei):
    sql = var.sql_applogin + imei
    result = pyMysql.mysqlGetMessage(cursor_obd,sql)
    if result == -1:
        return -1
    elif result == ():
        return "None"
    else:
        apploginrecord = result[0][0]
        if apploginrecord == None:
            return "No_Record"
        else:
            return apploginrecord
    
# 获取用户的手机号码
def customermoble(cursor_obd,tid):
    sql = var.sql_phone1 + tid
    result = pyMysql.mysqlGetMessage(cursor_obd,sql)
    if result == -1:
        return -1
    elif result == ():
        return "None1"
    else:
        customer_id = result[0][0]
        sql = var.sql_phone2 + str(customer_id)
        result = pyMysql.mysqlGetMessage(cursor_obd,sql)
        if result == -1:
            return -1
        elif result == ():
            return "None2"
        else:
            mobile = result[0][0]
            if mobile != None:
                return mobile
            else:
                return "None3"

# 设备所属批次
def product_batch(cursor_tcm,imei):
    #sql = var.sql_batch1 + imei + var.sql_batch2
    sql = var.sql_batch1 + imei
    result = pyMysql.mysqlGetMessage(cursor_tcm,sql)
    if result == -1:
        return -1
    elif result == ():
        return "None"
    else:
        #batch = result[0][0]
        batch = result[len(result)-1][0]
        if batch == None:
            return "No_Record"
        else:
            return batch

    
        
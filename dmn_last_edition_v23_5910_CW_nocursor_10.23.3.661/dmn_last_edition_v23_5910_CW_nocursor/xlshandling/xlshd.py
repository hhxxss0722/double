#-*- coding:utf-8 -*-
from xlutils.copy import copy
import xlwt,xlrd
from variable import var
import datetime
from filehandling import fn
import string
import urllib2

def obd_login_table(wbk_dx,table_dx):

    # 获得列的所有值
    imei_dx = table_dx.col_values(var.col_imei)
    supplier_dx = table_dx.col_values(var.col_type)
    login_dx = table_dx.col_values(var.col_login)
    # 下行，03-02 修改
    #network_dx = table_dx.col_values(var.col_network)
    network_dx = table_dx.col_values(var.col_group)
    len_dx = len(login_dx)
    #print table_dx.row_values(52)
    # 打开 obd_login_table.xls
    if var.sign_test == 0:
        wbk_lx = xlrd.open_workbook(var.everyday_login_path)
    else:
        wbk_lx = xlrd.open_workbook(r'D:\xiao\obd\obd_login_table.xls')
    table_lx = wbk_lx.sheet_by_index(0)
    imei_lx = table_lx.col_values(var.xls_imei)
    cols_lx = table_lx.ncols
    #rows_lx = table_lx.nrows
    len_lx = len(imei_lx)  
    
    # 复制xls
    wbk_cp = copy(wbk_lx)
    sheet = wbk_cp.get_sheet(0)
    if var.dt == table_lx.cell_value(0,cols_lx-1):
        cols_lx = cols_lx - 1
    else:
        # 写入当天的日期
        sheet.write(0,cols_lx,var.dt)

    # data.xls数据写入obd_login_table.xls
    for dx in xrange(len_dx):
        if type(imei_dx[dx]) == unicode and imei_dx[dx][0:2] == '86':
            # imei不在obd_login_table.xls中
            if imei_dx[dx] not in imei_lx and cmp(imei_dx[dx],'imei') != 0:
                sheet.write(len_lx,var.xls_imei,imei_dx[dx])
                sheet.write(len_lx,var.xls_network,network_dx[dx])
                sheet.write(len_lx,var.xls_supplier,supplier_dx[dx])
                sheet.write(len_lx,var.xls_order,len_lx)
                if login_dx[dx] == 'login':
                    sheet.write(len_lx,cols_lx,'0')
                elif login_dx[dx] == 'nolgin':
                    sheet.write(len_lx,cols_lx,'2')
                elif login_dx[dx] == 'server_error':
                    sheet.write(len_lx,cols_lx,'4')
                else:
                    sheet.write(len_lx,cols_lx,'1')
                len_lx += 1
            # imei 已在obd_login_table.xls中
            elif imei_dx[dx] in imei_lx:
                # 获取特定imei号的位置
                index=imei_lx.index(imei_dx[dx])
                # 下2行，03-02 增加.
                sheet.write(index,var.xls_supplier,supplier_dx[dx])
                sheet.write(index,var.xls_network,network_dx[dx])
                if login_dx[dx] == 'login':
                    sheet.write(index,cols_lx,'0')
                elif login_dx[dx] == 'nolgin':
                    sheet.write(index,cols_lx,'2')
                elif login_dx[dx] == 'server_error':
                    sheet.write(index,cols_lx,'4')
                else:
                    sheet.write(index,cols_lx,'1')

    if var.sign_test == 0:
        wbk_cp.save(var.everyday_login_path)
    else:
        wbk_cp.save(r'D:\xiao\obd\obd_login_table.xls')
    

def xls_handling(wbk_dx,table_dx):
    # 新建xls表，bug.xls
    wbk_bg = xlwt.Workbook(encoding = 'utf-8')
    sheet_bg = wbk_bg.add_sheet('sheet 1',cell_overwrite_ok=True)
    #nrow_bg = sheet_bg.nrows
        
    # bug.xls的列头
    fn.write_dict_data(sheet_bg,var.row_bg,var.dict_bg)
    var.row_bg += 1
    
    # 打开设备登录xls
    if var.sign_test == 0:
        wbk_lp = xlrd.open_workbook(var.everyday_login_path)
    else:
        wbk_lp = xlrd.open_workbook(r'D:\xiao\obd\obd_login_table.xls')
    table_lp = wbk_lp.sheet_by_index(0)
    col_lp = table_lp.ncols
    imei_lp = table_lp.col_values(var.xls_imei)
    
    # data.xls的数据异常判断
    rows_xh = table_dx.nrows
    
    for row in xrange(1,rows_xh):
        rows_value = table_dx.row_values(row)

        # 设备每天登录情况的处理
        if rows_value[var.col_imei] in imei_lp:
            index_lp = imei_lp.index(rows_value[var.col_imei])
            value_lp1 = table_lp.cell_value(index_lp,col_lp-1)
            value_lp2 = table_lp.cell_value(index_lp,col_lp-2)
            value_lp3 = table_lp.cell_value(index_lp,col_lp-3)
            value_lp4 = table_lp.cell_value(index_lp,col_lp-4)
            value_lp5 = table_lp.cell_value(index_lp,col_lp-5)
            # 前4天连续异常，当天恢复正常
            if value_lp2 != '' and value_lp3 != '' and value_lp4 != '' and value_lp5 != '':
                if value_lp1 == '0' and value_lp2 != '0' and value_lp3 != '0' and value_lp4 != '0' and value_lp5 != '0':
                    if value_lp2 != '4' and value_lp3 != '4' and value_lp4 != '4' and value_lp5 != '4':
                        xls_data(sheet_bg,table_dx,row,var.col_login,u'：设备恢复登录')
            # 包括当天在内连续5天异常
            if value_lp2 != '' and value_lp3 != '' and value_lp4 != '' and value_lp5 != '':
                if value_lp1 == '2' and value_lp2 != '0' and value_lp3 != '0' and value_lp4 != '0' and value_lp5 == '0':
                    if value_lp2 != '4' and value_lp3 != '4' and value_lp4 != '4' and value_lp5 != '4':
                        xls_data(sheet_bg,table_dx,row,var.col_login,u'：设备不再登录')
                        # 自动下发重启指令
                        '''
                        if var.ctrl_sign == 'JG':
                            pass
                        else:
                            if var.model_sign == 0 or var.model_sign == 1:
                                if rows_value[var.col_imsi] != 'null':
                                    var.ct_sms += 1
                                    url = 'http://10.21.1.17:8080/obd-ws/ws/0.1/debug/reset?imei=' + rows_value[var.col_imei] + '&flag=0'
                                    urllib2.urlopen(url, timeout=10)
                                    var.imei_list.append(rows_value[var.col_imei])
                        '''
        else:
            pass
        '''
        # 车辆里程和油量的处理
        for i in xrange(var.col_mileage,var.col_oil+1):
            if rows_value[i] == u'异常':

                xls_data(sheet_bg,table_dx,row,i,u'异常')
        
        # 车辆转速和车速的处理
        for i in xrange(var.col_enginespeed,var.col_speed+1):
            if rows_value[i] == u'异常':
                xls_data(sheet_bg,table_dx,row,i,u'异常')
            elif rows_value[i] == u'不支持':
                xls_data(sheet_bg,table_dx,row,i,u'不支持')
        '''
        # C1设备主控和CM3的默认版本问题，设备持续工作
        if (rows_value[var.col_software] == 'C101123802' and rows_value[var.col_hardware] == '0003010013' and rows_value[var.col_login] == 'login') or \
            (rows_value[var.col_software] == 'C100923713' and rows_value[var.col_hardware] == '0003010012' and rows_value[var.col_login] == 'login'):
            xls_data(sheet_bg,table_dx,row,var.col_hardware,u'可能持续工作,自动下发重启指令')
            # 自动下发重启指令
            if var.ctrl_sign == 'JG':
                pass
            else:
                if var.model_sign == 0 or var.model_sign == 1:
                    if rows_value[var.col_imsi] != 'null':
                        var.ct_sms += 1
                        url = 'http://10.21.1.17:8080/obd-ws/ws/0.1/debug/software/upgrade?imei=' + rows_value[var.col_imei] + '&flag=0'
                        urllib2.urlopen(url, timeout=5)
                        var.imei_list.append(rows_value[var.col_imei])

        # C2设备主控和CM3升级
        if var.ctrl_sign == 'JG':
            if rows_value[var.col_login] == 'login' and rows_value[var.col_imsi] != 'null':
                if (rows_value[var.col_software] == 'C120104915' or rows_value[var.col_software] == 'C220144915' or rows_value[var.col_software] == 'C220324B18' or rows_value[var.col_software] == 'C220384C17' or rows_value[var.col_software] == 'C220445115'):
                    # 自动下发重启指令
                    if var.model_sign == 0 or var.model_sign == 1:
                        var.ct_sms += 1
                        url = 'http://172.16.200.153:8080/obd-ws/ws/0.1/debug/software/upgrade?imei=' + rows_value[var.col_imei] + '&flag=0'
                        urllib2.urlopen(url, timeout=5)
                        var.imei_list.append(rows_value[var.col_imei])
                    else:
                        pass
                else:
                    pass
            else:
                pass
            
        else:
            if rows_value[var.col_login] == 'login' and rows_value[var.col_imsi] != 'null':
                if (rows_value[var.col_software] == 'C200284625' or rows_value[var.col_software] == 'C200484711' or rows_value[var.col_software] == 'C200644722' or rows_value[var.col_software] == 'C200864918' or rows_value[var.col_software] == 'C201264B18' or rows_value[var.col_software] == 'C201405115' ):
                    # 自动下发重启指令
                    if var.model_sign == 0 or var.model_sign == 1:
                        var.ct_sms += 1
                        url = 'http://10.21.1.17:8080/obd-ws/ws/0.1/debug/software/upgrade?imei=' + rows_value[var.col_imei] + '&flag=0'
                        urllib2.urlopen(url, timeout=5)
                        var.imei_list.append(rows_value[var.col_imei])
                    else:
                        pass
                else:
                    pass
            else:
                pass


        '''
        # 下发的配置信息处理 -- 低压阈值不是11.3
        if rows_value[var.col_alarmvolt] != '' and rows_value[var.col_alarmvolt] != '11.3':
            xls_data(sheet_bg,table_dx,row,var.col_alarmvolt,u'：' + rows_value[var.col_alarmvolt])
        
        # 下发的配置信息处理 -- 震动阈值不是0-255 or 1000-1255
        if rows_value[var.col_shakevalue] != '':
            if -1.0 <float(rows_value[var.col_shakevalue]) < 256.0 or 999 <float(rows_value[var.col_shakevalue] < 1256):
                pass
            else:
                xls_data(sheet_bg,table_dx,row,var.col_shakevalue,u'：' + rows_value[var.col_shakevalue])
            
        # 下发的配置信息处理 -- acc_gps 值不是0.70,-0.85,25.0,20.0
        if var.ctrl_sign == 'JG':
            if rows_value[var.col_accgps] != '' and rows_value[var.col_accgps] != '0.70,-0.85,20.0,20.0':
                xls_data(sheet_bg,table_dx,row,var.col_accgps,u'：' + rows_value[var.col_accgps])
        else:
            if rows_value[var.col_accgps] != '' and rows_value[var.col_accgps] != '0.70,-0.85,25.0,20.0':
                xls_data(sheet_bg,table_dx,row,var.col_accgps,u'：' + rows_value[var.col_accgps])
        
        # 下发的配置信息处理 -- 碰撞阈值不是7.0
        if rows_value[var.col_collision] != '' and rows_value[var.col_collision] != '7.0':
            xls_data(sheet_bg,table_dx,row,var.col_collision,u'：' + rows_value[var.col_collision])
        '''
        # 1004 次数等于0的处理
        if rows_value[var.col_count_1004] != '' and rows_value[var.col_count_1004] == 0:
            xls_data(sheet_bg,table_dx,row,var.col_count_1004,u'：' + str(int(rows_value[var.col_count_1004])))
        
        '''
        # 2001 次数大于150的处理
        if rows_value[var.col_count_2001] != '' and rows_value[var.col_count_2001] > 150:
            xls_data(sheet_bg,table_dx,row,var.col_count_2001,u'：' + str(int(rows_value[var.col_count_2001])))
        
        # 2011 次数大于2000的处理
        if rows_value[var.col_count_2011] != '' and rows_value[var.col_count_2011] > 2000:
            xls_data(sheet_bg,table_dx,row,var.col_count_2011,u'：' + str(int(rows_value[var.col_count_2011])))
        
        # 2021 次数大于65的处理
        if rows_value[var.col_count_2021] != '' and rows_value[var.col_count_2021] > 65:
            xls_data(sheet_bg,table_dx,row,var.col_count_2021,u'：' + str(int(rows_value[var.col_count_2021])))
        
        # 2031 次数大于10的处理
        if rows_value[var.col_count_2031] != '' and rows_value[var.col_count_2031] > 65:
            xls_data(sheet_bg,table_dx,row,var.col_count_2031,u'：' + str(int(rows_value[var.col_count_2031])))
        
        # 3021 次数大于10的处理
        if rows_value[var.col_count_3021] != '' and rows_value[var.col_count_3021] > 10:
            xls_data(sheet_bg,table_dx,row,var.col_count_3021,u'：' + str(int(rows_value[var.col_count_3021])))

        # 3031 次数大于1的处理
        if rows_value[var.col_count_3031] != '' and rows_value[var.col_count_3031] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_count_3031,u'：' + str(int(rows_value[var.col_count_3031])))

        # 4001\4002 次数大于25的处理
        for i in xrange(var.col_count_4001,var.col_count_4002+1):
            if rows_value[i] != '' and rows_value[i] > 25:
                xls_data(sheet_bg,table_dx,row,i,u'：' + str(int(rows_value[i])))
        '''
        # 4001 - 4002 差值大于2的处理
        if rows_value[var.col_count_4001] != '' and rows_value[var.col_count_4002] != '' and \
            (rows_value[var.col_count_4001]-rows_value[var.col_count_4002]) > 1:
            xls_data(sheet_bg,table_dx,row,var.col_count_4001,u'-4002数量大于2,排查')
        '''
        # 4011 次数大于0的处理
        if rows_value[var.col_count_4011] != '' and rows_value[var.col_count_4011] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_count_4011,u'：' + str(int(rows_value[var.col_count_4011])))
        
        # 5001 次数大于50的处理
        if rows_value[var.col_count_5001] != '' and rows_value[var.col_count_5001] > 50:
            xls_data(sheet_bg,table_dx,row,var.col_count_5001,u'：' + str(int(rows_value[var.col_count_5001])))
        
        
        # 5005\5006 次数大于3的处理
        for i in xrange(var.col_count_5005,var.col_count_5006+1):
            if rows_value[i] != '' and rows_value[i] > 3:
                xls_data(sheet_bg,table_dx,row,i,u'：' + str(int(rows_value[i])))
        '''
        
        
        # 9990 次数大于0的处理
        if rows_value[var.col_count_9990] != '' and rows_value[var.col_count_9990] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_count_9990,u'：' + str(int(rows_value[var.col_count_9990])))
        '''
        # 9999 次数大于50的处理
        if rows_value[var.col_count_9999] != '' and rows_value[var.col_count_9999] > 50:
            xls_data(sheet_bg,table_dx,row,var.col_count_9999,u'：' + str(int(rows_value[var.col_count_9999])))
        
        # 设备登录次数，上传数据包重复次数大于20次的处理
        for i in xrange(var.col_count_lgin,var.col_duplicate+1):
            if rows_value[i] != '' and rows_value[i] > 20:
                xls_data(sheet_bg,table_dx,row,i,u'：' + str(int(rows_value[i])))
        '''
        # 数据延迟上报至少1天的处理
        if rows_value[var.col_count_updelay] != '' and rows_value[var.col_count_updelay] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_count_updelay,u'：' + str(int(rows_value[var.col_count_updelay])) + u'，人工排查')
        
        # 漏报4001，误报4002的处理
        for i in xrange(var.col_count_miss4001,var.col_count_error4002+1):
            if rows_value[i] != '' and rows_value[i] > 0:
                xls_data(sheet_bg,table_dx,row,i,u'：' + str(int(rows_value[i])))

        # BNDS 次数大于1的处理
        if rows_value[var.col_bnds] != '' and rows_value[var.col_bnds] > 1:
            xls_data(sheet_bg,table_dx,row,var.col_bnds,u'：' + str(int(rows_value[var.col_bnds])))

        '''
        # 设备重启次数大于1的处理
        if rows_value[var.col_count_reset] != '' and rows_value[var.col_count_reset] > 1:
            xls_data(sheet_bg,table_dx,row,var.col_count_reset,u'：' + str(int(rows_value[var.col_count_reset])))
        '''

        # 2001包上报间隔的处理
        if rows_value[var.col_rate2001] != '' and rows_value[var.col_rate2001] == u'异常':
            xls_data(sheet_bg,table_dx,row,var.col_rate2001,u'：' + rows_value[var.col_rate2001])
        '''
        # 数据包格式异常的处理
        for i in xrange(var.col_form1004,var.col_formtime+1):
            if rows_value[i] != '':
                xls_data(sheet_bg,table_dx,row,i,u'数量：' + str(int(rows_value[i])))
        '''
        '''
        # 9061 次数大于0的处理
        if rows_value[var.col_debug_9061] != '' and rows_value[var.col_debug_9061] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_debug_9061,u'：' + str(int(rows_value[var.col_debug_9061])))
        '''
        # 9071\9072\9073\9073 次数大于0的处理
        for i in xrange(var.col_debug_9071,var.col_debug_9074+1):
            if rows_value[i] != '' and rows_value[i] > 0:
                xls_data(sheet_bg,table_dx,row,i,u'：' + str(int(rows_value[i])))
                
        # 9301 次数大于0的处理
        if rows_value[var.col_debug_9301] != '' and rows_value[var.col_debug_9301] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_debug_9301,u'：' + str(int(rows_value[var.col_debug_9301])))
        
        # 9303 次数大于0的处理
        if rows_value[var.col_debug_9303] != '' and rows_value[var.col_debug_9303] > 0:
            xls_data(sheet_bg,table_dx,row,var.col_debug_9303,u'：' + str(int(rows_value[var.col_debug_9303])))

        # 设备上报了数据，但没有配置下发
        if rows_value[var.col_login] == 'login' and rows_value[var.col_count_lgin] == '':
            xls_data(sheet_bg,table_dx,row,var.col_count_lgin,u'：无')
        

    if var.sign_test == 0:
        fn.savexls(wbk_bg,var.excel_file_name[:-9] + '-bug.xls')
    else:
        fn.savexls(wbk_bg,r'D:\xiao\obd\bug.xls')
    
def xls_data(sheet,table_dx,row,col,value):
    fn.write_single_data(sheet,var.row_bg,var.bg_0,var.row_bg)
    fn.write_single_data(sheet,var.row_bg,var.bg_1,table_dx.cell(row,var.col_type).value)
    fn.write_single_data(sheet,var.row_bg,var.bg_2,table_dx.cell(row,var.col_imei).value)
    fn.write_single_data(sheet,var.row_bg,var.bg_3,col)
    fn.write_single_data(sheet,var.row_bg,var.bg_4,table_dx.cell(0,col).value + value)
    fn.write_single_data(sheet,var.row_bg,var.bg_5,table_dx.cell(row,var.col_software).value)
    fn.write_single_data(sheet,var.row_bg,var.bg_6,table_dx.cell(row,var.col_hardware).value)
    
    fn.write_single_data(sheet,var.row_bg,var.bg_7,table_dx.cell(row,var.col_group).value)
    fn.write_single_data(sheet,var.row_bg,var.bg_8,table_dx.cell(row,var.col_network).value)
    
    fn.write_single_data(sheet,var.row_bg,var.bg_9,table_dx.cell(row,var.col_model).value)
    fn.write_single_data(sheet,var.row_bg,var.bg_10,table_dx.cell(row,var.col_style).value)
    fn.write_single_data(sheet,var.row_bg,var.bg_11,var.dt)
    var.row_bg += 1

#-*- coding:utf-8 -*-
from xlutils.copy import copy
import xlwt
import xlrd
from var import var
import datetime
from file import fn
import time

def login_record_everyday():
    #open result xls
    wbk_dx,table_dx = fn.openxlrd(var.path_rslt,u"data")
    imei_dx = table_dx.col_values(var.cl_imei)
    lgin_dx = table_dx.col_values(var.cl_lgin)
    len_dx = len(lgin_dx)
    
    #open login_record_everyday.xls
    wbk_lx = xlrd.open_workbook(var.path_lrcd)
    table_lx = wbk_lx.sheet_by_index(0)
    imei_lx = table_lx.col_values(var.imei_xls)
    cols_lx = table_lx.ncols
    len_lx = len(imei_lx)  
    
    #copy xls
    wbk_cp = copy(wbk_lx)
    sheet = wbk_cp.get_sheet(0)
    if var.dt == table_lx.cell_value(0,cols_lx-1):
        cols_lx = cols_lx - 1
    else:
        sheet.write(0,cols_lx,var.dt)

    #result.xls data write login_record_everyday.xls
    for dx in xrange(len_dx):
        if type(imei_dx[dx]) == unicode and imei_dx[dx][0:2] == "86":
            #imei not in login_record_everyday.xls
            if imei_dx[dx] not in imei_lx and cmp(imei_dx[dx],"imei") != 0:
                sheet.write(len_lx,var.imei_xls,imei_dx[dx])
                sheet.write(len_lx,var.sn_xls,len_lx)
                if lgin_dx[dx] == "login":
                    sheet.write(len_lx,cols_lx,u"√")
                elif lgin_dx[dx] == "nolgin":
                    sheet.write(len_lx,cols_lx,u"×")
                elif lgin_dx[dx] == "svr_err":
                    sheet.write(len_lx,cols_lx,u"?")
                else:
                    sheet.write(len_lx,cols_lx,u"?")
                len_lx += 1
            #imei in login_record_everyday.xls
            elif imei_dx[dx] in imei_lx:
                #imei index
                index=imei_lx.index(imei_dx[dx])
                if lgin_dx[dx] == "login":
                    sheet.write(index,cols_lx,u"√")
                elif lgin_dx[dx] == "nolgin":
                    sheet.write(index,cols_lx,u"×")
                elif lgin_dx[dx] == "svr_err":
                    sheet.write(index,cols_lx,u"?")
                else:
                    sheet.write(index,cols_lx,u"?")
            else:
                print "prt1 imei:%s,dx:%s" % (imei_dx[dx],dx)
        else:
            print "prt2 imei:%s,dx:%s" % (imei_dx[dx],dx)
    wbk_cp.save(var.path_lrcd)
    
    time.sleep(2)
    
    wbk_lr,table_lr = fn.openxlrd(var.path_lrcd,u"lred")
    cols_lr = table_lr.ncols
    rows_lr = table_lr.nrows
    imei_lr = table_lr.col_values(var.imei_xls)
    if cols_lr >=4:
        value_tday = table_lr.col_values(cols_lr-1)
        value_yday = table_lr.col_values(cols_lr-2)
        for rows in xrange(rows_lr):
            if value_tday[rows] == u"√" and value_yday[rows] == u"×":
                #设备恢复正常
                if imei_lr[rows] in imei_dx:
                    idx=imei_dx.index(imei_lr[rows])
                    if table_dx.cell_value(idx,var.cl_ct_3032) != "":
                        var.ct_resm += 1
                        var.dc_resm[imei_lr[rows]] = table_dx.cell_value(idx,var.cl_dscn) + "<br />"
                    else:
                        var.ct_resm += 1
                        var.dc_resm[imei_lr[rows]] = table_dx.cell_value(idx,var.cl_dlay) + "<br />"
                else:
                    var.dc_resm[imei_lr[rows]] = "y" + "<br />"
            elif value_tday[rows] == u"×" and value_yday[rows] == u"√":
                #设备进入失联
                var.ct_lost += 1
                var.dc_lost[imei_lr[rows]] = "x" + "<br />"
            else:
                pass
    else:
        pass
    
    #if var.type_imei != 'mlxy' and var.type_imei != 'baoxian':
    if var.type_imei != 'baoxian':
        rst_9081 = table_dx.col_values(var.cl_db_9081)
        rst_9082 = table_dx.col_values(var.cl_db_9082)
        rst_3006 = table_dx.col_values(var.cl_db_3006)
        rst_3012 = table_dx.col_values(var.cl_db_3012)
        for dx in xrange(1,len_dx):
            if rst_9081[dx] != "" and int(rst_9081[dx]) > 0:
                var.dc_debg[imei_dx[dx]] = "9081" + "  _  " + str(rst_9081[dx]) +  "<br />"
            if rst_9082[dx] != "" and int(rst_9082[dx]) > 0:
                var.dc_debg[imei_dx[dx]] = "9082" + "  _  " + str(rst_9082[dx]) + "<br />"
            if rst_3006[dx] != "" and int(rst_3006[dx]) > 0:
                var.dc_debg[imei_dx[dx]] = "3006" + "  _  " + str(rst_3006[dx]) +  "<br />"
            if rst_3012[dx] != "" and int(rst_3012[dx]) > 0:
                var.dc_debg[imei_dx[dx]] = "3012" + "  _  " + str(rst_3012[dx]) +  "<br />"
            
        
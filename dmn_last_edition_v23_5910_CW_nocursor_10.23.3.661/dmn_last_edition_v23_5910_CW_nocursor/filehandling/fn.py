#-*- coding:utf-8 -*-
import xlwt
import xlrd
from xlutils.copy import copy

# 打开imei的文件，得到imei号

def open_file_imei(file_imei_txt):
    file_imei = open(file_imei_txt,'r')
    imei_lines = file_imei.readlines()
    return file_imei,imei_lines

# 关闭imei的文件

def close_file_imei(file_imei):
    file_imei.close()
    print 'file_imei is closed.'

# 创建excel表格

def openxlwt():
    wbk = xlwt.Workbook(encoding = 'utf-8')
    data = wbk.add_sheet('data',cell_overwrite_ok=True)
    abnormal = wbk.add_sheet('abnormal',cell_overwrite_ok=True) 
    print 'xlwt open success.'
    return wbk,data,abnormal

# 打开excel表格

def openxlrd(excel_file_name,name):
    wbk = xlrd.open_workbook(excel_file_name)
    table = wbk.sheet_by_name(name)
    return wbk,table

# 修改excel表格

def revisexlrd(excel_file_name,name):
    wbk_r = xlrd.open_workbook(excel_file_name)
    table = wbk_r.sheet_by_name(name)
    wbk = copy(wbk_r)
    sheet = wb.get_sheet(0)
    return wbk,table,sheet
    

# 保存excel表格

def savexls(wbk,excel_file_name):
    wbk.save(excel_file_name)


# excel写入单个数据

def write_single_data(sheet,rowx,colx,data_object):
    sheet.write(rowx,colx,data_object)

# excel写入dict数据
def write_dict_data(sheet,rowx,dict):
    for key in dict.keys():
        sheet.write(rowx,key,dict[key])

# excel写入dict数据
def write_dict_other(sheet,rowx,dict):
    for key in dict.keys():
        if dict[key] > 0:
            sheet.write(rowx,key,dict[key])

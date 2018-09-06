import xlwt,xlrd
from xlutils.copy import copy
import time,os

localTime = time.strftime("%Y%m%d",time.localtime())
file_name = 'c:\\testlog\\' + localTime + '.xls'
# def make_file(file_name):
#     if os.path.exists(file_name):

# def modify_xlrd(excel_name, name):
#     if os.path.exists(file_name):
#         work_bk_r = xlrd.open_workbook(excel_name)
#     else:
#         table = work_bk_r.sheet_by_name(name)
#         work_bk = copy(work_bk_r)
#         sheet = work_bk.get_sheet(0)
#         return work_bk,table,sheet

def open_xlwt():
    work_bk = xlwt.Workbook(encoding = 'utf-8')
    data = work_bk.add_sheet('data',cell_overwrite_ok = True)
    # abnormal = work_bk.add_sheet('abnormal',cell_overwrite_ok = True)
    return work_bk,data


# 创建excel表格
def openxlwt():
    wbk = xlwt.Workbook(encoding="utf-8")
    data = wbk.add_sheet("data", cell_overwrite_ok=True)
    abnormal = wbk.add_sheet("abnormal", cell_overwrite_ok=True)
    print("xlwt open success.")
    return wbk, data, abnormal


# 打开excel表格
def openxlrd(excel_file_name, name):
    wbk = xlrd.open_workbook(excel_file_name)
    table = wbk.sheet_by_name(name)
    return wbk, table


# 修改excel表格
def revisexlrd(excel_file_name, name):
    wbk_r = xlrd.open_workbook(excel_file_name)
    table = wbk_r.sheet_by_name(name)
    wbk = copy(wbk_r)
    sheet = wbk.get_sheet(name)
    return wbk, table, sheet


# 保存excel表格
def savexls(wbk, excel_file_name):
    wbk.save(excel_file_name)


# excel写入单个数据
def write_single_data(sheet, rowx, colx, data_object):
    sheet.write(rowx, colx, data_object)


# excel写入dict数据
def write_dict_data(sheet, rowx, dict):
    for key in dict.keys():
        sheet.write(rowx, key, dict[key])


# excel写入dict数据
def write_dict_other(sheet, rowx, dict):
    for key in dict.keys():
        if dict[key] > 0:
            sheet.write(rowx, key, dict[key])

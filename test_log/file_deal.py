
import win32ui
import xlwt
import xlrd
from xlutils.copy import copy

def data_result(path):
    name = 'log_analysis'
    work_bk, table = open_xlrd(path, name)
    nrows = table.nrows
    rows_list = []
    col_dic = {}
    col_key = table.row_values(0)

    for row_id in range(1,nrows):
        row_dic = {}
        row_value = table.row_values(row_id)
        for col_id in range(0,len(col_key)):
            row_dic[col_key[col_id]] = row_value[col_id]
        if row_dic['数据类型'] != 'H':
            rows_list.append(row_dic)
    # print(rows_list)

    for col_id in range(0, len(col_key)):
        col_list_temp = table.col_values(col_id)
        # print(col_list_temp)
        if col_list_temp:
            del col_list_temp[0]
            col_dic[col_key[col_id]] = col_list_temp
    temp_col_dic = table.col_values(3)
    del temp_col_dic[0]
    # print(temp_col_dic)

    for key in col_key:
        # print(key)
        for row_id in range(0,nrows-2):
            # print(row_id)
            if temp_col_dic[row_id] == 'H':
                # print(col_dic[key][row_id])
                # print(row_id)
                col_dic[key][row_id] = ''
        while '' in col_dic[key]:
            col_dic[key].remove('')

    return rows_list,col_dic

def open_xlwt():
    work_bk = xlwt.Workbook(encoding = 'utf-8')
    data = work_bk.add_sheet('data',cell_overwrite_ok = True)
    # abnormal = work_bk.add_sheet('abnormal',cell_overwrite_ok = True)
    return work_bk,data

def open_xlrd(excel_file_name,name):
    work_bk = xlrd.open_workbook(excel_file_name)
    table = work_bk.sheet_by_name(name)
    return work_bk,table

def modify_xlrd(excel_name, name):
    work_bk_r = xlrd.open_workbook(excel_name)
    table = work_bk_r.sheet_by_name(name)
    work_bk = copy(work_bk_r)
    sheet = work_bk.get_sheet(0)
    return work_bk,table,sheet

def save_excel(wook_bk,excel_name):
    wook_bk.save(excel_name)

def write_data(sheet,row,dict):
    for key in dict.keys():
        sheet.write(row,key,dict[key])





import xlrd
import win32ui
import sys
import re
import os

row_list = ['sig_name','msg_name','start_bit','sig_len','val_range','unit','formula','sta_value']
content_title = ['Tbox统一信号名称','报文名称','信号起始位','信号长度(bit)','物理值范围','单位','计算公式','车厂状态类信号']
id_title = ['报文名称','报文id','报文周期(ms)','报文长度','信号格式']

sig_len = 8
scale = ''
sig_value = ''
bo_list = []

def idToInt(id):
    intId = int(id,16)
    return intId

def sig_value_split(x):
    sig_value = ''
    if x != '':
        list_sig = str(x).strip().split('\n')
        for value in list_sig:
            if '##' in value:
                list_value = re.split('\W+',value)
                sig_value = sig_value + str(int(list_value[0].strip(),16))+' "' + list_value[1] + '" '
    else:pass


def formula_split(x):
    factor = ''
    offset = ''
    x = str(x).upper().strip()
    if x == '':
        x = 'X'
    elif 'X' not in x:
        print('shuru cuowu 的')
    else:
        if '*X' in x:
            factor = x.split('*X')[0]
            offset = x.split('*X')[1]
            if offset =='':
                offset = '0'
            elif '+' in offset:
                offset = offset.strip('+')
            else:
                pass
        else:
            factor = '1'
            offset = x.split('X')[1]
            if offset == '':
                offset = '0'
            elif '+' in offset:
                offset = offset.strip('+')
            else:
                pass
    return (factor,offset)

def scale_split(x):
    scale_min = 0
    scale_max = 0
    (factor,offset) = formula_split(scale)
    if factor ==''or offset == '':
        factor = 1
        offset = 0
    else:
        pass
    if x == '':
        scale_min = offset
        scale_max = factor * (2**sig_len) + offset
    else:
        scale_min = x.split('~')[0]
        scale_max = x.split('~')[1]
    return [scale_min,scale_max]

def openExecl(path):
    title_num = 0
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    n_rows = table.nrows
    n_cols = table.ncols
    sig_info = []
    id_info = []
    sig_cols = []
    id_cols = []
    name_to_id = {}
    id_info_row = 0
    base_path = os.path.dirname(path)
    print(base_path)
    new_dbc = base_path + '\\result\\'+ 'dbc_result'+'.dbc'
    dbc_pre1 = base_path + '\\pre_dbc\\'+ 'dbc_pre1'+'.txt'
    dbc_pre2 = base_path + '\\pre_dbc\\' + 'dbc_pre2' + '.txt'
    open_pre1 = open(dbc_pre1, 'r')
    open_pre2 = open(dbc_pre2, 'r')
    new_file = open(new_dbc,'w',encoding='utf-8')
    new_file.write(open_pre1.read()+'\n')
    new_file.write('\n'* 3)

    for i in range(0,n_rows):
        sig_len = table.row_values(i)[7]
        scale = table.row_values(i)[8]
        sig_value = table.row_values(i)[13]
        if table.row_values(i)[5] == '报文名称':
            sig_info_row = i
            for j in range(0,table.ncols):
                if table.row_values(i)[j] in content_title:
                    sig_cols.append(j)
        elif id_info_row == 0 and table.row_values(i)[2] == 'YES':
            temp_sig = []
            for index in sig_cols:
                s = table.row_values(i)[index]
                if type(s) == float:
                    s = str(int(table.row_values(i)[index]))
                temp_sig.append(s)
            sig_info.append(temp_sig)   ##sig_info 为所有信号信息集合
        elif table.row_values(i)[0] == '报文名称':
            id_info_row = i
            for j in range(0,n_cols):
                if table.row_values(i)[j] in id_title:
                    id_cols.append(j)
            for j in range(i+1,n_rows):
                type_order = 0
                tem_id = []
                name_to_id[table.row_values(j)[0]] = table.row_values(j)[1]
                for index in id_cols:
                    temp = table.row_values(j)[index]
                    if type(temp) == float:
                        temp = str(int(temp))
                    tem_id.append(temp)
                bo = 'BO_ '+ str(idToInt(tem_id[1])) + ' '+ tem_id[0] + ': ' + str(tem_id[3]) + ' Vector__XXX'
                new_file.write(bo+'\n')
                for temp_sig in sig_info:
                    if tem_id[4] == 'intel':
                        type_order = 1
                    else:type_order = 0
                    if temp_sig[1] == tem_id[0]:
                        (factor, offset) = formula_split(temp_sig[6])
                        [min_value,max_value] = scale_split(temp_sig[4])
                        sg = ' SG_ ' + temp_sig[0] + ' : ' + temp_sig[2] +'|'+ temp_sig[3] + '@'+ str(type_order) + '+' + ' (' + factor +  ',' + offset + ') '+ '[' + min_value + '|'+ max_value + '] '+'"'+temp_sig[5]+'"'+' Vector__XXX'
                        new_file.write(sg+'\n')
                new_file.write( '\n')
                id_info.append(tem_id)
                # id_info[table.row_values(j)[0]] = tem_id
                bo_list.append(bo)
    new_file.write('\n' * 3)
    new_file.write(open_pre2.read() + '\n'*2)
    for value  in id_info:
        id = str(idToInt(value[1]))
        cycle_time = 'BA_ "GenMsgCycleTime" BO_ ' + id + ' ' + value[2] + ';'
        send_type = 'BA_ "GenMsgSendType" BO_ ' + id + ' 0;'
        frame_format = 'BA_ "VFrameFormat" BO_ ' + id + ' 3;'
        new_file.write(cycle_time + '\n' + send_type + '\n' + frame_format + '\n')
    for msg_value in sig_info:
        if msg_value[7] != '':
            temp_msg = str(msg_value[7]).split('\n')
            write_line = ''
            for detail_msg in temp_msg :
                index_id = re.split('\W+',detail_msg,1)[0]
                index_id = str(index_id)
                index_id = int(index_id,16)
                content = re.split('\W+',detail_msg,1)[1]
                write_line = write_line + ' ' + str(index_id) + ' "' + content + '"'
            new_file.write('VAL_ ' + str(idToInt(name_to_id[msg_value[1]])) + ' ' + msg_value[0]  + write_line + ';')
            new_file.write('\n')
                ## temp_id = (table.row_values(j)[id_cols[0]],table.row_values(j)[id_cols[1]],table.row_values(j)[id_cols[2]],table.row_values(j)[id_cols[3]],table.row_values(j)[id_cols[4]])

# dlg = win32ui.CreateFileDialog(1)
# dlg.SetOFNInitialDir('C:\1work\T-box\Tools\dbc生成工具')
# dlg.DoModal()
#
# filename = dlg.GetPathName()
openExecl(u'C:\\1work\T-box\A_TBOX_file\huxiaoshuang\dbc_generate\江西玖发纯电动汽车_GB_协议对接表_V1.1.xlsx')
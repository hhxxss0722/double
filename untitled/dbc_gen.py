# -*- coding: utf-8 -*-
import xlrd
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import win32ui
from collections import OrderedDict

LINE = 0  # 行号
HEADERROW = 3  # 指定行索引
SIGCOL = 2  # 支持的信号—列索引
MESCOL = 0  # 报文名行
LST_MES_NAME = []  # 报文名列表
ERRORFIle = ''  # 错误报告路径


def PrintError(item, value):
    str_err = 'Error about ' + str(item) + ' = ' + str(value) + ' occurred in line: ' + str(LINE)
    print str_err
    ERRORFIle.write(str_err + '\n')


def SaveSig(sig_infor, erow):
    str_sig_infor = map(str, sig_infor)
    lst_sig_infor = ['sig_name', 'mes_name', 'startbit', 'sig_len', 'phy_scale', 'unit', 'formula', 'sig_state']
    d_sig_infor = OrderedDict(zip(lst_sig_infor, str_sig_infor))
    # print d_sig_infor
    if d_sig_infor['phy_scale'].find('~'):
        d_sig_infor['phy_scale'] = d_sig_infor['phy_scale'].split('~')

    else:  # 待添加table values情况
        pass

    raw_formula = d_sig_infor['formula']
    if d_sig_infor['formula'] == 'X':
        d_sig_infor['formula'] = [1, 0]

    # elif d_sig_infor['formula'].find(r'*X'):	#不能全字匹配
    elif r'*X' in d_sig_infor['formula']:
        d_sig_infor['formula'] = d_sig_infor['formula'].split(r'*X')
        # 此处可加入*前的数字判断
        if d_sig_infor['formula'][1] == '':
            d_sig_infor['formula'][1] = 0
        elif r'+' in d_sig_infor['formula'][1]:
            d_sig_infor['formula'][1] = d_sig_infor['formula'][1].split('+')[1]
        elif r'-' in d_sig_infor['formula'][1]:
            pass
        else:
            PrintError('formula', raw_formula)
    else:
        d_sig_infor['formula'] = d_sig_infor['formula'].split('X')
        if d_sig_infor['formula'][0] == '':
            d_sig_infor['formula'][0] = 1
        else:
            PrintError('formula', raw_formula)
        if d_sig_infor['formula'][1] == '':
            d_sig_infor['formula'][0] = 0
        elif r'+' in d_sig_infor['formula'][1]:
            d_sig_infor['formula'][1] = d_sig_infor['formula'][1].split('+')[1]
        elif r'-' in d_sig_infor['formula'][1]:
            pass
        else:
            PrintError('formula', raw_formula)

    if d_sig_infor['mes_name'] in LST_MES_NAME:
        sig_str = ' SG_ ' + d_sig_infor['sig_name'] + ' : ' + d_sig_infor['startbit'] + '|' + d_sig_infor[
            'sig_len'] + '@' + '1-' + ' (' + str(d_sig_infor['formula'][0]) + ',' + str(
            d_sig_infor['formula'][1]) + ') ' + '[' + str(d_sig_infor['phy_scale'][0]) + '|' + str(
            d_sig_infor['phy_scale'][1]) + '] "' + d_sig_infor['unit'] + '" Vector__XXX' + '\n'
        print sig_str
    else:
        LST_MES_NAME.append(d_sig_infor['mes_name'])
        mes_str = 'BO_ ' + '2566865000' + ' ' + d_sig_infor['mes_name'] + ':' + '5' + ' Vector__XXX' + '\n'
        sig_str = ' SG_ ' + d_sig_infor['sig_name'] + ' : ' + d_sig_infor['startbit'] + '|' + d_sig_infor[
            'sig_len'] + '@' + '1-' + ' (' + str(d_sig_infor['formula'][0]) + ',' + str(
            d_sig_infor['formula'][1]) + ') ' + '[' + str(d_sig_infor['phy_scale'][0]) + '|' + str(
            d_sig_infor['phy_scale'][1]) + '] "' + d_sig_infor['unit'] + '" Vector__XXX' + '\n'
        print mes_str, sig_str

    return mes_str, sig_str


class SIGNAL(object):
    is_signed = '+'
    sig_init = 0

    def __init__(self, mes_name, sig_name, start_bit, sig_len, sig_formula, phy_scale, sig_unit, value_tables):
        # lst_sig = ['sig_name', 'mes_name', 'start_bit', 'sig_len', 'phy_scale', 'sig_unit', 'sig_formula', 'sig_state']
        self.mes_name = mes_name
        self.sig_name = sig_name
        self.start_bit = start_bit
        self.sig_len = sig_len
        self.sig_formula = sig_formula
        self.phy_scale = phy_scale
        self.sig_unit = sig_unit
        self.sig_min = 0
        self.sig_max = 0
        self.value_tables = value_tables

        self.byte_order = 1  # 也可在类方法中定义、赋值
        self.factor = 1
        self.offset = 0
        # print type(self.start_bit)
        if isinstance(self.start_bit, (str, float)):
            self.start_bit = int(float(self.start_bit))
            self.sig_len = int(float(self.sig_len))
            # elif isinstance(self.start_bit,str):
            # self.start_bit = int(self.start_bit)
            # self.sig_len = int(self.sig_len)
            # else:
            # pass

            # def FormatValue(self):
            # self.start_bit = int(float(self.start_bit))
            # self.sig_len = int(float(self.sig_len))

            # return self.start_bit,self.sig_len

    def formula_split(self):
        try:
            if self.sig_formula == '':
                raw_formula = 'X'
            else:
                raw_formula = str(self.sig_formula).upper().strip()
            if 'X' in raw_formula:
                # if self.sig_formula == 'X':
                # self.factor = 1
                # self.offset = 0
                # pass
                # else:
                if r'*X' in raw_formula:
                    raw_formula = raw_formula.split(r'*X')
                    # 此处可加入*前的数字判断
                    self.factor = raw_formula[0]
                else:
                    raw_formula = raw_formula.split('X')
                    if raw_formula[0] == '':
                        self.factor = 1
                    else:
                        PrintError('factor', raw_formula[0])

                # judge offset
                if raw_formula[1] == '':
                    self.offset = 0
                elif r'+' in raw_formula[1]:
                    self.offset = raw_formula[1].split('+')[1]
                elif r'-' in raw_formula[1]:
                    self.offset = raw_formula[1]
                else:
                    PrintError('offect', raw_formula[1])
            else:
                PrintError('formula_value xx', raw_formula)
        except:
            PrintError('formula_value', self.sig_formula)

        return self.factor, self.offset

    def scale_split(self):
        self.formula_split()
        # print type(self.factor),type(self.offset)	#int or str
        if self.phy_scale == '':
            self.sig_min = self.offset
            self.sig_max = int(self.factor) * (2 ** self.sig_len) + int(self.offset)   #  ???????????
        # print self.sig_min,self.sig_max
        elif r'~' in self.phy_scale:
            raw_scale = str(self.phy_scale).strip()
            raw_scale = raw_scale.split('~')
            self.sig_min = raw_scale[0].strip()
            self.sig_max = raw_scale[1].strip()
        else:
            pass

        return self.sig_min, self.sig_max

    def starbit_conv(self):
        # self.FormatValue()
        d_sb = {0: 0, 1: 8, 2: 16, 3: 24, 4: 32, 5: 40, 6: 48, 7: 56}
        start_bit_conv = 0
        n = self.start_bit / 8
        len_c = 8 - self.start_bit % 8  # 当前起始位所在byte中所占的bit长度
        len_r = self.sig_len - len_c  # 剩余bit长度
        n1 = len_r / 8  # 剩余长度对8取整
        n2 = len_r % 8  # 剩余长度对8取余
        try:
            if n2 != 0:
                if len_r < 0:
                    n_s = n + n1 + 1
                    start_bit_conv = d_sb[n_s] + n2 - 1
                else:
                    n_s = n - n1 - 1
                    start_bit_conv = d_sb[n_s] + n2 - 1
            else:
                n_s = n - n1
                start_bit_conv = d_sb[n_s] + 7

        except:
            PrintError('Motorola: startbit and siglen', self.start_bit)

        return start_bit_conv

    def value_table_split(self, mes_id):
        lst_vts = []
        sig_vt_one = []
        sig_vt_all = []
        state_temp = ''
        index = re.compile('\W')  # 匹配任意非字母或数字字符及两边的空白字符
        if self.value_tables != '':
            lst_vts = [str(x).strip() for x in self.value_tables.split('\n')]
            # print lst_vts
            # lst_sign = [r'~', r' - ', r'——',r'--',r'—', r'–', r'=', r'：', r':']
            for single_vt in lst_vts:
                # sig_vt_one = index.split(single_vt)
                sig_vt_one = re.split(r'\W+', single_vt, 1)
                # print sig_vt_one
                # sig_vt_one.remove('')
                if len(sig_vt_one) != 2:
                    PrintError('singal state', single_vt)
                    continue
                else:
                    state_temp += str(int(str(sig_vt_one[0]), 16)) + ' "' + str(sig_vt_one[1]) + '" '

                    # sign = [y for y in lst_sign if y in single_vt]

            tail_value_table = 'VAL_ ' + str(mes_id) + ' ' + self.sig_name + ' ' + state_temp + ';' + '\n'
        # pre_value_table = 'VAL_TABLE_ ' + tail_value_table + '\r\n'

        else:
            pass

        return tail_value_table

    def write_sig(self, byte_order):
        # self.FormatValue()
        # (res_sig_min,res_sig_max) = self.scale_split()
        # (res_factor,res_offect) = self.formula_split()
        self.scale_split()
        self.formula_split()
        # print byte_order,type(byte_order)
        self.byte_order = byte_order
        if self.byte_order == 0:        #   moto？
            # start_bit_conv = abs(self.start_bit - self.sig_len)	- 1		#abs(x)返回x的绝对值
            start_bit_conv = self.starbit_conv()
        else:                           #   intel？
            start_bit_conv = self.start_bit

        # self.is_signed =
        sig_str = ' SG_ ' + self.sig_name + ' : ' + str(start_bit_conv) + '|' + str(self.sig_len) + '@' + str(
            self.byte_order) + self.is_signed + ' (' + str(self.factor) + ',' + str(self.offset) + ') ' + '[' + str(
            self.sig_min) + '|' + str(
            self.sig_max) + '] "' + self.sig_unit + '" Vector__XXX' + '\n'  # self.sig_unit.encode('gb2312')
        # print sig_str
        return sig_str


class MESSAGE(object):
    def __init__(self, mes_name, mes_id, mes_cycle, mes_len, byte_order):
        # SIGNAL.__init__(self, mes_name, sig_name, start_bit, sig_len, sig_formula, phy_scale, sig_unit)
        self.mes_name = mes_name
        self.mes_id = mes_id
        self.byte_order = byte_order

        self.mes_cycle = int(float(mes_cycle))
        self.mes_len = int(float(mes_len))

    def mes_id_conv(self):
        try:
            self.mes_id = str((int(self.mes_id, 16) & 0x1fffffff))
        except:
            PrintError('message id = ', self.mes_id)
        return self.mes_id

    def byte_order_conv(self):
        # b_order = self.byte_order.lower()
        if self.byte_order.strip().lower() == 'intel':
            self.byte_order = 1
        elif self.byte_order.strip().lower() == 'motorola':
            self.byte_order = 0
        else:
            PrintError('ByteOrder', self.byte_order)
        return self.byte_order

    # def FormatValue(self):
    # self.mes_cycle = int(float(self.mes_cycle))
    # self.mes_len = int(float(self.mes_len))
    # return self.mes_cycle,self.mes_len

    def write_mes(self):
        # self.FormatValue()
        lst_other = []
        self.mes_id_conv()
        mes_str = '\n' + 'BO_ ' + str(self.mes_id) + ' ' + self.mes_name + ': ' + str(
            self.mes_len) + ' Vector__XXX' + '\n'

        cyc_str = 'BA_ "GenMsgCycleTime" BO_ ' + str(self.mes_id) + ' ' + str(self.mes_cycle) + ';' + '\n'
        stype_str = 'BA_ "GenMsgSendType" BO_ ' + str(self.mes_id) + ' 0;' + '\n'
        vff_str = 'BA_ "VFrameFormat" BO_ ' + str(self.mes_id) + ' 3;' + '\n'

        lst_other.extend([vff_str, stype_str, cyc_str])

        return mes_str, lst_other


def InforMatch(infor):
    re_infor = {}
    str_infor = map(str, infor)
    if len(str_infor) == 8:
        lst_sig = ['sig_name', 'mes_name', 'start_bit', 'sig_len', 'phy_scale', 'sig_unit', 'sig_formula', 'sig_state']
        re_infor = OrderedDict(zip(lst_sig, str_infor))
    elif len(str_infor) == 5:
        lst_mes = ['mes_name', 'mes_id', 'mes_cycle', 'mes_len', 'byte_order']
        re_infor = OrderedDict(zip(lst_mes, str_infor))
    else:
        PrintError(str_infor, '信号或报文属性有效个数错误！')
    return re_infor


def GetLine(filename, newfile, pre_dbc_1, pre_dbc_2):
    # filename :execl file; newfile :dbc file ; pre_dbc_1:pre_dbc_1
    data = xlrd.open_workbook(filename)  # 'D:\Python27\PYTHON\dbc_generate\excelFile.xlsx'
    table = data.sheets()[1]  # 读某sheet
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    valid_sig_idex = [u'Tbox统一信号名称', u'报文名称', u'信号起始位', u'信号长度(bit)', u'物理值范围', u'单位', u'计算公式', u'车厂状态类信号']
    valid_mes_idex = [u'报文名称', u'报文id', u'报文周期(ms)', u'报文长度', u'信号格式']
    sig_col = []
    mes_col = []
    dict_sig_index = {}
    dict_mes_index = {}
    m_row = 0
    sig_obj = []
    mes_obj = []
    lst_others = []
    lst_vts = []

    newfile.write(pre_dbc_1.read())  #.dbc file
    newfile.write('\n')
    for i in xrange(0, nrows):
        global LINE
        LINE = i
        rowValues = table.row_values(i)  # 某一行数据
        if i < HEADERROW:        # HEADERROW's default value is 3
            continue
        elif i == HEADERROW:
            for j, item in enumerate(rowValues):
                # print item,j
                # if valid_sig_idex.has_key(item):
                # valid_sig_idex[item] = j
                if item.strip() in valid_sig_idex:
                    sig_col.append(j) # 保存关键数据列的索引
                else:
                    continue
                    # dict_sig_index = OrderedDict(zip(valid_sig_idex,sig_col))

        elif table.row(i)[MESCOL].value == u'报文名称':  # MESCOL 的默认值为0
            m_row = i
            for j, item in enumerate(rowValues):
                if item.strip() in valid_mes_idex:
                    mes_col.append(j) #保存关键信号id的列索引
                else:
                    continue
                    # dict_mes_index = OrderedDict(zip(valid_mes_idex,mes_col))
        else:
            lst_sig = []
            # print type(rowValues)
            if m_row == 0 and table.row(i)[SIGCOL].value == 'YES':   #  m_row 的默认值为0，SIGCOL 的默认值为2
                # for value in dict_sig_index.values():
                for value in sig_col:
                    v = int(value)
                    # print table.row(i)[v].value
                    lst_sig.append(str(table.row(i)[v].value).strip())
                # SaveSig(lst_sig,i)	#非类思想
                d_sig = InforMatch(lst_sig)
                d_sig['sig_name'] = SIGNAL(d_sig['mes_name'], d_sig['sig_name'], d_sig['start_bit'], d_sig['sig_len'],
                                           d_sig['sig_formula'], d_sig['phy_scale'], d_sig['sig_unit'],
                                           d_sig['sig_state'])
                # lst_sig = ['sig_name', 'mes_name', 'start_bit', 'sig_len', 'phy_scale', 'sig_unit', 'sig_formula', 'sig_state']
                sig_obj.append(d_sig['sig_name'])  # 信号对象列表
            # d_sig['sig_name'].write_sig()

            elif m_row != 0 and i > m_row:
                lst_mes = []
                for value in mes_col:
                    v = int(value)
                    lst_mes.append(str(table.row(i)[v].value).strip())
                d_mes = InforMatch(lst_mes)
                d_mes['mes_name'] = MESSAGE(d_mes['mes_name'], d_mes['mes_id'], d_mes['mes_cycle'], d_mes['mes_len'],
                                            d_mes['byte_order'])
                curr_mes = d_mes['mes_name']
                (mes_str, lst_other) = curr_mes.write_mes()
                newfile.write(mes_str)  # 写报文行  BO_
                lst_others.extend(lst_other)    # BA_

                curr_mes.byte_order_conv()
                for obj in sig_obj:
                    if curr_mes.mes_name == obj.mes_name:
                        sig_str = obj.write_sig(curr_mes.byte_order)
                        newfile.write(sig_str)  # 写信号行
                        if obj.value_tables != '':
                            vts_str = obj.value_table_split(curr_mes.mes_id)  # 存储value tables  VAL_
                            print vts_str
                            lst_vts.extend(vts_str)
                    else:
                        pass
            else:
                continue
    newfile.write('\n')
    newfile.write(pre_dbc_2.read())
    newfile.write('\r\n')

    for item in lst_others:
        newfile.write(item)
    for item in lst_vts:
        newfile.write(item)


def CreatPath(file1, path):
    infile = open(file1, "r")  # 打开文件
    new_folder = 'result'
    dbc_name = 'dbc_result' + '.dbc'
    err_name = 'dbc_error' + '.txt'
    pre_dbc_p1 = os.path.join(path, "pre_dbc\dbc_pre1.txt")
    print pre_dbc_p1
    pre_dbc_p2 = os.path.join(path, "pre_dbc\dbc_pre2.txt")
    print pre_dbc_p2

    new_path = os.path.join(path, new_folder)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)

    new_txt = os.path.join(new_path, dbc_name)  #.dbc file
    print 'new_txt'+ new_txt
    new_error_dir = os.path.join(new_path, err_name)

    # try:
    pre_dbc_1 = open(pre_dbc_p1, 'r')
    pre_dbc_2 = open(pre_dbc_p2, 'r')
    outfile = open(new_txt, 'w')
    errfile = open(new_error_dir, 'w')
    global ERRORFIle
    ERRORFIle = errfile

    # except:
    # PrintError('open file', 'fail!')

    GetLine(file1, outfile, pre_dbc_1, pre_dbc_2)  #file1--对接表，outfile--.dbc文件

    infile.close()  # 文件关闭
    outfile.close()
    pre_dbc_1.close()
    pre_dbc_2.close()
    errfile.close()


def ChooseFile():
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    # dlg.SetOFNInitialDir('D:/Python27/PYTHON') # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()

    filename = dlg.GetPathName()  # 获取选择的文件名称
    print '---'+ filename
    if filename == '':
        exit

    # sel_path = os.path.split(filename)[0]
    # dir_name = os.path.split(filename)[1]
    # folder_name = re.split('\.',dir_name)[0]


    sel_path = os.path.dirname(filename)
    # print sel_path
    dir_name = os.path.basename(filename)
    # print dir_name
    folder_name = os.path.splitext(dir_name)[0]
    # print folder_name
    CreatPath(filename, sel_path)


if __name__ == "__main__":
    ChooseFile()
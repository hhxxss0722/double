# -*- coding: utf-8 -*-
__author__ = 'yanshaowei'

import random
import time
import chardet

RAW_MIN = 'RAW_MIN'
RAW_MAX = 'RAW_MAX'
FACTORY_MIN = 'FACTORY_MIN'
FACTORY_MAX = 'FACTORY_MAX'
PLATFORM_MIN = 'PLATFORM_MIN'
PLATFORM_MAX = 'PLATFORM_MAX'
RANDOM = 'RANDOM'
STATRT_TIME = 0.000000

#                   0          1        2               3          4               5          6
value_mode_list = [RAW_MIN, RAW_MAX, FACTORY_MIN, FACTORY_MAX, PLATFORM_MIN, PLATFORM_MAX, RANDOM]

CMD_LINE_SUM = 2000
# MSG_PERIOD = 1

random_val_dict = {}

alarm_sig_name = 'alarm_sig_name'

GROUP_SIG_LIST = []

STATED_SIG_DISPLAY_DIC = {}

BAT_ALARM_SIG_DISPLAY_STR = 'bat_alarm_sig'

def create_asc_file(root_path, src_path_compoent, output_pre_path, dbc_list, group_infor_dic, stated_sig_display_dic):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or dbc list is error!')

    global GROUP_SIG_LIST
    GROUP_SIG_LIST = (group_infor_dic['group2list']).keys()

    global  STATED_SIG_DISPLAY_DIC
    STATED_SIG_DISPLAY_DIC = stated_sig_display_dic

    pre_f_path = root_path + '\\' + src_path_compoent + '\\' + 'asc_pre_file.asc'
    
    for dbc in dbc_list:
        output_path = output_pre_path + '\\' + dbc.file_name +'.asc'    #+ '_' + mode.lower()
        _create_asc_predix_file(pre_f_path, output_path, dbc.message_list)
        for mode in value_mode_list:            
            _create_specified_asc_file(output_path, dbc.message_list, mode)
        expect_output_path = output_pre_path + '\\' + dbc.file_name + '_expect_report.txt'
        _create_expect_report_file(expect_output_path, dbc)

    print('create asc files and expect report file success!')

def _create_asc_predix_file(pre_f_path, output_path, msg_list):
    if len(pre_f_path) == 0 or len(output_path) == 0 or len(msg_list) == 0:
        raise TypeError('pre_f_path or output_path or msg list is error!')

    target_f_path = output_path
    try:
        pre_f = open(pre_f_path, 'r')
        tar_f = open(target_f_path, 'w')

        # local_time = time.asctime(time.localtime(time.time()))
        local_time = time.asctime()
        tar_f.write('date ' + local_time + '\n')

        tar_f.write(pre_f.read())
        tar_f.write('\n')

        tar_f.close()
        pre_f.close()
    except:
        raise TypeError('operate asc_pre_file file fail!')

def _create_specified_asc_file(output_path, msg_list, value_mode):
    global STATRT_TIME
    start_time = STATRT_TIME
    target_f_path = output_path
     
    tar_f = open(target_f_path, 'a')
    cnt = 0
    msg_count = len(msg_list)
    if msg_count in range(0,11):
        Itl_per = 10.00/msg_count 
    elif msg_count in range(10,21) :
        Itl_per = 20.00/msg_count
    elif msg_count in range(20,51):
        Itl_per = 50.00/msg_count
    elif msg_count in range(50,101):
        Itl_per = 100.00/msg_count
    else:
        Itl_per = 2
    
    while cnt < CMD_LINE_SUM:
        for msg in msg_list:

            pre_str = '    ' + '{:.5f}'.format(start_time / 1000) + ' 0 ' + msg.ID[2:] + 'x' +'    Tx   d 8 '

            str1 = pre_str + _get_target_cmd_str(msg, value_mode) + '\n'
            tar_f.write(str1)

            start_time += Itl_per

        cnt += 1

    tar_f.close()
    # global STATRT_TIME
    STATRT_TIME = start_time


# get target cmd string
def _get_target_cmd_str(msg, value_mode):

    cmd_raw_min_str = '00 00 00 00 00 00 00 00'
    cmd_raw_max_str = 'FF FF FF FF FF FF FF FF'

    if value_mode == RAW_MIN:
        return cmd_raw_min_str

    if value_mode == RAW_MAX:
        return cmd_raw_max_str

    cmd_str = '00 00 00 00 00 00 00 00'

    for sig in msg.all_sig_list:
        target_v = _get_target_value(sig, value_mode)

        if target_v < 0:
            print(sig.name + ' ' + value_mode + r' mode target value is error!(%d) please check dbc file [offset] part!' % (target_v))
            target_v = 0

        cmd_str = _set_cmd_str(cmd_str, sig, target_v)

    return cmd_str

# set cmd string
def _set_cmd_str(cmd_str, sig, target_value):

    # assert target_value >= 0, 'target value is little than zero!'

    # if target_value < 0:
    #     target_value = 0

    start_bit = sig.start_bit
    length_bit = sig.length_bit
    byte_index = start_bit / 8
    ordering = sig.ordering
    byte_length = sig.get_length_byte()

    if target_value == 0:
        data_str = '0' * length_bit
    else:
        # 10 ---> 0b1010 ---> 1010
        data_str = bin(int(target_value))[2:]
        data_str = '0' * (length_bit - len(data_str)) + data_str

    prefix_zero = '0' * (start_bit % 8)
    suffix_zero = '0' * (8 - ((start_bit + length_bit - 1) % 8) - 1)

    data_bin_str = suffix_zero + data_str + prefix_zero

    if len(data_bin_str) < length_bit:
        data_bin_str = '0' * (length_bit - len(data_bin_str)) + data_bin_str

    data_bin_list = list(data_bin_str)

    data_list = []
    cnt = 0
    while cnt < byte_length:
        tt_list = data_bin_list[(cnt + 0)*8:(cnt + 1)*8]
        try:
            data = '{:0>2}'.format(str(hex(int(''.join(tt_list), 2)))[2:])
        except:
            raise Exception

        data_list.append(data)

        cnt += 1

    data_str_1 = ''.join(data_list)

    str1 = ''
    str1 += _set_full_byte(cmd_str, data_str_1, ordering, sig.get_length_byte(), byte_index)

    return str1

def _set_full_byte(cmd_str, data_str, ordering, byte_sum, byte_index):
    cmd_list = cmd_str.split(' ')
    # little endian
    # L-M-H 0x123456 L:56-byte1 M:34-byte2 H:12-byte3
    if ordering:
        i = 0
        while(i < byte_sum):
            cmd_data_str = cmd_list[byte_index + byte_sum - 1 - i]
            set_data_str = data_str[i*2 : i*2 + 2]
            try:
                cmd_data_str = '{:0>2}'.format(hex(int(cmd_data_str, 16) | int(set_data_str, 16))[2:] )
            except:
                raise TypeError('data error!')
                pass
            cmd_list[byte_index + byte_sum - 1 - i] = cmd_data_str
            i += 1
    else:
        i = 0
        while(i < byte_sum):
            cmd_data_str = cmd_list[byte_index + i]
            set_data_str = data_str[i*2 : i*2 + 2]
            try:
                cmd_data_str = '{:0>2}'.format(hex(int(cmd_data_str, 16) | int(set_data_str, 16))[2:] )
            except:
                raise TypeError('data error!')
                pass
            cmd_list[byte_index + i] = cmd_data_str
            i += 1

    return ' '.join(cmd_list)

def _set_part_of_byte(cmd_str, data_str, start_bit, length_bit):
    cmd_list = cmd_str.split(' ')
    byte_index = start_bit / 8

    data = cmd_list[byte_index]

    result = '{:0>2}'.format(hex(int(data, 16) | int(data_str, 16))[2:] )

    cmd_list[byte_index] = result

    return ' '.join(cmd_list)

# get target value
def _get_target_value(sig, mode):

    if mode == FACTORY_MIN:
        return _get_factory_min_corr_raw_val(sig)
    elif mode == FACTORY_MAX:
        return _get_factory_max_corr_raw_val(sig)
    else:
        if mode == PLATFORM_MIN:
            return _get_platform_min_corr_raw_val(sig)
        elif mode == PLATFORM_MAX:
            return _get_platform_max_corr_raw_val(sig)
        elif mode == RANDOM:
            return _get_random_val(sig)
        else:
            raise TypeError('value mode is error!')
    pass

def _get_factory_min_corr_raw_val(sig):
    value  = (sig.min_val - sig.offset) / sig.scale
    return int(value)

def _get_factory_max_corr_raw_val(sig):
    value  = (sig.max_val - sig.offset) / sig.scale
    return int(value)

def _get_platform_min_corr_raw_val(sig):
    formula = sig.formula
    dis_value = formula.min_val * formula.scale + formula.offset

    if (formula.length * 8) <= sig.length_bit:
        value  = (dis_value - sig.offset) / sig.scale
        if value >= 0:
            return int(value)
    elif dis_value < 0:
        pass
    else:
        pass

    return _get_factory_min_corr_raw_val(sig)

def _get_platform_max_corr_raw_val(sig):
    formula = sig.formula
    if (formula.length * 8) <= sig.length_bit:
        dis_value = formula.max_val * formula.scale + formula.offset
        value  = (dis_value - sig.offset) / sig.scale
        return int(value)
    else:
        return _get_factory_max_corr_raw_val(sig)


def _get_random_val(sig):
    formula = sig.formula
    if random_val_dict.has_key(sig.name):
        return random_val_dict[sig.name]

    f_min_raw = _get_factory_min_corr_raw_val(sig)
    f_max_raw = _get_factory_max_corr_raw_val(sig)

    p_min_raw = _get_platform_min_corr_raw_val(sig)
    p_max_raw = _get_platform_max_corr_raw_val(sig)

    if f_min_raw >= p_min_raw:
        min_v = f_min_raw
    else:
        min_v = p_min_raw

    if f_max_raw >= p_max_raw:
        max_v = p_max_raw
    else:
        max_v = f_max_raw

    max_v /= 3

    if max_v < min_v:
        min_v = max_v + min_v
        max_v = min_v - max_v
        min_v = min_v - max_v

    try:
        random_v = random.randint(min_v, max_v)
    except:
        raise TypeError('get random value fail!')

    dic = {sig.name: random_v}

    random_val_dict.update(dic)

    return random_v

def _create_expect_report_file(expect_output_path, dbc):
    try:
        tar_f = open(expect_output_path, 'w')
    except:
        raise TypeError('open expect_output_path failed')

    raw_min_except_list = []
    raw_max_except_list = []
    facotry_min_except_list = []
    facotry_max_except_list = []
    platform_min_except_list = []
    platform_max_except_list = []
    random_except_list = []

    for msg in dbc.message_list:
        for sig in msg.all_sig_list:
            formula = sig.formula
            if formula == None:
                raise TypeError('get corresponding formula fail!')

            display_name = sig.zh_name

            x = type(display_name)

            display_name.encode('utf-8')

            raw_min_except_list.append(_get_raw_min_except_str(sig, display_name))
            raw_max_except_list.append(_get_raw_max_except_str(sig, display_name))
            facotry_min_except_list.append(_get_facotry_min_except_str(sig, display_name))
            facotry_max_except_list.append(_get_facotry_max_except_str(sig, display_name))
            platform_min_except_list.append(_get_platform_min_except_str(sig, display_name))
            platform_max_except_list.append(_get_platform_max_except_str(sig, display_name))
            random_except_list.append(_get_random_except_str(sig, display_name))
            
    str1 = '*********************'.decode('utf-8')

    raw_min_except_list.insert(0, u'raw min except value   ' + str1 + '\n')
    raw_max_except_list.insert(0, u'raw max except value   ' + str1 + '\n')
    facotry_min_except_list.insert(0, u'factory min except value   ' + str1 + '\n')
    facotry_max_except_list.insert(0, u'factory max except value   ' + str1 + '\n')
    platform_min_except_list.insert(0, u'platform min except value   ' + str1 + '\n')
    platform_max_except_list.insert(0, u'platform max except value   ' + str1 + '\n')
    random_except_list.insert(0, u'random except value   ' + str1 + '\n')

    tar_f.write(''.join(raw_min_except_list).encode('gbk'))
    tar_f.write(''.join(raw_max_except_list).encode('gbk'))
    tar_f.write(''.join(facotry_min_except_list).encode('gbk'))
    tar_f.write(''.join(facotry_max_except_list).encode('gbk'))
    tar_f.write(''.join(platform_min_except_list).encode('gbk'))
    tar_f.write(''.join(platform_max_except_list).encode('gbk'))
    tar_f.write(''.join(random_except_list).encode('gbk'))

    tar_f.close()

split_str = ' ------------ '

def _get_raw_min_except_str(sig, display_name):
    corr_data = 0
    str1 = ''

    try:
        str2 = _get_display_val(corr_data, sig)
        str1 = '\t' + display_name + split_str + str(hex(corr_data)) + split_str + str2 + '\n'
    except:
        pass

    return str1

def _get_raw_max_except_str(sig, display_name):
    val = int('{:1>32}'.format('')[(32 - sig.length_bit):], 2)

    str1 = '\t' + display_name + split_str + str(hex(val)) + split_str + _get_display_val(val, sig ) + '\n'

    return str1

def _get_facotry_min_except_str(sig, display_name):
    val = _get_factory_min_corr_raw_val(sig)

    str1 = ''
    try:
        str1 = '\t' + display_name + split_str + str(hex(val)) + split_str + _get_display_val(val, sig ) + '\n'
    except:
        strr = _get_display_val(val, sig )

    return str1

def _get_facotry_max_except_str(sig, display_name):
    val = _get_factory_max_corr_raw_val(sig)
    str1 = '\t' + display_name + split_str + str(hex(val)) + split_str + _get_display_val(val, sig ) + '\n'

    return str1

def _get_platform_min_except_str(sig, display_name):
    val = _get_platform_min_corr_raw_val(sig)
    str1 = '\t' + display_name + split_str + str(hex(val)) + split_str + _get_display_val(val, sig ) + '\n'

    return str1

def _get_platform_max_except_str(sig, display_name):
    val = _get_platform_max_corr_raw_val(sig)
    str1 = '\t' + display_name + split_str + str(hex(val)) + split_str + _get_display_val(val, sig ) + '\n'

    return str1

def _get_random_except_str(sig, display_name):
    try:
        data = random_val_dict[sig.name]
    except:
        print('get random value fail!')

    str1 = '\t' + display_name + split_str + str(hex(data)) + split_str + _get_display_val(data, sig ) + '\n'

    return str1

# def _get_display_name(sig):
#     return name

def _get_display_val(data, sig):

    formula = sig.formula
    # real value
    val = data * sig.scale + sig.offset

    plat_corr_max_v = formula.max_val * formula.scale + formula.offset
    plat_corr_min_v = formula.min_val * formula.scale + formula.offset

    sig_corr_max_v = sig.max_val
    sig_corr_min_v = sig.min_val

    formula_unit = formula.unit
    sig_unit = sig.unit

    unit = sig_unit

    str1 = sig.get_unit_transition()
    if len(str1) > 0:
        val = float(str1) * float(val)
        sig_corr_max_v = float(str1) * float(sig_corr_max_v)
        sig_corr_min_v = float(str1) * float(sig_corr_min_v)
        unit = formula_unit

    prefix = ''
    if val < sig_corr_min_v or val > sig_corr_max_v:
        prefix = unicode('无效', 'utf-8')

    if (val < plat_corr_min_v and val >= sig_corr_min_v) \
        or (val > plat_corr_max_v and val <= sig_corr_max_v):
        prefix = unicode('异常', 'utf-8')

    if sig.is_state_sig:
        stated_suffix_str = ''
        key_list = STATED_SIG_DISPLAY_DIC.keys()
        if sig.name in key_list:
            stated_suffix_str = STATED_SIG_DISPLAY_DIC[sig.name]

        if sig.is_bat_alarm_sig:
            stated_suffix_str = STATED_SIG_DISPLAY_DIC[BAT_ALARM_SIG_DISPLAY_STR]

        dic = sig.get_display_dict()
        key = str(int(data))

        str1 = ''
        if key in dic.keys():
            str1 = dic[key]
        else:
            # return str(hex(int(data)))
            str1 = unicode('无效', 'utf-8')

        if len(stated_suffix_str) > 0:
            return str1 + '\t PLAT:' + stated_suffix_str
        else:
            return str1

    platform_range_str  = 'PLAT->FACTORY:[' + str(plat_corr_min_v) + ', ' + str(plat_corr_max_v) + ' ' + formula_unit +']'

    try:
        sig_range_str       = 'FACTORY:[' + str(sig.min_val) + ', ' + str(sig.max_val) + ' ' + sig.unit + ']'
    except:
        x = chardet.d
        pass

    if len(prefix) > 0:
        return  prefix + '\t(' + '{:.3f}'.format(val) + ' ' + unit +')\t' + sig_range_str + '\t' + platform_range_str
    else:
        return '(' + '{:.3f}'.format(val) + ' ' + unit + ')\t' + sig_range_str + '\t' + platform_range_str

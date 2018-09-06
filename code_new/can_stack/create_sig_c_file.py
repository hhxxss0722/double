# -*- coding: utf-8 -*-
'''create_sig_c_file module'''

import operator
from public.utility import *

type_value_dict =\
{
    'uint8_t':'u8Value',
    'uint16_t':'u16Value',
    'uint32_t':'u32Value',
    'uint64_t':'u64Value'
}

type_to_invalid_dict =\
{
    'uint8_t':'INVALID_UINT8',
    'uint16_t':'INVALID_UINT16',
    'uint32_t':'INVALID_UINT32',
    'uint64_t':'INVALID_UINT32' # use 32bit max value as 64bit max value
}

# only jx platform
motor_gear_str = 'motor_gear'
brake_gear_str = 'brake_gear'
driver_gear_str = 'driver_gear'

_gb_highest_alarm_level_str = 'highest_alarm_level'

different_unit_list = []

exist_sig_name_list = []
exist_sig_list = []

NOT_GROUP_IN_GROUP_STYLE = 0
# g in g main fun
GROUP_IN_GROUP_STYLE_1 = 1
# g in g sub fun
GROUP_IN_GROUP_STYLE_2 = 2

VALID_SIG_NAME_LIST = []

GROUP_TO_LIST = {}
MULTI_G_NAME_LIST = []

PLATFORM_MODE = ''


def create_sig_c_file(sig_c_src_path_prefix, sig_c_output_path, dbc_list, valid_sig_name_list, different_unit_path,
                      platform_mode, group_infor_dic):
    if len(dbc_list) == 0 or len(group_infor_dic) == 0:
        print('***********************ERROR!***********************')
        print_cur_info()
        quit(1)

    global PLATFORM_MODE
    PLATFORM_MODE = platform_mode

    global VALID_SIG_NAME_LIST
    VALID_SIG_NAME_LIST = valid_sig_name_list

    global GROUP_TO_LIST
    GROUP_TO_LIST = group_infor_dic['group2list']

    global MULTI_G_NAME_LIST
    MULTI_G_NAME_LIST = group_infor_dic['multi_g_name_list']

    target_sig_f_path = sig_c_output_path

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name
    
    try:
        tar_f = open(target_sig_f_path, 'w')

    except:
        raise TypeError('operate sig.c file fail!')

    str1 = r'#include "canstack_conf.h"'+'\n'
    str1 += r'#include "canstack_sig.h"'+'\n'
    str1 += r'#include "dat_man.h"'+'\n\n'
    str1 += '#ifdef CANSTACK_' + valid_file_name.upper() + '\n'
    str1 += '#include "canstack_' + valid_file_name.upper() + '_msg.h"\n\n'
    tar_f.write(str1)

    message_list = []

    # get message list set
    for dbc in dbc_list:
        message_list += dbc.message_list

        str1 = '/**************************CAN_' + str(dbc.can_channel) + '**************************/\n'
        tar_f.write(str1)
        # vehicle sig define
        for message in dbc.message_list:
            str1 = '/* ' + message.name + ':'+ message.ID + ' */\n'
            str1 += '#define CAN_' + message.name.upper() + '_DATA_ARRAY\t\t\t' + 'canstack_message_array' + str(dbc.can_channel) + '[' + message.name.upper() + '].p_u8Data\n'
            str1 += '#define CAN_' + message.name.upper() + '_OUTIND\t\t\t' + 'canstack_message_array' + str(dbc.can_channel) + '[' + message.name.upper() + '].outind'
            str1 += '\n\n'

            tar_f.write(str1)

    general_alarm_sig_list = []

    for message in message_list:

        general_alarm_sig_list += message.alarm_sig_list

        for sig in message.sig_list:

            exist_sig_list.append(sig)

            if False == _judge_and_save_sig_group(sig):
                exist_sig_name_list.append(sig.name)

                # CANSTACK_SET_SIG_BODY(bat_soc) {}
                str1 = _create_set_sig_body(sig)

                tar_f.write(str1)

    tar_f.write('\n')

    # write group sig's fun body
    # like CANSTACK_GET_GROUP_SIG_FUN_BODY(bat_cell_volt, 0) and CANSTACK_SET_SIG_BODY(bat_cell_volt)
    _write_group_sig_fun_body(tar_f)

    if _gb_highest_alarm_level_str not in exist_sig_name_list:
        # highest_alarm_level function must exist
        str1 = '\nCANSTACK_SET_SIG_BODY(highest_alarm_level);\n'
        tar_f.write(str1)

    remain_sig_name_list = set(valid_sig_name_list) - set(exist_sig_name_list)

    if len(remain_sig_name_list) > 0:
        # create remain sig's SET_SIGNAL fun body. like:CANSTACK_SET_SIG_BODY(invalid_sig)
        str1 = '/* get invalid_sig\'s value */\n'
        str1 += 'CANSTACK_SET_SIG_BODY(invalid_sig)\n'
        str1 += '{return FLOAT_MAX_VALUE;}\n\n'
        tar_f.write(str1)

    # create sig_infor_t sig_infor_array[]
    str1 = _create_sig_infor_array(valid_sig_name_list, remain_sig_name_list)
    tar_f.write(str1)

    # add suffix content
    sig_suffix_f_path = sig_c_src_path_prefix + '\\' + 'canstack_xxx_sig_c_suffix.c'
    try:
        pre_f = open(sig_suffix_f_path, 'r')
        tar_f.write(pre_f.read())

        pre_f.close()
    except:
        raise TypeError('operate sig.c suffix file fail!')

    tar_f.write('\n\n')

    str1 = _create_deal_error_status_fun(message_list)

    tar_f.write(str1)

#     if platform_mode == 'gb_platform':
#         str1 = _create_gb_code2index(general_alarm_sig_list)
#         tar_f.write(str1)

    tar_f.write('\n#endif\n')
    tar_f.close()

    if len(different_unit_list) != 0:
        str1 = '\n'.join(different_unit_list)

        d_f = open(different_unit_path, 'w')
        d_f.write(str1.encode('gbk'))
        d_f.close()
    else:
        d_f = open(different_unit_path, 'w')
        d_f.write('此地无银三百两。\n\t\t---匿名者留言')
        d_f.close()

    print('create sig.c file success!')

# write group sig's fun body
# like CANSTACK_GET_GROUP_SIG_FUN_BODY(bat_cell_volt, 0) and CANSTACK_SET_SIG_BODY(bat_cell_volt)
def _write_group_sig_fun_body(tar_f):

    # if not platform_mode in platform_group_sig_man_dic.keys():
    #     print('[%s] mode is not found!' % platform_mode)
    #     print_cur_info()
    #     quit(1)

    prefix_str_list = GROUP_TO_LIST.keys()

    for prefix_str in prefix_str_list:
        if len(GROUP_TO_LIST[prefix_str]) > 0:
            if not prefix_str in MULTI_G_NAME_LIST:
                str1 = ''
                str1 += _create_get_group_sig_fun_body(GROUP_TO_LIST[prefix_str], prefix_str)
                str1 += _create_set_sig_body_for_group(GROUP_TO_LIST[prefix_str], prefix_str)
                tar_f.write(str1)
            else:
                str1 = ''
                str1 += _create_set_g_in_g_sig_fun_body(GROUP_TO_LIST[prefix_str], prefix_str)
                tar_f.write(str1)

    return True

# group in group sig fun body
def _create_set_g_in_g_sig_fun_body(sig_list, valid_name):

    name_list = []
    for sig in sig_list:
        name_list.append(sig.name)

    # delete last '_'
    # sig_x_y ---> sig_x
    new_name_list = []
    for name in name_list:
        name = name[:name.rfind('_')]
        new_name_list.append(name)

    name_set = set(new_name_list)

    new_name_list = list(name_set)
    new_name_list.sort()

    # temp_x:[temp_x_1...]
    x_l = []
    for x in new_name_list:
        x_l.append([])

    name2sig_dic = dict(zip(new_name_list, x_l))

    for name in new_name_list:
        for sig in sig_list:
            sig_name = sig.name
            if sig_name.startswith(name):
                (name2sig_dic[name]).append(sig)

    str1 = ''
    # create g in g impletement fun
    # create g in g sub fun
    for name in new_name_list:
        str1 += _create_get_group_sig_fun_body(name2sig_dic[name], name)
        str1 += _create_set_sig_body_for_group([], name, GROUP_IN_GROUP_STYLE_2, len(name2sig_dic[name]))

    # create g in g main fun
    str1 += _create_set_sig_body_for_group([], valid_name, GROUP_IN_GROUP_STYLE_1, len(name_set))

    return str1

# judge and save sig group
def _judge_and_save_sig_group(sig):

    # if not platform_mode in platform_group_sig_man_dic.keys():
    #     print('[%s] mode is not found!' % platform_mode)
    #     print_cur_info()
    #     quit(1)

    prefix_str_list = GROUP_TO_LIST.keys()

    for prefix_str in prefix_str_list:
        if sig.name.startswith(prefix_str):
            exist_sig_name_list.append(prefix_str)
            GROUP_TO_LIST[prefix_str].append(sig)

            return True

    return False

# create get group sig fun body
def _create_get_group_sig_fun_body(sig_list, valid_name):
    str1 = ''
    sig_list.sort(key = lambda Sig: Sig.suffix_num, reverse = False)

    sum = len(sig_list)
    cnt = 0

    while cnt < sum:
        sig = sig_list[cnt]
        str1 += _create_set_sig_body(sig, str(cnt + 1), valid_name)
        cnt += 1

    return str1


# create set sig boy for "group" sig. like:CANSTACK_SET_SIG_BODY(bat_cell_volt)
def _create_set_sig_body_for_group(sig_list, valid_name, group_style = NOT_GROUP_IN_GROUP_STYLE, group_sum = 0):

    if group_sum == 0:
        # sig_list.sort(key = operator.attrgetter('suffix_num'), reverse = False)
        sig_list.sort(key = lambda Sig: Sig.suffix_num, reverse = False)
        sum = len(sig_list)
    else:
        sum = group_sum

    cnt = 0
    str1 = \
'''\
/* get %(valid_name)s value */
CANSTACK_SET_GROUP_BODY(%(valid_name)s)
{
    float fValue = 0.0;
    %(init_str)s

    switch(%(index)s)
    {
'''
    dic = \
        {
            'valid_name': valid_name,
            'init_str': 'uint8_t index = *(uint8_t *)param;',
            'index': 'index',
        }

    if group_style == GROUP_IN_GROUP_STYLE_1:
        dic['init_str'] = 'uint8_t* pi = (uint8_t *)param;'
        dic['index'] = 'pi[0]'

    if group_style == GROUP_IN_GROUP_STYLE_2:
        dic['init_str'] = 'uint8_t* pi = (uint8_t *)param;'
        dic['index'] = 'pi[1]'

    str1 = str1 % dic

    while cnt < sum:
        str1 += '\t\tcase ' + str(cnt) + ':\n'

        if group_style == NOT_GROUP_IN_GROUP_STYLE:
            str2 = '\t\t\tfValue = CANSTACK_GET_GROUP_SIG(' + valid_name + ', ' + str(cnt + 1) + ');' + '/* ' + (sig_list[cnt]).name + ' */\n'
        elif group_style == GROUP_IN_GROUP_STYLE_1:
            str2 = '\t\t\tfValue = CANSTACK_SET_GROUP_FOR_X(' + valid_name + ', ' + str(cnt + 1) + ');' + '/* ' + valid_name + '_' + str(cnt + 1) + ' */\n'
        elif group_style == GROUP_IN_GROUP_STYLE_2:
            str2 = '\t\t\tfValue = CANSTACK_GET_GROUP_SIG(' + valid_name + ', ' + str(cnt + 1) + ');' + '/* ' + valid_name + '_' + str(cnt + 1) + ' */\n'
        else:
            raise TypeError('error!')

        str1 += str2

        str1 += '\t\tbreak;\n'
        cnt += 1

    str1 += '\t\tdefault:\n'
    str1 += '\t\t\tfValue = FLOAT_MAX_VALUE;\n'
    str1 += '\t\tbreak;\n'
    str1 += '\t}\n'

    str1 += '\treturn fValue;\n'

    str1 += '}\n'

    return str1

# get sig with name
def _get_sig_with_name(sig_list, name):
    for sig in sig_list:
        if name == sig.name:
            return sig
        elif sig.name.startswith(name):
            return sig
        else:
            pass

    return None

# sig_infor_t sig_infor_array[]
def _create_sig_infor_array(valid_sig_name_list, remain_sig_name_list):

    remain_sig_name_list_temp = list(remain_sig_name_list)
    exist_sig_list_temp = exist_sig_list[:]

    special_str = ''

    if PLATFORM_MODE == 'gb_platform':
        if _gb_highest_alarm_level_str in exist_sig_list:
            pass
        elif _gb_highest_alarm_level_str in remain_sig_name_list_temp:
            remain_sig_name_list_temp.remove(_gb_highest_alarm_level_str)
            special_str = _gb_highest_alarm_level_str
        else:
            special_str = _gb_highest_alarm_level_str

    # sig_infor_t sig_infor_array[]
    str1 = 'sig_infor_t sig_infor_array[] =\n'
    str1 += '{\n'

    for name in valid_sig_name_list:
        if name in remain_sig_name_list_temp:
            str1 += '\t{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},\t/* ' + name + ' */\n'
        elif len(special_str) > 0 and name == special_str:
            str1 += '\t{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(' + name + ')},\t/* ' + name + ' */\n'
        else:
            sig = _get_sig_with_name(exist_sig_list, name)
            if sig == None:
                sig = _get_sig_with_name(exist_sig_list, name + '_1')
                if sig == None:
                    raise TypeError('sig name error!')

            str1 += '\t{ ' + type_to_invalid_dict[sig.get_data_type()] + ', CANSTACK_SET_SIG_FUN_NAME(' + name + ')},\t/* ' + name + ' */\n'

    str1 += '\n};\n'
    return str1

# CANSTACK_SET_SIG_BODY(bat_soc) {}
def _create_set_sig_body(sig, index_str = None, valid_name = None):
    # ((canstack_msg_data_t *)(CAN_VEHICLE_INFOR_DATA_ARRAY))->vehicle_infor.
    data_type_pre = '((canstack_msg_data_t *)CAN_' + sig.parent_message.name.upper() + '_DATA_ARRAY)->' + sig.parent_message.name + '.' + sig.name
    
    byte_flag = ''
    if sig.length_bit in range(1,9):
        byte_flag = 'FLOAT_MAX_BYTEVALUE'
    elif sig.length_bit in range(9,17):
        byte_flag = 'FLOAT_MAX_WORDVALUE'
    else:
        byte_flag = 'FLOAT_MAX_DWORDVALUE'
    
    str1 = ''
    str1 += '/* get ' + sig.name + ' value */\n'

    if index_str == None:
        str1 += 'CANSTACK_SET_SIG_BODY(' + sig.name + ')\n'
    else:
        str1 += 'CANSTACK_SET_GROUP_SIG_BODY(' + valid_name + ', ' + index_str + ')\n'

    str1 += '{\n'
    str1 += '\tfloat fValue = 0.0;\n'
    str1 += '\tuint32_t u32Value = 0;\n'
    str1 += '\t' + 'unData_type unData;\n'
    str1 += '\t' + 'unData.u32Data = 0;\n\n'
    str1 += '\tif(CAN_' + sig.parent_message.name.upper() + '_OUTIND)\n'
    str1 += '\t{return '+ byte_flag + ';}\n\n'
    # str1 += '\t' + type_value_dict[sig.get_data_type()] + ' = '

    assumption_len = sig.length_bit + (sig.start_bit % 8)
    assumption_byte = assumption_len / 8
    if (assumption_len % 8) > 0:
        assumption_byte += 1

    count1 = 0
    sum = assumption_byte

    if sum == 1:
        str1 += '\tunData.u8DataArray' + '[' + str(count1) + '] = ' + data_type_pre + ';\n'
    else:
        while count1 < sum:
            str1 += '\tunData.u8DataArray' + '[' + str(count1) + '] = ' + data_type_pre + '_' +str(assumption_byte) + ';\n'
            assumption_byte -= 1
            count1 += 1

    str1 += '\n\tu32Value = unData.u32Data;\n'

    if not sig.isSigned:
        str1 += '\t' + 'fValue = (float)(u32Value);\n\n'
    else:
        str1 += '\t/* judge signed value */\n'
        str1 += '\t' + 'if( (unData.u8DataArray[' + str(sig.get_length_byte() - 1) + '] & 0x80) == 0x80)\n'
        str1 += '\t' +'{' + '\n'
        str1 += '\t\t' + 'u32Value = (~u32Value);\n'
        str1 += '\t\t' + 'u32Value += 1;\n\n'
        str1 += '\t\t' + 'fValue = (float)(u32Value);\n'
        str1 += '\t\t' + 'fValue = (0 - fValue);\n'
        str1 += '\t' + '}' + '\n\n'

    if sig.scale != 1:
        str1 += '\tfValue *= ' + str(sig.scale) + ';\n'

    if sig.offset != 0:
        str1 += '\tfValue += ' + str(sig.offset) + ';\n\n'
    # min value is bigger than max value
    if sig.min_val > sig.max_val:
        print('-------------------------ERROR!-------------------------')
        print('[%s] min value is bigger than max value!' % sig.name)
        print_cur_info()
        quit(1)

    str1 += '\tif((fValue < ' + str(sig.min_val) + ') || (fValue > ' + str(sig.max_val) + '))\n'
    str1 += '\t{return '+ byte_flag + ';}\n'

    str2 = _unit_transition(sig)
    if len(str2) > 0:
        str1 += '\n\t//unit transition\n'
        str1 += '\tfValue *= ' + str2 + ';\n'

    if sig.is_state_sig and not sig.is_alarm_sig:
        dic = sig.get_state_dict()

        key_list = dic.keys()
        key_list.sort()

        str1 += '\n'
        for key in key_list:
            str1 += '\t' + 'if(fValue == ' + key + ' ) {return ' + dic[key] + ';}\n\n'

        # str1 += '\n\t//we only care \'valid\' parts'
        str1 += '\n\treturn '+ byte_flag + ';\n'
        str1 += '}\n'

        # if sig is stated return str1
        return str1

    str1 += '\n\treturn fValue;\n'
    str1 += '}\n'

    return str1

def _unit_transition(sig):

    formula = sig.formula
    formula_unit = formula.unit.upper()
    sig_unit = sig.unit.upper()

    formula_unit_str = formula.unit
    sig_unit_str = sig.unit

    if formula_unit_str == sig_unit_str:
        return ''

    str1 = 'plat:\t' + formula.sig_name + ' unit: ' + formula_unit_str + '\t<------>\t' + 'factory:\t'  + sig.name + ' unit: ' + sig_unit_str
    different_unit_list.append(str1)

    return sig.get_unit_transition()

def _create_deal_error_status_fun(msg_list):
    # create deal error status fun
    str1 = '/******************deal error status*******************/\n'

    str2 = \
r'''
#define ALARM_LEVEL_0   0
#define ALARM_LEVEL_1   1
#define ALARM_LEVEL_2   2
#define ALARM_LEVEL_3   3       // coresspond gb protocol highest alarm level

#define DEAL_OTHER_ERR(raw_val, level_0, level_1, level_2, level_3, alarm_level, errData) \
                            if( raw_val == level_0) \
                            { \
                                dat_gb_clear_other_err(errData);    \
                                alarm_level = ALARM_LEVEL_0;    \
                            } \
                            else if( raw_val == level_1) \
                            { \
                                dat_gb_add_other_err(errData);  \
                                alarm_level = ALARM_LEVEL_1;    \
                            } \
                            else if( raw_val == level_2) \
                            { \
                                dat_gb_add_other_err(errData);  \
                                alarm_level = ALARM_LEVEL_2;    \
                            } \
                            else if( raw_val == level_3) \
                            { \
                                dat_gb_add_other_err(errData);  \
                                alarm_level = ALARM_LEVEL_3;    \
                            } \
                            else \
                            {   \
                                dat_gb_clear_other_err(errData);    \
                                alarm_level = ALARM_LEVEL_0;    \
                            }

#define DEAL_BAT_ERR(raw_val, level_0, level_1, level_2, level_3, alarm_level, errData) \
                            if( raw_val == level_0) \
                            { \
                                dat_gb_clear_batalarm_err(errData); \
                                alarm_level = ALARM_LEVEL_0;    \
                            } \
                            else if( raw_val == level_1) \
                            { \
                                dat_gb_add_batalarm_err(errData);   \
                                alarm_level = ALARM_LEVEL_1;    \
                            } \
                            else if( raw_val == level_2) \
                            { \
                                dat_gb_add_batalarm_err(errData);   \
                                alarm_level = ALARM_LEVEL_2;    \
                            } \
                            else if( raw_val == level_3) \
                            { \
                                dat_gb_add_batalarm_err(errData);   \
                                alarm_level = ALARM_LEVEL_3;    \
                            } \
                            else \
                            {   \
                                dat_gb_clear_batalarm_err(errData); \
                                alarm_level = ALARM_LEVEL_0;    \
                            }
'''

    dic = { \
            'add_other_err': 'dat_add_other_err',
            'clear_other_err': 'dat_clear_other_err',
            'add_bat_err': 'dat_add_batalarm_err',
            'clear_bat_err': 'dat_clear_batalarm_err',
        }

    if PLATFORM_MODE == 'gb_platform':
        dic = { \
                'add_other_err': 'dat_gb_add_other_err',
                'clear_other_err': 'dat_gb_clear_other_err',
                'add_bat_err': 'dat_gb_add_batalarm_err',
                'clear_bat_err': 'dat_gb_clear_batalarm_err',
            }

    str1 += str2 % dic

    str1 += '/* deal default msg error status fun */\n'
    str1 += 'void deal_default_msg_error_status(cuint8_t *p_u8Data)\n'
    str1 += '{}\n\n'

    fun_prefix_str = 'void deal_'
    fun_suffix_str = '_error_status(cuint8_t *p_u8Data)'
    statement_prefix = 'data = ((canstack_msg_data_t *)CAN_'
    fun_comment_prefix_str = '/* deal '
    fun_comment_suffix_str = ' error status fun */'

    alarm_arr_suffix_str = '_ala_arr'
    alarm_arr_sum_suffix_str = '_ala_sum'

    have_alarm_sig_msg_list = []

    for msg in msg_list:
        if msg.alarm_sig_sum > 0:
            have_alarm_sig_msg_list.append(msg)

            msg_alarm_arr_str = msg.name + alarm_arr_suffix_str
            msg_alarm_sum_str = msg.name + alarm_arr_sum_suffix_str

            str1 += 'uint8_t ' + msg_alarm_arr_str + '[' + str(msg.alarm_sig_sum) + '] = { 0 };\n'
            str1 += 'uint8_t ' + msg_alarm_sum_str + ' = ' + str(msg.alarm_sig_sum) + ';\n\n'
            str1 += fun_comment_prefix_str + msg.name + '(' + msg.ID + ')' +fun_comment_suffix_str + '\n'
            str1 += fun_prefix_str + msg.name + fun_suffix_str + '\n'
            str1 += '{\n'
            str1 += '\tuint8_t data = 0xff;\n\n'

            cnt = 0
            # deal alarm sig with dtc
            for sig in msg.alarm_sig_list:
                str1 += '\t' + statement_prefix + msg.name.upper() + '_DATA_ARRAY)->' + msg.name + '.' + sig.name + ';\n'


                temp_dic = sig.get_alarm_level_dic()

                if temp_dic == None:
                    print('---------------- error! ----------------\n[%s] alarm data config error! please dbc file.' % sig.name)
                    print_cur_info()
                    quit(1)

                str1 += '\t' + 'DEAL_OTHER_ERR(data' + ', ' + temp_dic['level_0'] + ', ' + temp_dic['level_1'] \
                        + ', ' + temp_dic['level_2'] + ', ' + temp_dic['level_3'] + ', ' + msg_alarm_arr_str \
                        + '[' + str(cnt) + ']' + ', ' + str(hex(int(temp_dic['dtc']))) + ');\n'

                str1 += '\n'

                cnt += 1
            # deal alarm sig without dtc
            for sig in msg.bat_alarm_sig_list:
                str1 += '\t' + statement_prefix + msg.name.upper() + '_DATA_ARRAY)->' + msg.name + '.' + sig.name + ';\n'

                temp_dic = sig.get_alarm_level_dic()

                if temp_dic == None:
                    print('---------------- error! ----------------\n[%s] alarm data config error! please dbc file.' % sig.name)
                    print_cur_info()
                    quit(1)

                str1 += '\t' + 'DEAL_BAT_ERR(data' + ', ' + temp_dic['level_0'] + ', ' + temp_dic['level_1'] \
                        + ', ' + temp_dic['level_2'] + ', ' + temp_dic['level_3'] + ', ' + msg_alarm_arr_str \
                        + '[' + str(cnt) + ']' + ', ' + sig.name + ');\n'

                str1 += '\n'

                cnt += 1

            str1 += '}\n\n'
    # platform is gb platform and highest_alarm_level sig is not exist
    if PLATFORM_MODE == 'gb_platform' and _gb_highest_alarm_level_str not in exist_sig_name_list:
        str1 += 'CANSTACK_SET_SIG_BODY(' + _gb_highest_alarm_level_str + ')\n'
        str1 += '{\n'
        str1 += '\tuint8_t i = 0;\n'
        str1 += '\tuint8_t alarm_level = ALARM_LEVEL_0;\n\n'

        if len(have_alarm_sig_msg_list) > 0:
            for msg in have_alarm_sig_msg_list:
                str1 += '\tfor (i = 0; i < ' + msg.name + alarm_arr_sum_suffix_str + '; ' + 'i++)\n'
                str1 += '\t\tif (' + msg.name + alarm_arr_suffix_str + '[i] >= alarm_level)\n'
                str1 += '\t\t\talarm_level = ' + msg.name + alarm_arr_suffix_str + '[i];\n\n'

        str1 += '\treturn alarm_level;\n'
        str1 += '}\n\n\n'

    # else:
    #     if len(have_alarm_sig_msg_list) > 0:
    #         str1 += '\t// for avoid warning\n'
    #         for msg in have_alarm_sig_msg_list:
    #             str1 += '\t' + msg.name + alarm_arr_sum_suffix_str + ' = ' + msg.name + alarm_arr_sum_suffix_str + ';\n'
    #             str1 += '\t' + msg.name + alarm_arr_suffix_str + '[0] = ' + msg.name + alarm_arr_suffix_str + '[0];\n\n'

#     str1 += '/******************deal error status*******************/\n'

    return str1

def _create_gb_code2index(general_alarm_sig_list):
    code_list = []
    # get alarm sig's dtc value
    for sig in general_alarm_sig_list:
        dic = sig.get_alarm_level_dic()
        code_list.append(hex(int(dic[sig.general_alarm_dtc_str])))

    code_list.sort()

    str1 = '\n' + '#ifdef USING_PROTOCOL_GB' + '\n'*2
    str1 += 'userCode2Index_t st_gb_otherErrMap[] = ' + '\n'
    str1 += '{\n'

    if len(code_list) == 0:
        str1 += '\t{ 0xffffffff },\n'
    else:
        for str in code_list:
            str1 += '\t{' + str + '},\n'

    str1 += '};\n'

    str1 += \
'''\
userCode2IndexMan_t st_gb_otherErrMan =
{
    st_gb_otherErrMap,
    sizeof(st_gb_otherErrMap) / sizeof(st_gb_otherErrMap[0])
};

userCode2Index_t st_gb_chargeErrMap[] = {0};
userCode2IndexMan_t st_gb_chargeErrMan = {RT_NULL, 0};

userCode2Index_t st_gb_motorErrMap[] = {0};
userCode2IndexMan_t st_gb_motorErrMan = {RT_NULL, 0};

userCode2Index_t st_gb_engineErrMap[] = {0};
userCode2IndexMan_t st_gb_engineErrMan = {RT_NULL, 0};

userCode2IndexMan_t* p_dat_gb_Code2IndexMan[] =
{
    (userCode2IndexMan_t*)&st_gb_chargeErrMan,
    (userCode2IndexMan_t*)&st_gb_motorErrMan,
    (userCode2IndexMan_t*)&st_gb_engineErrMan,
    (userCode2IndexMan_t*)&st_gb_otherErrMan,
};
'''

    str1 += '\n' + '#endif' + '\n'

    return str1

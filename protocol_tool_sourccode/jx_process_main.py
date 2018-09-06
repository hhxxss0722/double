# -*- coding: utf-8 -*-
"""jx_process_main module"""

import win32ui
import time
import os,sys
import pprint
import easygui
import json


from can_stack.create_sig_h_file import *
from can_stack.create_sig_c_file import *
from can_stack.create_msg_h_file import *
from can_stack.create_msg_c_file import *
from can_stack.create_exch_h_file import *
from can_stack.create_exch_c_file import *
from can_stack.create_alarm_sig_infor_file import *

from public.parse_dbc_file import *
from public.parse_all_sigs_file import *
from public.dbc_class import *
from public.parse_formula_cfg_file import *

from auto_tool.create_asc_file import *
from public.utility import *

# root_path = real_root_path, src_path_component = r'source_file\jx_platform', platform_mode = 'jx_platform'
def jx_process_main(platform_config_dic):

    root_path = platform_config_dic['root_path']
    src_path_component = platform_config_dic['src_path_component']
    platform_mode = platform_config_dic['platform_mode']
    dbc_file_sum = platform_config_dic['dbc_file_sum']

    path_list, index_list = _get_path_and_index_list(dbc_file_sum)      ##[dbc file path , 1]
    path_dict = dict(zip(path_list, index_list))
    # print(path_dict)

    path_set = set(path_list)    ##dbc路径

    # print(path_set)

    # # get all sig list
    # all_sig_list, bat_alarm_sig_list = parse_all_sigs_file(root_path, src_path_component, 'all_sigs.txt', 'bat_alarm_sigs.txt')

    all_sig_infor_dic = _get_sig_infor_dic(root_path, src_path_component)       ##  all_sig_infor_json.txt
    bat_alarm_sig_dic = _get_bat_alarm_dic(root_path, src_path_component)       ##  bat_alarm_json.txt

    assert len(all_sig_infor_dic) > 0 and len(bat_alarm_sig_dic) > 0, 'all_sig_list or bat_alarm_sig_list is None!'

    print('-------all_sig_list-------\n')
    print('\n'.join(all_sig_infor_dic.keys()))
    print('\n*************************************')
    print('-------bat_alarm_sig_list-------\n')
    print('\n'.join(bat_alarm_sig_dic.keys()))
    print('\n*************************************')

    # get group inform dic
    group_infor_dic = _get_group_infor_dic(root_path, src_path_component)       ##  group_json.txt
    # get stated sig display dic
    stated_sig_display_dic = _get_stated_sig_display_dic(root_path, src_path_component)     ##  display4statedSignal_json.txt

    # get dbc list
    dbc_list = _get_dbc_list(path_set, path_dict, all_sig_infor_dic, bat_alarm_sig_dic, group_infor_dic)

    for dbc in dbc_list:
        dbc.speak()

    # # get formula config list
    # formula_list = parse_formula_cfg_file(root_path, src_path_component, 'formula_cfg.txt')
    #
    # if len(formula_list) == 0:
    #     raise TypeError('formula_list is empty!')
    #
    # print('\nformula sum = %d' % len(formula_list))

    # _create_new_json_file(formula_list, root_path, src_path_component)



    # for formula in formula_list:
    #     print('*************************************')
    #     formula.speak()
    # print('*************************************')

    valid_file_name = (dbc_list[0]).file_name.lower()

    can_stack_output_pre_path = root_path + '\\output\\can_stack\\'

    # create sig.h file canstack_xxx_sig.h
    sig_h_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name +'_sig.h'
    # create_sig_h_file(root_path, sig_h_output_path, messageList, dbc_file_name)
    create_sig_h_file(root_path, sig_h_output_path, dbc_list, platform_mode)
    # create sig.c file canstack_xxx_sig.c
    sig_c_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name +'_sig.c'
    different_unit_path = can_stack_output_pre_path + valid_file_name + '_different_unit_list.txt'
    sig_c_src_path_prefix = root_path + '\\' + src_path_component
    #由于版本3没有键的删除方法，所以100-101修改为102-103
    #valid_sig_list = all_sig_infor_dic.keys()
    #all_sig_infor_dic.pop('alarm_sig_name')
    all_sig_infor_dic.pop('alarm_sig_name')
    valid_sig_list = all_sig_infor_dic.keys()
    create_sig_c_file(sig_c_src_path_prefix, sig_c_output_path, dbc_list, valid_sig_list, different_unit_path,
                      platform_mode, group_infor_dic)
    # create msg.h file canstack_xxx_msg.h
    msg_h_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name +'_msg.h'
    create_msg_h_file(root_path, msg_h_output_path, dbc_list)
    # create msg.c file canstack_xxx_msg.c
    create_msg_c_file(root_path, can_stack_output_pre_path, dbc_list)
    # # # create exch.c file canstack_xxx_exch.c
    # # exch_c_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name.lower() +'_exch.c'
    # # different_unit_path = can_stack_output_pre_path + valid_file_name.lower() + '_different_unit_list.txt'
    # # create_exch_c_file(root_path, exch_c_output_path, different_unit_path, formula_list, dbc_list)
    #
    alarm_sig_infor_output_path = can_stack_output_pre_path + valid_file_name + '_alarm_sig_infor.txt'
    create_alarm_sig_infor_file(alarm_sig_infor_output_path, dbc_list)

    print('\nall formula sum = [%d]' % len(all_sig_infor_dic))
    print('\nall sig list sum = [%d]' % len(all_sig_infor_dic))

    for dbc in dbc_list:
        print('\n[%s]\n valid message sum = [%d]\n data sig sum = [%s]\n alarm sig sum = [%s]\n can channel = [%d]\n' % \
              (dbc.file_name, dbc.message_sum, dbc.data_sig_sum, dbc.alarm_sig_sum, dbc.can_channel))

    auto_tool_output_pre_path = root_path + '\\output\\auto_tool\\'
    # create *.asc file
    create_asc_file(root_path, src_path_component, auto_tool_output_pre_path, dbc_list, group_infor_dic, stated_sig_display_dic)
    os.system("pause")


def _get_dbc_list(path_set, path_dict, all_sig_infor_dic, bat_alarm_sig_dic, group_infor_dic):
    dbc_list = []

    for path in path_set:
        L1 = path.split('\\')

        message_list = parse_dbc_file(path, all_sig_infor_dic, bat_alarm_sig_dic, group_infor_dic)  # YD_CAN
        print('\n[%s]message sum = %d' % (L1[-1], len(message_list)))

        if len(message_list) == 0:
            raise TypeError('[%s] have no valid message!' % L1[-1])

        can_channel = path_dict[path]
        dbc_obj = Dbc_class(path, len(message_list), message_list, can_channel)
        dbc_list.append(dbc_obj)

    return dbc_list

def _get_path_and_index_list(dbc_file_sum):
    # dbc_file_sum = _get_dbc_file_sum()

    path_list = []
    index_list = []

    path_temp = None

    cnt = 0
    while cnt < dbc_file_sum:
        dlg = win32ui.CreateFileDialog(1, None, None, 0, "DBC File(*.dbc)|*.dbc||")

        dlg.SetOFNInitialDir('')
        dlg.DoModal()

        dbc_file_path = dlg.GetPathName()

        if len(dbc_file_path) == 0:
            print('no dbc file be selected!')
            print_cur_info()
            quit(1)

        print('dbc file path:%s' % dbc_file_path)

        if len(dbc_file_path) == 0:
            raise TypeError('file path is null!')

        if path_temp != dbc_file_path:
            path_temp = dbc_file_path
            path_list.append(dbc_file_path)
            index_list.append(cnt)

        time.sleep(1)

        cnt += 1

    return path_list, index_list

# get group sig dictionary
# 'sig_name':[]
def _get_group_infor_dic(root_path, src_path_component):
    json_path = root_path + '\\' + src_path_component + '\\' + 'group_json.txt'

    try:
        r_f = open(json_path, 'r')
    except:
        raise Exception

    context = r_f.read()

    if len(context) == 0:
        print_cur_info('****************ERROR!****************')
        print_cur_info()

    r_f.close()

    return json.loads(context, encoding='utf-8')

def _create_new_json_file(formula_list, root_path, src_path_component):
    fpath = root_path + '\\' + src_path_component + '\\' + 'all_sig_infor_json.txt'

    try:
        w_f = open(fpath, 'w')
    except:
        raise Exception

    w_f.write('{\n')

    for formula in formula_list:
        str1 = '\t"' + formula.sig_name + '":\n' + \
            '\t{\n' + \
            '\t\t"zh_name":"' + formula.zh_name + '",\n' + \
            '\t\t"formula":\n' + \
            '\t\t{\n' + \
            '\t\t\t"sig_name":' + '"' + formula.sig_name + '",\n' + \
            '\t\t\t"offset":' + str(formula.offset) + ',\n' + \
            '\t\t\t"scale":' + str(formula.scale) + ',\n' + \
            '\t\t\t"length":' + str(formula.get_byte_num()) + ',\n' + \
            '\t\t\t"min_val":' + str(formula.min_val) + ',\n' + \
            '\t\t\t"max_val":' + str(formula.max_val) + ',\n' + \
            '\t\t\t"invalid_val":' + str(formula.invalid_val) + ',\n' + \
            '\t\t\t"unit":' + '"' + formula.unit + '"\n' + \
            '\t\t}\n' + \
            '\t},\n\n'

        w_f.write(str1)

    w_f.write('}\n')

    w_f.close()

def _get_sig_infor_dic(root_path, src_path_component):
    json_path = root_path + '\\' + src_path_component + '\\' + 'all_sig_infor_json.txt'

    try:
        r_f = open(json_path, 'r',encoding='UTF-8')
    except:
        raise Exception

    context = r_f.read()

    if len(context) == 0:
        print_cur_info('****************ERROR!****************')
        print_cur_info()

    r_f.close()

    return json.loads(context, encoding='utf-8')

def _get_bat_alarm_dic(root_path, src_path_component):
    json_path = root_path + '\\' + src_path_component + '\\' + 'bat_alarm_json.txt'

    try:
        r_f = open(json_path, 'r',encoding='utf-8')
    except:
        raise Exception

    context = r_f.read()

    if len(context) == 0:
        print_cur_info('****************ERROR!****************')
        print_cur_info()

    r_f.close()

    return json.loads(context, encoding='utf-8')

def _get_stated_sig_display_dic(root_path, src_path_component):
    json_path = root_path + '\\' + src_path_component + '\\' + 'display4statedSignal_json.txt'

    try:
        r_f = open(json_path, 'r',encoding='utf-8')
    except:
        raise Exception

    context = r_f.read()

    if len(context) == 0:
        print_cur_info('****************ERROR!****************')
        print_cur_info()

    r_f.close()

    return json.loads(context, encoding='utf-8')

if __name__ == '__main__':
    jx_process_main()

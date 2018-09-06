# -*- coding: utf-8 -*-
"""main module"""

__name__ = '__main__'

import win32ui
import time
import os,sys
import pprint

root_path = sys.path[0]

pprint.pprint('root path ='+ root_path)

module_p_2 = root_path + '\\auto_tool'
sys.path.append(module_p_2)

module_p_3 = root_path + '\\public'
sys.path.append(module_p_3)

# pprint.pprint(sys.path)


from can_stack_new.create_sig_h_file import *
from can_stack_new.create_sig_c_file import *
from can_stack_new.create_msg_h_file import *
from can_stack_new.create_msg_c_file import *

from public.parse_dbc_file import *
from public.parse_all_sigs_file import *
from public.dbc_class import *
from public.parse_formula_cfg_file import *

from auto_tool.create_asc_file import *


def main():

    DBC_FILE_SUM = _get_dbc_file_sum()

    cnt = 0

    path_list = []
    index_list = []

    path_temp = None

    while cnt < DBC_FILE_SUM:
        dlg = win32ui.CreateFileDialog(1)

        dlg.SetOFNInitialDir('')
        dlg.DoModal()

        dbc_file_path = dlg.GetPathName()
        print('dbc file path:%s' % dbc_file_path)

        if len(dbc_file_path) == 0:
            raise TypeError('file path is null!')

        if path_temp != dbc_file_path:
            path_temp = dbc_file_path
            path_list.append(dbc_file_path)
            index_list.append(cnt)

        time.sleep(1)

        cnt += 1

    path_dict = dict(zip(path_list, index_list))
    print(path_dict)

    path_set = set(path_list)

    print(path_set)

    # get all sig list
    all_sig_list = parse_all_sigs_file(root_path, 'all_sigs.txt')

    if len(all_sig_list) == 0:
        raise TypeError('all_sig_list is None!')

    # print('-------all_sig_list-------\n')
    # for item in all_sig_list:
    #     print(item)
    # print('*************************************')

    # get dbc list
    dbc_list = _get_dbc_list(path_set, path_dict, all_sig_list)

    for dbc in dbc_list:
        dbc.speak()

    # get formula config list
    formula_list = parse_formula_cfg_file(root_path, 'formula_cfg.txt')

    if len(formula_list) == 0:
        raise TypeError('formula_list is empty!')

    print('\nformula sum = %d' % len(formula_list))

    # for formula in formula_list:
    #     print('*************************************')
    #     formula.speak()
    # print('*************************************')

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name

    can_stack_output_pre_path = root_path + '\\output\\can_stack_new\\'
    
    # create sig.h file canstack_xxx_sig.h
    sig_h_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name.lower() +'_sig.h'
    create_sig_h_file(root_path, sig_h_output_path, dbc_list, len(all_sig_list))
    # create sig.c file canstack_xxx_sig.c
    sig_c_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name.lower() +'_sig.c'
    create_sig_c_file(root_path, sig_c_output_path, dbc_list, all_sig_list)
    # create msg.h file canstack_xxx_msg.h
    msg_h_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name.lower() +'_msg.h'
    create_msg_h_file(root_path, msg_h_output_path, dbc_list)
    # create msg.c file canstack_xxx_msg.c
    create_msg_c_file(root_path, can_stack_output_pre_path, dbc_list)
    # # create exch.c file canstack_xxx_exch.c
    # exch_c_output_path = can_stack_output_pre_path + 'canstack_' + valid_file_name.lower() +'_exch.c'
    # different_unit_path = can_stack_output_pre_path + valid_file_name.lower() + '_different_unit_list.txt'
    # create_exch_c_file(root_path, exch_c_output_path, different_unit_path, formula_list, dbc_list)

    print('\nall formula sum = [%d]' % len(formula_list))
    print('\nall sig list sum = [%d]' % len(all_sig_list))

    for dbc in dbc_list:
        print('\n[%s] valid message sum = [%d]\n sig sum = [%s]\n can channel = [%d]\n' % (dbc.file_name, dbc.message_sum, dbc.sig_sum, dbc.can_channel ))
    
    auto_tool_output_pre_path = root_path + '\\output\\auto_tool\\'
    # create *.asc file
    create_asc_file(root_path, auto_tool_output_pre_path, dbc_list, formula_list)
    # os.system("pause")

def _get_dbc_list(path_set, path_dict, all_sig_list):
    dbc_list = []

    for path in path_set:
        L1 = path.split('\\')

        message_list = parse_dbc_file(path, all_sig_list)  # YD_CAN
        print('\n[%s]message sum = %d' % (L1[-1], len(message_list)))

        if len(message_list) == 0:
            raise TypeError('[%s] have no valid message!' % L1[-1])

        can_channel = path_dict[path]
        dbc_obj = Dbc_class(path, len(message_list), message_list, can_channel)
        dbc_list.append(dbc_obj)

    return dbc_list

def _get_dbc_file_sum():
    while True:
        number_str = raw_input('please input DBC file sum(min:1, max:3)--->:')
        if number_str.isdigit():
            number = int(number_str, 10)
            if number >= 1 and number <= 3:
                return number
        print('input error! input again!')


if __name__ == '__main__':
    main()

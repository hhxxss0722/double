# -*- coding: utf-8 -*-
"""main module"""

import win32ui
import time
import os,sys
import pprint
import easygui


from jx_process_main import *

root_path = os.path.abspath(sys.argv[0])

root_path_list = root_path.split('\\')
root_path_list.pop()
root_path = ('\\').join(root_path_list)
    
pprint.pprint('root path =' + root_path)

module_p_2 = root_path + '\\auto_tool'
sys.path.append(module_p_2)

module_p_3 = root_path + '\\public'
sys.path.append(module_p_3)

# pprint.pprint(sys.path)

jx_platform_config_dic = \
    {
        'root_path': root_path,
        'src_path_component': r'source_file\jx_platform',
        'platform_mode': 'jx_platform',
        'dbc_file_sum': 0,
        'deal_fun': jx_process_main,
    }

gb_platform_config_dic = \
    {
        'root_path': root_path,
        'src_path_component': r'source_file\gb_platform',
        'platform_mode': 'gb_platform',
        'dbc_file_sum': 0,
        'deal_fun': jx_process_main,
    }


JX_PLATFORM_INDEX = 0
GB_PLATFORM_INDEX = 1

platform_config_man_dic = \
    {
        JX_PLATFORM_INDEX: jx_platform_config_dic,
        GB_PLATFORM_INDEX: gb_platform_config_dic,
    }

def main():
    platform_index = _get_platform_index()

    print((platform_config_man_dic[platform_index])['platform_mode'])

    dbc_file_sum = _get_dbc_file_sum()

    print('dbc file sum = %d' % dbc_file_sum)

    (platform_config_man_dic[platform_index])['dbc_file_sum'] = dbc_file_sum
 
    # invoke special function
    (platform_config_man_dic[platform_index])['deal_fun'](platform_config_man_dic[platform_index])

    # os.system("pause")


# get platform index
def _get_platform_index():
    index = easygui.indexbox(msg='请选择平台', title='平台选择', choices=('江西平台'.decode('utf-8'), '国标平台'.decode('utf-8'), ))

    if index is None:
        print('none platform be selected!')

        quit(1)

    return index

# get dbc file sum
def _get_dbc_file_sum():
    number_str = easygui.enterbox(msg='请输入待处理DBC文件个数(1~3)')

    while True:
        if number_str is None:
            print('dbc file sum input is none!')

            break

        if number_str.isdigit():
            number = int(number_str, 10)
            if 1 <= number <= 3:
                return number
        number_str = easygui.enterbox(msg='输入有误，重新输入！输入范围(1~3)')
        # print('input error! input again!')
    quit(1)

if __name__ == '__main__':
    main()
    os.system("pause")

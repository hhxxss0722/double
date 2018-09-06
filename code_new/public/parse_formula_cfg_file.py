# -*- coding: utf-8 -*-

"""parse_formula_cfg_file module"""

import re

from public.formula_class import *

# fun:uint16_t get_vehicle_speed(void)
# sig_name:vehicle_speed
# zh_name:车速
# offset:0
# scale:0.1
# min_val:0
# max_val:2200
# invalid_val:65535
# unit:km/h

def parse_formula_cfg_file(root_path, src_path_compoent, file_name):
    print('enter parse_formula_cfg_file fun!\n')

    if len(file_name) == 0 or len(root_path) == 0:
        raise TypeError('root path or file name is none!')

    file_path = root_path + '\\' + src_path_compoent + '\\' + file_name

    dbc_f = open(file_path, 'r')
    file_lines = dbc_f.readlines()

    formula_list = []

    # fun:uint16_t get_vehicle_speed(void)
    fun_re = re.compile(r'fun:\s*(\w+)\s+(\w+)+\s*\((.+)\)')
    # sig_name:vehicle_speed
    sig_name_re = re.compile(r'sig_name:\s*(\w+)')
    # zh_name:档位
    zh_name_re = re.compile(r'zh_name:\s*([\u2E80-\u9FFF]+)')
    # offset:0
    offset_re = re.compile(r'offset:\s*(.*)')
    # scale:2
    scale_re = re.compile(r'scale:\s*(.*)')
    # min_val:0
    min_val_re = re.compile(r'min_val:\s*(.*)')
    # max_val:250
    max_val_re = re.compile(r'max_val:\s*(.*)')
    # invalid_val:65535
    invalid_val_re = re.compile(r'invalid_val:\s*(.*)')
    # unit:km
    unit_re = re.compile(r'unit:\s*(.*)')

    file_line_sum = len(file_lines)
    print('file_line_sum = %d\n' % file_line_sum)
    if file_line_sum == 0:
        raise TypeError('formula_cfg_file is empty!')

    cnt = 0
    return_data_t = ''
    name = ''
    param_str = ''
    sig_name = ''
    offset_str = ''
    scale_str = ''
    min_val_str = ''
    max_val_str = ''
    invalid_val_str = ''
    unit_str = ''
    zh_name = ''

    while cnt < file_line_sum:
        text_line = file_lines[cnt].strip()
        # fun:uint16_t get_vehicle_speed(void)
        if text_line.startswith('fun:'):
            fun_re_result = fun_re.search(text_line)
            try:
                return_data_t = fun_re_result.group(1)
                name = fun_re_result.group(2)
                param_str = fun_re_result.group(3)
            except:
                raise TypeError('[fun] format error! line = %s' % str(cnt + 1))
        # sig_name:vehicle_speed
        if text_line.startswith('sig_name:'):
            sig_name_re_result = sig_name_re.search(text_line)
            try:
                sig_name = sig_name_re_result.group(1)
            except:
                raise TypeError('[sig_name] format error! line = %s' % str(cnt + 1))
        # zh_name:档位
        if text_line.startswith('zh_name:'):
            zh_name = text_line[8:]
            # zh_name_re_result = zh_name_re.search(text_line)
            # try:
            #     zh_name = zh_name_re_result.group(1)
            # except:
            #     raise TypeError('[sig_name] format error! line = %s' % str(cnt + 1))
        # offset:0
        if text_line.startswith('offset:'):
            offset_re_result = offset_re.search(text_line)
            try:
                offset_str = offset_re_result.group(1)
            except:
                raise TypeError('[offset] format error! line = %s' % str(cnt + 1))
        # scale:2
        if text_line.startswith('scale:'):
            scale_re_result = scale_re.search(text_line)
            try:
                scale_str = scale_re_result.group(1)
            except:
                raise TypeError('[scale] format error! line = %s' % str(cnt + 1))
        # min_val:0
        if text_line.startswith('min_val:'):
            min_val_re_result = min_val_re.search(text_line)
            try:
                min_val_str = min_val_re_result.group(1)
            except:
                raise TypeError('[min_val] format error! line = %s' % str(cnt + 1))
        # max_val:0
        if text_line.startswith('max_val:'):
            max_val_re_result = max_val_re.search(text_line)
            try:
                max_val_str = max_val_re_result.group(1)
            except:
                raise TypeError('[min_val] format error! line = %s' % str(cnt + 1))
        # invalid_val:65535
        if text_line.startswith('invalid_val:'):
            invalid_val_re_result = invalid_val_re.search(text_line)
            try:
                invalid_val_str = invalid_val_re_result.group(1)
            except:
                raise TypeError('[min_val] format error! line = %s' % str(cnt + 1))
        # unit:%
        if text_line.startswith('unit:'):
            unit_re_result = unit_re.search(text_line)
            try:
                unit_str = unit_re_result.group(1)
            except:
                raise TypeError('[unit] format error! line = %s' % str(cnt + 1))

            if (len(return_data_t) == 0) or (len(name) == 0) or (len(param_str) == 0) or (len(sig_name) == 0):
                raise TypeError('formula attribute error! line = %s' % str(cnt + 1))

            if (len(offset_str) == 0) or (len(scale_str) == 0) or (len(min_val_str) == 0) or (len(max_val_str) == 0):
                raise TypeError('formula config error! line = %s' % str(cnt + 1))

            # __init__(self, return_data_type='', name='', param_str='', sig_name='', offset='', scale='', min_val='', max_val='', unit='')
            # (self, sig_name, zh_name, offset, scale, min_val, max_val, invalid_val, unit)
            formula_1 = Formula(sig_name, zh_name, offset_str, scale_str, min_val_str, max_val_str, invalid_val_str, unit_str)
            formula_list.append(formula_1)

            return_data_t = ''
            name = ''
            param_str = ''
            sig_name = ''
            offset_str = ''
            scale_str = ''
            invalid_val_str = ''
            unit_str = ''
            zh_name = ''

        cnt += 1

    print('parse formula_cfg_file success!')
    return formula_list
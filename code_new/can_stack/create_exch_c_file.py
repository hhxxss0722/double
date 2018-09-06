# -*- coding: utf-8 -*-
'''create_exch_c_file module'''

bat_cell_volt_prefix_str = 'bat_cell_volt'
bat_cell_temp_prefix_str = 'bat_cell_temp'
different_unit_list = []

# def create_exch_c_file(root_path, out_path, formula_list, message_list, dbc_file_name):
def create_exch_c_file(root_path, exch_c_output_path, different_unit_path, formula_list, dbc_list):
    if len(root_path) == 0 or len(formula_list) == 0 or len(dbc_list) == 0:
        raise TypeError('param is error!')

    target_f_path = exch_c_output_path

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name

    try:
        tar_f = open(target_f_path, 'w')

        str1 = '#include \"canstack_exch.h\"\n\n'
        str1 += '//#include \"canstack_' + valid_file_name.lower() + '_exch.h\"\n\n'
        str1 += '#ifdef CANSTACK_' + valid_file_name.upper() + '\n\n'

        tar_f.write(str1)
        tar_f.write('\n')
        tar_f.close()
    except:
        raise TypeError('operate msg.c file fail!')

    tar_f = open(target_f_path, 'a')

    message_list = []

    # get message list set
    for dbc in dbc_list:
        message_list += dbc.message_list

    for formula in formula_list:
        str1 = ''

        str1 += '\n/* ' + formula.name + ' */\n'
        str1 += formula.return_data_type + ' ' + formula.name + '(' + formula.param_str + ')\n'
        str1 += '{\n'
        sig = _find_sig_in_msg_list(formula.sig_name, message_list)

        if sig != None:
            str1 += _create_sig_formula(formula, sig)
        elif formula.sig_name == bat_cell_volt_prefix_str or formula.sig_name == bat_cell_temp_prefix_str:
            sig = _find_sig_in_msg_list(formula.sig_name + '_1', message_list)
            if sig != None:
                str1 += _create_sig_formula(formula, sig, formula.sig_name)
            else:
                str1 += '\treturn ' + str(formula.invalid_val) + ';'
        else:
            str1 += '\treturn ' + str(formula.invalid_val) + ';'

        str1 += '\n}'
        tar_f.write(str1)

    str1 = '\n#endif\n'
    tar_f.write(str1)

    tar_f.close()

    if len(different_unit_list) != 0:
        str1 = '\n'.join(different_unit_list)

        d_f = open(different_unit_path, 'w')
        d_f.write(str1)
        d_f.close()
    else:
        d_f = open(different_unit_path, 'w')
        d_f.write('此地无银三百两。\n\t\t---匿名者留言')
        d_f.close()

    print('create exch.c file success!')

type_value_dict =\
{
    'uint8_t':'u8Value',
    'uint16_t':'u16Value',
    'uint32_t':'u32Value',
    'uint64_t':'u64Value'
}

# transit part of formula unit
def _unit_transition(formula, sig):

    if formula.unit == sig.unit:
        return ''

    str1 = formula.name + ' unit: ' + formula.unit + '\t<------>\t' + sig.name + ' unit: ' + sig.unit
    different_unit_list.append(str1)

    if (formula.unit == 'MA') and (sig.unit == 'A'):
        return '1000'

    if (formula.unit == 'A') and (sig.unit == 'MA'):
        return '0.001'

    if (formula.unit == 'MV') and (sig.unit == 'V'):
        return '1000'

    if (formula.unit == 'V') and (sig.unit == 'MV'):
        return '0.001'

    return ''

def _create_sig_formula(formula, sig, group_sig_name = None):
    if group_sig_name == None:
        str1 = '\tfloat fValue = CANSTACK_READ_SIGNAL(' + sig.name + ');\n'
        str1 += '\n\tprintd("\\r\\n' + sig.name + ' = [%d]\\r\\n", (' + sig.get_data_type() +')fValue);\n\n'
    else:
        # fun param is uint8_t index
        str1 = '\tfloat fValue = CANSTACK_READ_GROUP_SIGNAL(' + group_sig_name + ', index);\n'
        str1 += '\n\tprintd("\\r\\n' + group_sig_name + ' = [%d]\\r\\n", (' + sig.get_data_type() +')fValue);\n\n'

    str1 += '\tif(FLOAT_MAX_VALUE == fValue)\n'
    str1 += '\t{return ' + str(formula.invalid_val) + ';}\n'

    str2 = _unit_transition(formula, sig)
    if len(str2) > 0:
        str1 += '\n\t//unit transition\n'
        str1 += '\tfValue *= ' + str2 + ';\n'

    if formula.offset != 0:
        str1 += '\n\tfValue -= (' + str(formula.offset) + ');\n'

    if formula.scale != 1:
        str1 += '\n\tfValue /= ' + str(formula.scale) + ';\n'

    str1 += '\n\t' + 'if( (fValue < ' + str(formula.min_val) + ') || (fValue > ' + str(formula.max_val) + ') )\n'
    str1 += '\t{return ' + str(formula.invalid_val) + ';}\n\n'

    str1 += '\treturn (' + formula.return_data_type + ')fValue;'

    return str1

def _find_sig_in_msg_list(sig_name, message_list):
    for message in message_list:
        for sig1 in message.sig_list:
            if sig1.name == sig_name:
                return sig1

    return None

# def create_general_fun_body(formula, sig):


# def _create_sig_formula(formula, sig):
#     value_str = type_value_dict[sig.get_data_type()]
#     str1 = ''
#     str1 += '\t' + sig.get_data_type() + ' ' + value_str + ' = CANSTACK_READ_SIGNAL(' + sig.name + ');\n'
#     str1 += '\t' + 'bool isGreater = false;\n'
#
#     # pro_var_type = ''
#     # pro_var_name = ''
#     # have_change = False
#
#     sig_int = int(sig.scale)
#     formula_int = int(formula.scale)
#     # 判断信号和平台的分辨率是否都为整数，整数使用uint16_t 否则使用float
#     if (sig_int == sig.scale) and (formula_int == formula.scale):
#         # 分辨率都为1且信号值类型与函数返回值类型相同则不用强制转换
#         if (sig_int == 1) and (formula_int == 1) and (sig.get_data_type() == formula.return_data_type):
#             pro_var_type = sig.get_data_type()
#             pro_var_name = value_str
#             have_change = False
#         else:
#             pro_var_type = formula.return_data_type
#             pro_var_name = type_value_dict[formula.return_data_type]
#             have_change = True
#     else:
#         pro_var_type = 'float'
#         pro_var_name = 'fValue'
#         have_change = True
#
#     if have_change:
#         str1 += '\t' + pro_var_type + ' ' + pro_var_name + ' = (' + pro_var_type + ')' + value_str + ';\n'
#         str1 += '\t' + pro_var_name + ' *= ' + str(sig.scale) + ';\n'
#
#     str1 += '\n'
#
#     if sig.offset == 0:
#         negative = False
#         pass
#     elif sig.offset > 0:
#         negative = False
#         str1 += '\t' + pro_var_name + ' += ' + str(sig.offset) + ';\n'
#     else:
#         negative = True
#         abs_value = str( abs(sig.offset) )
#         str1 += '\tif(' + pro_var_name + ' >= ' + abs_value + ')\n'
#         str1 += '\t{\n'
#         str1 += '\t\t' + pro_var_name + ' -= ' + abs_value + ';' + '//real value\n'
#         str1 += '\t\t' + 'isGreater = true;\n'
#         str1 += '\t}\n'
#         str1 += '\telse\n'
#         str1 += '\t{\n'
#         str1 += '\t\t' + pro_var_name + ' = ' + abs_value + ' - ' + pro_var_name + ';\n'
#         str1 += '\t\t' + 'isGreater = false;\n'
#         str1 += '\t}\n'
#
#     str1 += '\n'
#     str1 += '\t // [' + str(sig.min_val) + ',' + str(sig.max_val) + ']\n'
#
#     if negative:
#         str1 += '\tif( (isGreater && (' + pro_var_name + ' > ' + str(sig.max_val) + ' ) ) || ( !isGreater && (' + \
#                 pro_var_name + ' > ' + str(sig.min_val) + ' ) ) )\n'
#     else:
#         str1 += '\tif( (' + pro_var_name + ' > ' + str(sig.max_val) + '  ) || (' + pro_var_name + ' < ' + str(sig.min_val) + ' ) )\n'
#
#     str1 += '\t{\n'
#     str1 += '\t\t' + 'return ' + str(formula.invalid_val) + ';\n'
#     str1 += '\t}\n'
#
#     abs_value = str(abs(formula.offset))
#     if negative:
#         str1 += '\tif(isGreater)\n'
#         str1 += '\t{\n'
#         str1 += '\t\t' + pro_var_name + ' += ' + abs_value + ';\n'
#         str1 += '\t\t' + pro_var_name + ' *= ' + str(formula.scale) + ';\n'
#         str1 += '\t}\n'
#     else:
#         # 根据实际情况，formula offset 多为负值，这里都写成 + offset
#         str1 += '\t' + pro_var_name + ' += ' + abs_value + ';\n'
#         str1 += '\t' + pro_var_name + ' *= ' + str(formula.scale) + ';\n'
#
#     str1 += '\n'
#
#     str1 += '\t' + 'return(' + formula.return_data_type + ')' + pro_var_name + ';\n'
#
#     return str1

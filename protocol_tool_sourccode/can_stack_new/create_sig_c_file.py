# -*- coding: utf-8 -*-
'''creat_sig_c_file module'''

import operator

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

exist_sig_name_list = []
exist_sig_list = []

bat_cell_volt_prefix_str = 'bat_cell_volt'
bat_cell_volt_list = []

bat_cell_temp_prefix_str = 'bat_cell_temp'
bat_cell_temp_list = []

# def create_sig_c_file(root_path, out_path, message_list, all_sig_list, dbc_file_name):
def create_sig_c_file(root_path, sig_c_output_path, dbc_list, valid_sig_name_list):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or dbc list is None!')

    target_sig_f_path = sig_c_output_path

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name

    try:
        tar_f = open(target_sig_f_path, 'w')

    except:
        raise TypeError('operate sig.c file fail!')

    str1 = '#include \"canstack_' + valid_file_name.lower() + '_sig.h\"\n'
    str1 += '#include \"canstack_' + valid_file_name.lower() + '_msg.h\"\n\n\n'
    str1 += '#ifdef CANSTACK_' + valid_file_name.upper() + '\n\n'

    tar_f.write(str1)

    message_list = []

    # get message list set
    for dbc in dbc_list:
        message_list += dbc.message_list

    # # vehicle sig define
    # for message in message_list:
    #     str1 = '/* ' + message.name + ':'+ message.ID + ' */\n'
    #     str1 += '#define CAN_' + message.name.upper() + '_DATA_ARRAY\t\t\tDATA_ARRAY(' + message.name + ')\n'
    #     str1 += '#define CAN_' + message.name.upper() + '_OUTIND\t\t\tMESSAGE_OUTIND(' + message.name + ')\n'
    #     str1 += '\n'
    #     str1 += 'extern DATA_ARRAY_DECLARE(' + message.name + ');\n'
    #     str1 += 'extern MESSAGE_OUTIND_DECLARE(' + message.name + ');\n'
    #
    #     tar_f.write(str1)

    for message in message_list:

        for sig in message.sig_list:

            exist_sig_list.append(sig)

            if sig.name.startswith(bat_cell_volt_prefix_str):
                # bat_cell_volt_x
                exist_sig_name_list.append(bat_cell_volt_prefix_str)
                bat_cell_volt_list.append(sig)
            elif sig.name.startswith(bat_cell_temp_prefix_str):
                # bat_cell_temp_x
                exist_sig_name_list.append(bat_cell_temp_prefix_str)
                bat_cell_temp_list.append(sig)
            else:
                exist_sig_name_list.append(sig.name)

                # CANSTACK_SET_SIG_BODY(bat_soc) {}
                str1 = _create_set_sig_body(sig)

                tar_f.write(str1)

    tar_f.write('\n')

    # create CANSTACK_GET_GROUP_SIG_FUN_BODY(bat_cell_volt, 0) and CANSTACK_SET_SIG_BODY(bat_cell_volt)
    if len(bat_cell_volt_list) > 0:
        str1 = ''
        str1 += _create_get_group_sig_fun_body(bat_cell_volt_list, bat_cell_volt_prefix_str)
        str1 += _create_set_sig_body_for_group(bat_cell_volt_list, bat_cell_volt_prefix_str)
        tar_f.write(str1)

    # create CANSTACK_GET_GROUP_SIG_FUN_BODY(bat_cell_temp, 0) and CANSTACK_SET_SIG_BODY(bat_cell_temp)
    if len(bat_cell_temp_list) > 0:
        str1 = ''
        str1 += _create_get_group_sig_fun_body(bat_cell_temp_list, bat_cell_temp_prefix_str)
        str1 += _create_set_sig_body_for_group(bat_cell_temp_list, bat_cell_temp_prefix_str)
        tar_f.write(str1)

    remain_sig_name_list = set(valid_sig_name_list) - set(exist_sig_name_list)

    if len(remain_sig_name_list) > 0:
        # create remain sig's SET_SIGNAL fun body. like:CANSTACK_SET_SIG_BODY(invalid_sig)
        str1 = '/* get invalid_sig value */\n'
        str1 += 'CANSTACK_SET_SIG_BODY(invalid_sig)\n'
        str1 += '{return FLOAT_MAX_VALUE;}\n\n'
        tar_f.write(str1)

    # create sig_infor_t sig_infor_array[]
    str1 = _create_sig_infor_array(valid_sig_name_list, remain_sig_name_list)
    tar_f.write(str1)

    sig_suffix_f_path = root_path + '\\' + 'source_file' + '\\' + 'canstack_xxx_new_sig_c_suffix.c'
    try:
        pre_f = open(sig_suffix_f_path, 'r')
        tar_f.write(pre_f.read())

        pre_f.close()
    except:
        raise TypeError('operate sig.c suffix file fail!')

    tar_f.close()

    print('create sig.c file success!')

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
def _create_set_sig_body_for_group(sig_list, valid_name):
    # sig_list.sort(key = operator.attrgetter('suffix_num'), reverse = False)
    sig_list.sort(key = lambda Sig: Sig.suffix_num, reverse = False)
    sum = len(sig_list)
    cnt = 0

    str1 = ''
    str1 += '/* get ' + valid_name + ' value */\n'
    str1 += 'CANSTACK_SET_GROUP_BODY(' + valid_name + ')\n'
    str1 += '{\n'
    str1 += '\tfloat fValue = 0.0;\n'
    str1 += '\tuint8_t index = *(uint8_t *)param;\n\n'
    str1 += '\tswitch(index)\n'
    str1 += '\t{\n'

    while cnt < sum:
        sig = sig_list[cnt]
        str1 += '\t\tcase ' + str(cnt) + ':\n'
        str1 += '\t\t\tfValue = CANSTACK_GET_GROUP_SIG(' + valid_name + ', ' + str(cnt + 1) + ');' + '/* ' + sig.name + ' */\n'
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

    return None

# sig_infor_t sig_infor_array[]
def _create_sig_infor_array(valid_sig_name_list, remain_sig_name_list):
    # sig_infor_t sig_infor_array[] __at(SIG_INFOR_ARRAY_ADD)=
    str1 = 'sig_infor_t sig_infor_array[] __at(SIG_INFOR_ARRAY_ADD)=\n'
    str1 += '{\n'

    for name in valid_sig_name_list:
        if name in remain_sig_name_list:
            str1 += '\t{ CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},\t/* ' + name + ' */\n'
        else:
            sig = _get_sig_with_name(exist_sig_list, name)
            if sig == None:
                sig = _get_sig_with_name(exist_sig_list, name + '_1')
                if sig == None:
                    raise TypeError('sig name error!')

            str1 += '\t{ CANSTACK_SET_SIG_FUN_NAME(' + name + ')},\t/* ' + name + ' */\n'

    str1 += '\n};\n'
    return str1

# CANSTACK_SET_SIG_BODY(bat_soc) {}
def _create_set_sig_body(sig, index_str = None, valid_name = None):
    # ((canstack_msg_data_t *)(CAN_VEHICLE_INFOR_DATA_ARRAY))->vehicle_infor.
    data_type_pre = '((canstack_msg_data_t *)CAN_' + sig.parent_message.name.upper() + '_DATA_ARRAY)->' + sig.parent_message.name + '.' + sig.name
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
    str1 += '\tif(CAN_' + sig.parent_message.name.upper() + '_TIMEOUT_FLAG)\n'
    str1 += '\t{return FLOAT_MAX_VALUE;}\n\n'
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
    # specified data will be set corresponding bit
    # if (sig.start_bit % 8) > 0:
        # str1 += '\n\t' + 'unData.u32Data >>= ' + str(sig.start_bit % 8) + ';\n'
        # str1 += '\t' + 'unData.u32Data &= ' + '( ~(0xFFFFFFFF <<' + str(32 - (sig.start_bit % 8)) + '));\n'

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
    # min value is litter than max value
    if sig.min_val < sig.max_val:
        str1 += '\tif((fValue < ' + str(sig.min_val) + ') || (fValue > ' + str(sig.max_val) + '))\n'
        str1 += '\t{return FLOAT_MAX_VALUE;}\n\n'

    str1 += '\treturn fValue;\n'
    str1 += '}\n'

    return str1

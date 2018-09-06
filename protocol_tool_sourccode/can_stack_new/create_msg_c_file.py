# -*- coding: utf-8 -*-
'''creat_msg_c_file module'''

# msg_c_output_path = output_pre_path + 'canstack_' + dbc_file_name.lower() +'_msg.c'
def create_msg_c_file(root_path, output_pre_path, dbc_list):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or dbc list is error!')

    for dbc in dbc_list:
        output_path = output_pre_path + 'canstack_' + dbc.file_name.lower() +'_msg.c'
        _create_specified_msg_c_file(root_path, output_path, dbc.message_list, dbc.valid_file_name, str(dbc.can_channel))

# create specified msg.c file
def _create_specified_msg_c_file(root_path, out_path, message_list, dbc_file_name, channel_str):
    if len(root_path) == 0 or len(message_list) == 0:
        raise TypeError('root path or message list is error!')

    target_f_path = out_path

    try:
        tar_f = open(target_f_path, 'w')

    except:
        raise TypeError('operate msg.c file fail!')

    str1 = '#include \"canstack_' + dbc_file_name.lower() + '_msg.h\"\n'
    str1 += '#include \"canstack_' + dbc_file_name.lower() + '_sig.h\"\n\n'
    str1 += '#ifdef CANSTACK_' + dbc_file_name.upper() + '\n\n'

    tar_f.write(str1)

    str1 = '//CAN' + channel_str + '\n' +'#ifdef CANSTACK_CAN' + channel_str + '\n\n'
    tar_f.write(str1)

    str1 = 'typedef enum\n'
    str1 += '{\n'

    # define enumeration
    count = 0
    for message in message_list:
        upper_name = message.name.upper()

        str1 += '\t' + upper_name + ' = ' + str(count) + ',\n'
        count += 1

    str1 += '}msg_type;\n\n'
    tar_f.write(str1)

    message_timeout_fun_str = 'message_timeout_fun_' + channel_str
    message_timeout_fun_def_str = 'static void ' + message_timeout_fun_str + '(void * parg, cuint8_t index)'

    get_timeout_flag_str = 'get_timeout_flag_' + channel_str
    get_timeout_flag_def_str = 'static cuint8_t ' + get_timeout_flag_str + '(cuint8_t index)'

    get_limit_cnt_str = 'get_limit_cnt_' + channel_str
    get_limit_cnt_def_str = 'static cuint16_t ' + get_limit_cnt_str + '(cuint8_t index)'

    get_current_cnt_str = 'get_current_cnt_' + channel_str
    get_current_cnt_def_str = 'static cuint16_t ' + get_current_cnt_str + '(cuint8_t index)'

    add_current_cnt_str = 'add_current_cnt_' + channel_str
    add_current_cnt_def_str = 'static void '+ add_current_cnt_str + '(cuint8_t index)'

    timeout_fun_str = 'timeout_fun_' + channel_str
    timeout_fun_def_str = 'static void ' + timeout_fun_str + '(cuint8_t index)'

    init_can_msg_infor_str = 'init_can_msg_infor_' + channel_str
    init_can_msg_infor_def_str = 'static void ' + init_can_msg_infor_str + '(void)'

    message_recv_fun_str = 'message_recv_fun_' + channel_str
    message_recv_fun_def_str = 'static void ' + message_recv_fun_str + '(void * parg, cuint8_t index)'

    # declare static fun
    str1 = message_timeout_fun_def_str + ';\n'
    str1 += get_timeout_flag_def_str + ';\n'
    str1 += get_limit_cnt_def_str + ';\n'
    str1 += get_current_cnt_def_str + ';\n'
    str1 += add_current_cnt_def_str + ';\n'
    str1 += timeout_fun_def_str + ';\n'
    str1 += init_can_msg_infor_def_str + ';\n\n'
    tar_f.write(str1)

    msg_upper_name_list = []

    for message in message_list:
        str1 = ''
        upper_name = message.name.upper()

        msg_upper_name_list.append(upper_name)

        # /* hybird_infor:0x18EF4AEF */
        str1 += '/* ' + message.name + ':'+ message.ID + ' */' + '\n'

        # #define CAN_HYBIRD_INFOR_ID                     0x18EF4AEF
        str1 += '#define CAN_'+ upper_name +'_ID\t\t\t\t\t' + message.ID + '\n'

        # #define CAN_HYBIRD_INFOR_CYCLE                  200
        str1 += '#define CAN_'+ upper_name + '_CYCLE\t\t\t\t\t' + message.period + '\n'

        str1 += '\n'
        tar_f.write(str1)

    tar_f.write('\n')

    # define msg_infor_x[]
    str1 = 'can_msg_infor_t msg_infor_' + channel_str + '[] __at(MSG_INFOR_ADD_' + channel_str + ')=\n'
    str1 += '{\n'
    count = 0
    while count < len(msg_upper_name_list):
        str1 += '\t{ CAN_' + msg_upper_name_list[count] + '_CYCLE / PUBLIC_TIMER_SCALE, (cuint8_t)' + msg_upper_name_list[count] + '},\n'
        count += 1
    str1 += '};\n\n'
    tar_f.write(str1)

    # define init_can_msg_infor_x
    str1 = init_can_msg_infor_def_str + '\n'
    str1 += '{\n'
    str1 += '\t' + 'memset((cuint8_t *)CAN_TIMEOUT_FLAG_ADD_BASE_' + channel_str + ', c_True, CAN_TIMEOUT_FLAG_SIZE_' + channel_str + ');\n'
    str1 += '\t' + 'memset((cuint8_t *)CAN_CURRENT_CNT_ADD_BASE_' + channel_str + ', 0x0, CAN_CURRENT_CNT_SIZE_' + channel_str + ');\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define msg_infor_manager_x
    str1 = 'const can_msg_infor_manager_t msg_infor_manager_' + channel_str + ' __at(MSG_INFOR_MANAGER_ADD_' + channel_str + ')=\n'
    str1 += '{\n'
    str1 += '\t' + 'ARRAY_SIZE(' + 'msg_infor_' + channel_str + '),\n'
    str1 += '\t' + init_can_msg_infor_str + ',\n'
    str1 += '\t' + get_timeout_flag_str + ',\n'
    str1 += '\t' + get_limit_cnt_str + ',\n'
    str1 += '\t' + get_current_cnt_str + ',\n'
    str1 += '\t' + add_current_cnt_str + ',\n'
    str1 += '\t' + timeout_fun_str + ',\n'
    str1 += '};\n\n'
    tar_f.write(str1)

    # define canstack_filter_x[]
    str1 = 'cuint32_t canstack_filter_' + channel_str + '[] __at(CANSTACK_FILTER_ADD_' + channel_str + ')=\n'
    str1 += '{\n'
    count = 0
    while count < len(msg_upper_name_list):
        str1 += '\tCAN_' +msg_upper_name_list[count] + '_ID,			0xFFFFFFFF,\n'
        count += 1
    str1 += '};\n\n'
    tar_f.write(str1)

    # define can_filter_manager_x
    str1 = 'can_filter_manager_t	can_filter_manager_' + channel_str + ' __at(CAN_FILTER_MANAGER_ADD_' + channel_str + ')=\n'
    str1 += '{\n'
    str1 += '\t' + 'ARRAY_SIZE(' + 'canstack_filter_' + channel_str + ') / 2,\n'
    str1 += '\tcanstack_filter_' + channel_str + ',\n'
    str1 += '};\n\n'
    tar_f.write(str1)

    # define get_timeout_flag_x
    str1 = get_timeout_flag_def_str + '\n'
    str1 += '{\n'
    str1 += '\treturn (*(cuint8_t*)(CAN_TIMEOUT_FLAG_ADD_BASE_' + channel_str + ' + index));\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define get_limit_cnt_x
    str1 = get_limit_cnt_def_str + '\n'
    str1 += '{\n'
    str1 += '\treturn msg_infor_' + channel_str + '[index].u16LimitCnt;\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define get_current_cnt_x
    str1 = get_current_cnt_def_str + '\n'
    str1 += '{\n'
    str1 += '\treturn *( (cuint16_t*)CAN_CURRENT_CNT_ADD_BASE_' + channel_str + ' + index );\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define add_current_cnt_x
    str1 = add_current_cnt_def_str + '\n'
    str1 += '{\n'
    str1 += '\t*( (cuint16_t*)CAN_CURRENT_CNT_ADD_BASE_' + channel_str + ' + index ) += 1;\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define timeout_fun_x
    str1 = timeout_fun_def_str + '\n'
    str1 += '{\n'
    str1 += '\tmessage_timeout_fun_' + channel_str + '(0, msg_infor_' + channel_str + '[index].u8MsgType);\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define message_timeout_fun_x
    str1 = message_timeout_fun_def_str + '\n'
    str1 += '{\n'
    str1 += '\t*( (cuint16_t *)CAN_CURRENT_CNT_ADD_BASE_' + channel_str + ' + index ) = 0;\n'
    str1 += '\t*( (cuint8_t *)CAN_TIMEOUT_FLAG_ADD_BASE_' + channel_str + ' + index ) = c_True;\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define message_recv_fun_x
    str1 = message_recv_fun_def_str + '\n'
    str1 += '{\n'
    str1 += '\tmemcpy(\n'
    str1 += '\t\t( (cuint8_t *)CAN_DATA_ARRAY_ADD_BASE_' + channel_str + ' + index * DATA_ARRAY_NEED_SIZE),\n'
    str1 += '\t\t(cuint8_t *)parg,\n'
    str1 += '\t\tDATA_ARRAY_SIZE\n'
    str1 += '\t\t);\n\n'
    str1 += '\t*( (cuint16_t *)CAN_CURRENT_CNT_ADD_BASE_' + channel_str + ' + index ) = 0;\n'
    str1 += '\t*( (cuint8_t *)CAN_TIMEOUT_FLAG_ADD_BASE_' + channel_str + ' + index ) = c_False;\n'
    str1 += '}\n\n'
    tar_f.write(str1)

    # define can_parser_chx
    str1 = 'cint8_t can_parser_ch' + channel_str + '(CAN_Message_Type * m)\n'
    str1 += '{\n'
    str1 += '\tif(m->dlc != 8)\n'
    str1 += '\t{\n'
    str1 += '\t\treturn -1;\n'
    str1 += '\t}\n\n'

    str1 += '\tswitch(m->id)\n'
    str1 += '\t{\n'

    count = 0
    while count < len(msg_upper_name_list):
        str1 += '\t\tcase CAN_' + msg_upper_name_list[count] + '_ID:\n'
        str1 += '\t\t\t' + message_recv_fun_str + '(m->data, (cuint8_t)' + msg_upper_name_list[count] + ');\n'
        str1 += '\t\t\tbreak;\n'
        count += 1

    str1 += '\t\tdefault:\n'
    str1 += '\t\t\tbreak;\n'
    str1 += '\t}\n\n'
    str1 += '\treturn 0;\n'

    str1 += '}\n'
    tar_f.write(str1)

    str1 = '#endif\n\n#endif\n'
    tar_f.write(str1)

    tar_f.close()

    print('create msg.c file success!')


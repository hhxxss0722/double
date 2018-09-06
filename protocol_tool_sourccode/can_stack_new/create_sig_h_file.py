# -*- coding: utf-8 -*-
'''creat_sig_h_file module'''

# def create_sig_h_file(root_path, out_path, message_list, dbc_file_name):
def create_sig_h_file(root_path, sig_h_output_path, dbc_list, all_sig_sum):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or dbc list is None!')

    target_sig_h_f_path = sig_h_output_path

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name

    try:
        tar_f = open(target_sig_h_f_path, 'w')

    except:
        raise TypeError('operate sig.h file fail!')

    str1 = '#ifndef CAN_STACK_' + valid_file_name.upper() + '_SIG_H\n'
    str1 += '#define CAN_STACK_' + valid_file_name.upper() + '_SIG_H\n\n'
    str1 += '#include \"canstack_sig.h\"\n\n'
    str1 += '#ifdef CANSTACK_' + valid_file_name.upper() + '\n\n'

    str1 += '#define SIG_SUM		' + str(all_sig_sum) + '\n'
    str1 += '#include \"canstack_add_size_list.h\"\n\n'

    tar_f.write(str1)
    # for dbc in dbc_list:
    #     message_list = dbc.message_list
    #     str1 = '\n/********************' + 'can_' + str(dbc.can_channel) + '********************/'
    #     tar_f.write(str1)
    #     for message in message_list:
    #         tar_f.write('\n')
    #
    #         str1 = '/* ' + message.name + ':'+ message.ID + ' */'
    #         tar_f.write(str1)
    #         tar_f.write('\n')
    #
    #         for sig in message.sig_list:
    #             str1 = 'CANSTACK_DECLARE_SGINAL(' + sig.name + ', '  + sig.get_data_type() + ');' + '\n'
    #             tar_f.write(str1)

    str1 = '\n' + '#endif' + '\n' + '\n' + '#endif\n'

    tar_f.write(str1)

    tar_f.close()

    print('create sig.h file success!')
